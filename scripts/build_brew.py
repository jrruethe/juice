#!/usr/bin/env python3
"""build_brew.py — regenerate a version's Homebrewery brew from its tables.

The D8 model:

   tables/<table>/<table>.json
                            the META table: {header, template, dice, columns,
                            rows}; rows[i] = "*" (auto 1..N, printed bold)
                            | [values…] (number column, verbatim)
                            | "<table>_<n>.json" (content column)
   tables/<table>/json/<table>_<n>.json
                            a content column: {header, rows}
   tables/<table>/text/, tables/<table>/markdown/
                            the per-column dumps (written by --dump)
   tables/index.json        ordered list of meta file names
  homebrewery/template/<name>.md.j2
                           a TEMPLATE: the brew with [[table:<id>]] and
                           [[template:<id>]] placeholders
                           (e.g. pocketfold.md.j2, screen.md.j2)
   homebrewery/layout/<name>.json
                            a PAPER: orientation, paper size (paper_w_in,
                            paper_h_in), padding_em, gutter_em, and an
                            optional paper_name (used in the style's
                            comments) (e.g. usletter.json, a4.json)
   homebrewery/patches/<template>_<paper>.patch
                            OPTIONAL: a unified-diff tweak applied to the
                            rendered doc in memory before it is written —
                            paper-specific cosmetics (e.g. A4 wording or
                            font-size wraps) that the shared template must
                            not carry. The build fails loudly if a hunk no
                            longer matches the render (regenerate: build
                            with --no-patch, re-tweak a copy, diff -u).
   homebrewery/output/<template>_<paper>.md
                            the generated brew — one per template x paper
                            combination (pocketfold_usletter.md,
                            pocketfold_a4.md, screen_usletter.md, …)

Templates and papers are independent axes: any template builds with any
paper. A template's <style> block may use jinja: it includes
shared/style.css.j2 (the shared rules) and takes its geometry numbers from
the chosen layout file — the script computes the derived values (halves,
quarters) since CSS calc() cannot divide. A <style> block without jinja
passes through unchanged (and needs no layout values).

Running this rebuilds the chosen variant's brew doc:
  [[table:<id>]]     -> the composite table, rendered from the meta
  [[template:<id>]]  -> the {{template}} block from the meta

Both are emitted from the meta — change a column file (or the meta), re-run,
and the brew doc regenerates.

Rendering rules (the "pretty" format):
  * every header/data cell gets at least one space on each side
  * column width = longest cell (markup included) + 2; cells centered
  * pipes align across every row; the separator row is tight (|:---:|)
  * "*" number columns print bold; inline number columns print verbatim
  * a meta's optional "colspans" prints header spans the renderer's way:
    a colspan-s header cell carries s pipes (`| A || B |`) and is padded
    across the full span — the combined width of the s columns it covers —
    so the remaining header cells stay aligned with the separator row; the
    spanned-over columns (which must have empty headers) have no cell of
    their own in the header line
  * a data cell ending in ^ is right-justified so the caret sits flush
    against the closing pipe (the renderer's rowspan marker; a space after
    it would print a literal ^ instead of merging into the cell above)

With --dump it also writes the per-column dumps
(tables/<table>/text/<col>.txt and tables/<table>/markdown/<col>.md).

Usage:
  python3 scripts/build_brew.py <version_dir> [--version juice_smoothie] \
      [--template NAME] [--paper NAME] [--all] [--dump] [--no-patch]

    --template NAME --paper NAME
                            one variant: homebrewery/template/NAME.md.j2
                            with homebrewery/layout/NAME.json
                            -> homebrewery/output/<template>_<paper>.md
    --all (also the default when neither flag is given)
                            every template/ x layout/ combination that
                            exists
    --dump
                            also write the per-column dumps
    --no-patch
                            skip homebrewery/patches/<template>_<paper>.patch
                            (use when regenerating a patch against a
                            changed render)
"""

import argparse
import json
import re
import sys
from pathlib import Path


def center(cell, width):
    pad = width - len(cell)
    left = pad // 2
    return " " * left + cell + " " * (pad - left)


