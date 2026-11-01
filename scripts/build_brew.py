#!/usr/bin/env python3
"""build_brew.py — regenerate a version's Homebrewery brew from its tables.

The D8 model:

  tables/<table>.json      the META table: {header, template, dice, columns,
                           rows}; rows[i] = "*" (auto 1..N, printed bold)
                           | [values…] (number column, verbatim)
                           | "<table>_<n>.json" (content column)
  tables/<table>_<n>.json  a content column: {header, rows}
  tables/index.json        ordered list of meta file names
  homebrewery/template.md.j2  the brew with [[table:<id>]] and
                           [[template:<id>]] placeholders. The <style> block may
                           use jinja: it includes ../shared/style.css.j2 (the
                           shared rules) and takes its geometry numbers from
                           homebrewery/layout.json (orientation, paper size,
                           padding_em, gutter_em) — the script computes the
                           derived values (halves, quarters) since CSS calc()
                           cannot divide. A <style> block without jinja passes
                           through unchanged.

Running this rebuilds homebrewery/pocketfold.md:
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

With --dump it also writes the per-column dumps (tables/<col>.txt / .md).

Usage:
  python3 scripts/build_brew.py <version_dir> [--version juice_smoothie] [--dump]
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
    p = vdir / "tables" / f"{name}.json"
    if not p.exists():
        sys.exit(f"missing meta file: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def load_col(vdir, name):
    p = vdir / "tables" / name  # ref is the full file name, e.g. "quest_1.json"
    if not p.exists():
        sys.exit(f"missing column file: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def resolve(meta, vdir):
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
            v = load_col(vdir, ref)["rows"]
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


def layout_vars(vdir, root):
    """layout.json -> the jinja variables the <style> block renders with."""
    lj_p = vdir / "homebrewery" / "layout.json"
    if not lj_p.exists():
        sys.exit(f"the template's <style> block uses jinja but {lj_p} is missing")
    lj = json.loads(lj_p.read_text(encoding="utf-8"))
    for k in ("orientation", "paper_w_in", "paper_h_in", "padding_em", "gutter_em"):
        if k not in lj:
            sys.exit(f"{lj_p}: missing key {k!r}")
    pad, gut, hg = lj["padding_em"], lj["gutter_em"], lj["gutter_em"] / 2
    fmt = lambda x: f"{x:g}em"
    v = {
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


def render_template_style(template, vdir, root):
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
    style = env.from_string(style_src).render(**layout_vars(vdir, root))
    return pre + "<style>" + style + "</style>" + post


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("version_dir")
    ap.add_argument("--version", default=None,
                    help='informational (e.g. "juice_smoothie")')
    ap.add_argument("--dump", action="store_true",
                    help="also write tables/<col>.txt and .md for content columns")
    args = ap.parse_args()

    vdir = Path(args.version_dir)
    template_path = vdir / "homebrewery" / "template.md.j2"
    if not template_path.exists():
        template_path = vdir / "homebrewery" / "template.md"
    if not template_path.exists():
        sys.exit(f"missing template: {vdir}/homebrewery/template.md.j2")
    out_path = vdir / "homebrewery" / "pocketfold.md"
    template = render_template_style(template_path.read_text(encoding="utf-8"),
                                     vdir, vdir.resolve().parent)
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
        n, cols = resolve(meta, vdir)
        doc = doc.replace(f"[[table:{tid}]]", render_table(meta, cols))
        if tid in found_templates:
            doc = doc.replace(f"[[template:{tid}]]",
                              "{{template\n" + meta["template"] + "\n}}")
    if "[[" in doc:
        sys.exit("unreplaced placeholder left in output")

    out_path.write_text(doc, encoding="utf-8")
    summary = ", ".join(f"{name[:-5]}({len(load_meta(vdir, name[:-5])['rows'])}c)"
                        for name in index)
    print(f"rebuilt {out_path} — {len(index)} tables: {summary}")

    if args.dump:
        dumped = 0
        for name in index:
            meta = load_meta(vdir, name[:-5])
            for ref in meta["rows"]:
                if ref == "*" or isinstance(ref, list):
                    continue  # number columns have no files to dump
                col = load_col(vdir, ref)
                base = vdir / "tables" / ref[:-5]
                (base.with_suffix(".txt")).write_text(
                    "\n".join(col["rows"]) + "\n", encoding="utf-8")
                w = max(len(col["header"]),
                        max(len(r) for r in col["rows"])) + 2
                md = ["|" + " " + center("#", 1) + " |"
                      + " " + center(col["header"], w - 2) + " |",
                      "|:" + "-" * 1 + ":|:" + "-" * (w - 2) + ":|"]
                for i, r in enumerate(col["rows"]):
                    md.append("|" + " " + center(str(i + 1), 1) + " |"
                              + " " + center(r, w - 2) + " |")
                (base.with_suffix(".md")).write_text("\n".join(md) + "\n",
                                                     encoding="utf-8")
                dumped += 1
        print(f"dumped {dumped} columns to .txt/.md")


if __name__ == "__main__":
    main()
