#!/usr/bin/env python3
"""build_pregen.py — generate a pregenerated adventure brew.

The same template x paper mechanism as build_brew.py, except the
placeholders are filled by RUNNING scripts/roll.py — so every run
produces a fresh random pregen (this builder is non-deterministic by
design; the double-build md5 check does not apply to it):

   pregen/homebrewery/template/<name>.md.j2
                            the TEMPLATE: the brew with each generated
                            table replaced by a [[gen:<key>]] placeholder
                            (e.g. pregen.md.j2). Body = plain Homebrewery
                            markdown; only the <style> block uses jinja
                            (shared style + the paper's geometry), as in
                            build_brew.py
   pregen/homebrewery/layout/<paper>.json
                            a PAPER (usletter.json, a4.json)
   pregen/sections.json
                            the executable spec: [{name, roll: […],
                            header?}, …] in template order. name matches a
                            [[gen:<name>]] placeholder; roll is the
                            scripts/roll.py argument list (version dir
                            first), e.g. ["smoothie", "quest_start",
                            "-o", "md", "-n", "20"]; the optional header
                            retitles the table (roll.py's -H) — the
                            pregen's section titles can differ from the
                            tables' brew headers (adventure:
                            "Where do you Start?")
   pregen/homebrewery/output/<template>_<paper>.md
                            the generated pregen (pregen_usletter.md,
                            pregen_a4.md, …)

Usage:
  python3 scripts/build_pregen.py pregen [--template NAME] [--paper NAME]
      [--all]

    --template NAME --paper NAME   one variant
    --all (also the no-flag default)
                                   every template/ x layout/ combination
                                   that exists
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from build_brew import find_layout, find_template, render_template_style


def gen_sections(vdir):
    p = vdir / "sections.json"
    if not p.exists():
        sys.exit(f"missing sections manifest: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def roll_section(vdir, root, section):
    """Run the section's roll.py command; return its stdout (the table).
    The argument list is the README's command minus python3 and ./scripts/
    roll.py: [version_dir, table…], resolved against the repo root. An
    optional "header" key retitles the table (roll.py's -H) — the pregen's
    section titles can differ from the tables' brew headers."""
    args = [sys.executable, str(root / "scripts" / "roll.py"),
            str(root / section["roll"][0]), *section["roll"][1:]]
    if "header" in section:
        args += ["-H", section["header"]]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"{section['name']}: roll failed:\n{r.stderr or r.stdout}")
    return r.stdout.rstrip("\n")


def build_variant(vdir, root, template_path, layout_path, out_name):
    """Build one variant: render the template's style, QA the placeholders,
    roll every section, splice the tables in, write the output."""
    template = render_template_style(template_path.read_text(encoding="utf-8"),
                                     vdir, root, layout_path)
    sections = gen_sections(vdir)

    # --- QA: placeholders and manifest agree, in both directions --------
    found = set(re.findall(r"\[\[gen:([a-z0-9_]+)\]\]", template))
    names = [s["name"] for s in sections]
    if len(set(names)) != len(names):
        sys.exit(f"sections.json has duplicate names: "
                 f"{sorted(n for n in names if names.count(n) > 1)}")
    if found != set(names):
        sys.exit(f"[[gen:…]] mismatch:\n  template: {sorted(found)}\n"
                 f"  manifest: {sorted(names)}")

    # --- QA: nothing table-shaped may remain in the template ------------
    stray = [l for l in template.split("\n") if l.lstrip().startswith("|")]
    if stray:
        sys.exit(f"template still contains {len(stray)} markdown table "
                 f"lines — a section must come from sections.json")

    doc = template
    for s in sections:
        doc = doc.replace(f"[[gen:{s['name']}]]", roll_section(vdir, root, s))
    if "[[gen:" in doc:
        sys.exit("unreplaced placeholder left in output")

    out_dir = vdir / "homebrewery" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / out_name
    out_path.write_text(doc, encoding="utf-8")
    print(f"pregenerated {out_path} — {len(sections)} sections "
          f"(new random roll)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("version_dir")
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
        build_variant(vdir, root, tpath, lpath, out_name)


if __name__ == "__main__":
    main()