def load_meta(vdir, name):
    p = vdir / "tables" / name / f"{name}.json"
    if not p.exists():
        sys.exit(f"missing meta file: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def load_col(vdir, tid, name):
    p = vdir / "tables" / tid / "json" / name  # name = "<tid>_<n>.json"
    if not p.exists():
        sys.exit(f"missing column file: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def resolve(meta, tid, vdir):
    """meta -> (n, [(header, display_values, bold), …]) in printed order."""
    refs = meta["rows"]
    headers = meta["columns"]
    if len(refs) != len(headers):
        sys.exit(f"{meta and meta.get('header')}: columns/rows length mismatch")
    vals = []
    n = None
    for i, ref in enumerate(refs):
        if ref == "*":
            v = None  # synthesized once n is known
        elif isinstance(ref, list):
            v = ref
        else:
            v = load_col(vdir, tid, ref)["rows"]
            if n is None:
                n = len(v)
        if v is not None:
            if n is None:
                n = len(v)
            elif len(v) != n:
                sys.exit(f"{headers[i]!r}: {len(v)} rows, expected {n}")
        vals.append(v)
    out = []
    for i, (ref, h) in enumerate(zip(refs, headers)):
        if ref == "*":
            out.append((h, [f"**{i + 1}**" for i in range(n)], True))
        elif isinstance(ref, list):
            out.append((h, ref, False))  # verbatim — the author's markup
        else:
            out.append((h, vals[i], False))
    return n, out


def render_table(meta, cols):
    n = len(cols[0][1])
    for h, rows, _ in cols:
        if len(rows) != n:
            sys.exit(f"{meta['header']}: column {h!r} has {len(rows)} rows, "
                     f"expected {n}")
    headers = [h for h, _, _ in cols]
    ncols = len(cols)
    spans = meta.get("colspans", [1] * ncols)
    if len(spans) != ncols:
        sys.exit(f"{meta['header']}: colspans covers {len(spans)} columns, "
                 f"expected {ncols}")
    widths = [max(len(headers[j]), max(len(cols[j][1][i]) for i in range(n))) + 2
              for j in range(ncols)]
    lines = []
    # Header: a cell with colspan s > 1 is padded across the FULL span —
    # the combined width of the s columns it covers — so the header cells
    # after it stay aligned with the separator row (which keeps every
    # column's width); it carries s pipes — the trailing pipes ARE the
    # colspan to the renderer — and the spanned-over columns have no cell
    # of their own in the line.
    cells, j = [], 0
    while j < ncols:
        s = spans[j]
        if s == 0:
            sys.exit(f"{meta['header']}: broken colspans at column "
                     f"{headers[j]!r} (a 0 must follow its span)")
        if s > 1:
            for r in range(1, s):
                if headers[j + r] != "":
                    sys.exit(f"{meta['header']}: spanned-over header "
                             f"{headers[j + r]!r} is not empty")
            w = sum(widths[j:j + s])
            cells.append(" " + headers[j].ljust(w - 2) + " "
                         + "|" * (s - 1))
            j += s
        else:
            cells.append(" " + center(headers[j], widths[j] - 2) + " ")
            j += 1
    lines.append("|" + "|".join(cells) + "|")
    lines.append("|" + "|".join(":" + "-" * (w - 2) + ":" for w in widths) + "|")
    for i in range(n):
        cells = []
        for j in range(ncols):
            c = cols[j][1][i]
            if c.strip().endswith("^"):
                # a trailing ^ is the renderer's rowspan marker: it merges
                # this cell into the one above, so it must sit flush against
                # the closing pipe (any space after it breaks the merge)
                cells.append(" " * (widths[j] - len(c)) + c)
            else:
                cells.append(" " + center(c, widths[j] - 2) + " ")
        lines.append("|" + "|".join(cells) + "|")
    return "\n".join(lines)


def layout_vars(vdir, root, layout_path=None):
    """layout/<name>.json -> the jinja variables the <style> renders with."""
    if layout_path is None:
        sys.exit("the template's <style> block uses jinja but no layout "
                 "file was given (pick one with --paper, or run with --all)")
    lj_p = layout_path
    if not lj_p.exists():
        sys.exit(f"the template's <style> block uses jinja but {lj_p} is missing")
    lj = json.loads(lj_p.read_text(encoding="utf-8"))
    for k in ("orientation", "paper_w_in", "paper_h_in", "padding_em", "gutter_em"):
        if k not in lj:
            sys.exit(f"{lj_p}: missing key {k!r}")
    pad, gut, hg = lj["padding_em"], lj["gutter_em"], lj["gutter_em"] / 2
    fmt = lambda x: f"{x:g}em"
    v = {
        "paper_name": lj.get("paper_name", "US Letter"),
        "orientation": lj["orientation"],
        "page_w": f"{lj['paper_w_in']:g}in",
        "page_h": f"{lj['paper_h_in']:g}in",
        "padding": fmt(pad),
        "gutter": fmt(gut),
        "half_gutter": fmt(hg),
    }
    if lj["orientation"] == "portrait":
        # 4 rows x 2 cols on page 2; the fold lines run at 1/4, 1/2, 3/4 of
        # the paper's height, so rows are measured in the paper's height
        # quarters; the sideways-box width swap uses the paper's width.
        qh = lj["paper_h_in"] / 4
        v["quarter_h"] = f"{qh:g}in"
        v["row_outer_h"] = f"calc({qh:g}in - {fmt(pad)})"
        v["row_inner_h"] = f"{qh:g}in"
        v["lr_short_w"] = f"calc({qh:g}in - {fmt(pad + hg)})"
        v["lr_full_w"] = f"calc({qh:g}in - {fmt(gut)})"
        v["lr_h"] = f"calc({lj['paper_w_in'] / 2:g}in - {fmt(pad + hg)})"
    else:
        # 4-column top row on page 2; the fold lines run at 1/4, 1/2, 3/4 of
        # the paper's width, so columns are measured in its width quarters.
        qw = lj["paper_w_in"] / 4
        v["quarter_w"] = f"{qw:g}in"
        v["col_outer_w"] = f"calc({qw:g}in - {fmt(pad)})"
        v["col_inner_w"] = f"{qw:g}in"
    return v


def render_template_style(template, vdir, root, layout_path=None):
    """Render the template's <style> block with jinja, if it uses jinja."""
    if "<style>" not in template:
        return template
    pre, rest = template.split("<style>", 1)
    style_src, post = rest.split("</style>", 1)
    if "{{" not in style_src and "{%" not in style_src:
        return template  # plain style block — pass through unchanged
    import jinja2
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(root),
        trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True)
    style = env.from_string(style_src).render(
        **layout_vars(vdir, root, layout_path))
    return pre + "<style>" + style + "</style>" + post


def find_template(vdir, name, required=True):
    """A template file: homebrewery/template/<name>.md.j2. Returns None
    when not found and required is False."""
    p = vdir / "homebrewery" / "template" / f"{name}.md.j2"
    if p.exists():
        return p
    if required:
        sys.exit(f"missing template: {p}")
    return None


def find_layout(vdir, name, required=True):
    """A layout file: homebrewery/layout/<name>.json (the paper's
    geometry). May be absent (a plain, non-jinja <style> needs no layout
    values) unless required. Returns the path or None."""
    p = vdir / "homebrewery" / "layout" / f"{name}.json"
    if p.exists():
        return p
    if required:
        sys.exit(f"missing layout: {p}")
    return None


def parse_patch(patch_path):
    """A unified diff -> [(old_start, old_lines, new_lines), …], in order.
    The file headers (---/+++) are ignored — only the hunks matter. Each
    hunk's parsed line counts are checked against the counts its header
    claims, so a mangled patch file fails loudly instead of silently
    corrupting the doc."""
    hunks, hunk = [], None
    for line in patch_path.read_text(encoding="utf-8").split("\n"):
        if line.startswith("@@"):
            if hunk is not None:
                exp = hunk[0]
                if len(hunk[1]) != exp[0] or len(hunk[2]) != exp[1]:
                    sys.exit(f"{patch_path}: hunk at old line {hunk[3]} parsed "
                             f"as {len(hunk[1])} old / {len(hunk[2])} new lines, "
                             f"header claims {exp[0]} / {exp[1]}")
            m = re.fullmatch(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*", line)
            if not m:
                sys.exit(f"{patch_path}: bad hunk header {line!r}")
            hunk = [
                (int(m.group(2) or 1), int(m.group(4) or 1)),  # claimed counts
                [], [], int(m.group(1)),
            ]
            hunks.append(hunk)
        elif hunk is not None:
            if line.startswith("\\"):
                continue  # "\ No newline at end of file" — we never emit these
            if line[:1] in (" ", "-", "+"):
                if line[0] != "-":
                    hunk[2].append(line[1:])  # context AND added lines: new side
                if line[0] != "+":
                    hunk[1].append(line[1:])  # context AND removed lines: old side
    if hunk is not None:
        exp = hunk[0]
        if len(hunk[1]) != exp[0] or len(hunk[2]) != exp[1]:
            sys.exit(f"{patch_path}: hunk at old line {hunk[3]} parsed as "
                     f"{len(hunk[1])} old / {len(hunk[2])} new lines, header "
                     f"claims {exp[0]} / {exp[1]}")
    return [(h[3], h[1], h[2]) for h in hunks]


def apply_patch(doc, patch_path):
    """Apply a unified-diff patch to the rendered doc, in memory (old->new).
    Each hunk must match its old-side lines exactly — first at the recorded
    position (drift-adjusted for earlier hunks), then anywhere in the doc;
    a hunk with zero or multiple matches means the tables/template changed
    since the patch was made, so the build fails loudly rather than writing
    a doc that silently lost its tweaks."""
    lines = doc.split("\n")
    delta = 0
    for i, (start, old, new) in enumerate(parse_patch(patch_path), 1):
        pos = start - 1 + delta
        if pos >= 0 and old and lines[pos:pos + len(old)] == old:
            pass
        elif old:
            matches = [k for k in range(max(0, pos - 200),
                                        len(lines) - len(old) + 1)
                       if lines[k:k + len(old)] == old]
            if len(matches) != 1:
                sys.exit(f"{patch_path}: hunk {i} does not match the rendered "
                         f"doc ({len(matches)} matches) — the tables or "
                         f"template changed since the patch was made; "
                         f"regenerate it (build with --no-patch, re-tweak a "
                         f"copy of the output, diff -u, see "
                         f"docs/TABLE_FORMATS.md)")
            pos = matches[0]
        # an empty old is a pure insertion: the header's start is the last
        # unchanged line, so the new lines go after it
        if not old:
            pos = start + delta
        lines[pos:pos + len(old)] = new
        delta += len(new) - len(old)
    return "\n".join(lines)


def build_variant(vdir, root, template_path, layout_path, out_name, no_patch=False):
    """Build one variant: render the template's style, QA the placeholders,
    splice in every table, apply the variant's patch (if any), write
    homebrewery/<out_name>."""
    template = render_template_style(template_path.read_text(encoding="utf-8"),
                                     vdir, root, layout_path)
    index = json.loads((vdir / "tables" / "index.json").read_text(encoding="utf-8"))

    # --- QA: placeholders and metas agree, in both directions ------------
    found_tables = set(re.findall(r"\[\[table:([a-z0-9_]+)\]\]", template))
    found_templates = set(re.findall(r"\[\[template:([a-z0-9_]+)\]\]", template))
    meta_ids = [name[:-5] for name in index]  # <id> from <id>.json
    if found_tables != set(meta_ids):
        sys.exit(f"[[table:…]] mismatch:\n  template: {sorted(found_tables)}\n"
                 f"  index:    {sorted(meta_ids)}")
    for name in index:
        m = load_meta(vdir, name[:-5])
        tid = name[:-5]
        has_ph = tid in found_templates
        if (m["template"] != "") != has_ph:
            sys.exit(f"{name}: template field is "
                     f"{'empty' if m['template'] == '' else 'set'} but "
                     f"[[template:{tid}]] is {'missing' if not has_ph else 'present'}")

    # --- QA: nothing table-shaped may remain in the template --------------
    stray = [l for l in template.split("\n") if l.lstrip().startswith("|")]
    if stray:
        sys.exit(f"template still contains {len(stray)} markdown table lines")
    if "{{template" in template:
        sys.exit("template still contains a {{template}} block")

    doc = template
    for name in index:
        meta = load_meta(vdir, name[:-5])
        tid = name[:-5]
        n, cols = resolve(meta, tid, vdir)
        doc = doc.replace(f"[[table:{tid}]]", render_table(meta, cols))
        if tid in found_templates:
            doc = doc.replace(f"[[template:{tid}]]",
                              "{{template\n" + meta["template"] + "\n}}")
    if "[[" in doc:
        sys.exit("unreplaced placeholder left in output")

    out_dir = vdir / "homebrewery" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / out_name

    patch_path = vdir / "homebrewery" / "patches" / (out_name[:-3] + ".patch")
    if patch_path.exists():
        if no_patch:
            print(f"skipped {patch_path} (--no-patch)")
        else:
            doc = apply_patch(doc, patch_path)
            print(f"patched {out_path} with {patch_path}")

    out_path.write_text(doc, encoding="utf-8")
    summary = ", ".join(f"{name[:-5]}({len(load_meta(vdir, name[:-5])['rows'])}c)"
                        for name in index)
    print(f"rebuilt {out_path} — {len(index)} tables: {summary}")


def dump_columns(vdir):
    """Write the per-column dumps (tables/<col>.txt / .md)."""
    index = json.loads((vdir / "tables" / "index.json").read_text(encoding="utf-8"))
    dumped = 0
    for name in index:
        meta = load_meta(vdir, name[:-5])
        for ref in meta["rows"]:
            if ref == "*" or isinstance(ref, list):
                continue  # number columns have no files to dump
            col = load_col(vdir, name[:-5], ref)
            tdir = vdir / "tables" / name[:-5]
            (tdir / "text").mkdir(parents=True, exist_ok=True)
            (tdir / "markdown").mkdir(parents=True, exist_ok=True)
            (tdir / "text" / (ref[:-5] + ".txt")).write_text(
                "\n".join(col["rows"]) + "\n", encoding="utf-8")
            w = max(len(col["header"]),
                    max(len(r) for r in col["rows"])) + 2
            md = ["|" + " " + center("#", 1) + " |"
                  + " " + center(col["header"], w - 2) + " |",
                  "|:" + "-" * 1 + ":|:" + "-" * (w - 2) + ":|"]
            for i, r in enumerate(col["rows"]):
                md.append("|" + " " + center(str(i + 1), 1) + " |"
                          + " " + center(r, w - 2) + " |")
            (tdir / "markdown" / (ref[:-5] + ".md")).write_text(
                "\n".join(md) + "\n", encoding="utf-8")
            dumped += 1
    print(f"dumped {dumped} columns to .txt/.md")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("version_dir")
    ap.add_argument("--version", default=None,
                    help='informational (e.g. "juice_smoothie")')
    ap.add_argument("--template", default=None,
                    help="homebrewery/template/<name>.md.j2 to build "
                         "(with --paper)")
    ap.add_argument("--paper", default=None,
                    help="homebrewery/layout/<name>.json to build with "
                         "(with --template)")
    ap.add_argument("--all", action="store_true",
                    help="build every template/ x layout/ combination that "
                         "exists (also the default when neither --template "
                         "nor --paper is given)")
    ap.add_argument("--dump", action="store_true",
                    help="also write tables/<col>.txt and .md for content columns")
    ap.add_argument("--no-patch", action="store_true",
                    help="skip homebrewery/patches/<template>_<paper>.patch "
                         "(use when regenerating a patch)")
    args = ap.parse_args()

    vdir = Path(args.version_dir)
    root = vdir.resolve().parent
    hdir = vdir / "homebrewery"

    if args.all or (args.template is None and args.paper is None):
        tdir, ldir = hdir / "template", hdir / "layout"
        tnames = sorted(p.name[:-len(".md.j2")]
                        for p in tdir.glob("*.md.j2")) if tdir.is_dir() else []
        pnames = sorted(p.stem for p in ldir.glob("*.json")) if ldir.is_dir() else []
        if not tnames:
            sys.exit(f"no templates found in {tdir} (template/<name>.md.j2)")
        if not pnames:
            sys.exit(f"no layouts found in {ldir} (layout/<name>.json)")
        combos = [(find_template(vdir, t), find_layout(vdir, p),
                   f"{t}_{p}.md") for t in tnames for p in pnames]
    else:
        if args.template is None or args.paper is None:
            sys.exit("give both --template and --paper, or --all")
        combos = [(find_template(vdir, args.template),
                   find_layout(vdir, args.paper),
                   f"{args.template}_{args.paper}.md")]

    for tpath, lpath, out_name in combos:
        build_variant(vdir, root, tpath, lpath, out_name, no_patch=args.no_patch)
    if args.dump:
        dump_columns(vdir)


if __name__ == "__main__":
    main()
