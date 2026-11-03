#!/usr/bin/env python3
"""roll.py — roll one (or more) of a version's tables, Juice-style.

A playtest companion to build_brew.py: it reads the same table files the
generator uses and prints the result using the table's template from its
meta:

  python3 scripts/roll.py smoothie wilderness -c 5
  python3 scripts/roll.py smoothie conversation
  python3 scripts/roll.py pop quest            # the full quest sentence
  python3 scripts/roll.py pop oracle --die highest
  python3 scripts/roll.py smoothie quest_offer -c 10 -o md
  (a table id may also be given as its meta file name, e.g. "dialogue.json")

Rolling:
  * a table is rolled **per content column** — every content column gets its
    own roll of the table's die, and the face indexes that column's row
    (a full Pop! quest is 10d10: four columns on quest, three on person,
    three on location — so "Destroy Toxic Seal" is as valid as any row of
    the printed table). Number columns are lookup machinery only: they map
    a face to the printed row (d10-style `0` = face N; dual-`#` tables map
    the upper faces to the second `#`), they are never rolled themselves.
  * the sentence is the first table's meta template, with `[**Column**]`
    markers filled. A marker names a column of any already-rolled table.
    A marker that matches no rolled column but exactly ONE other table in
    the index (by header or alias) causes that table to be rolled too —
    so `roll.py pop quest` resolves Person and Location on its own.
    Markers with zero owners, or more than one, are left exactly as
    written: that is how template/header mismatches stay visible.
  * **aliases** let a template variable name a column whose printed header
    is longer or different: a meta may carry
    `"aliases": {"Motive": "Motive / Topic"}` — the printed header is
    untouched, the marker just resolves to that column's values.
  * dice `1dN`: one die per content column. dice `2d6`: one 2d6 roll per
    column; `--die left|highest|lowest` picks the die that indexes the row
    (the Juice oracle mechanic).
  * tables with an empty template print the rolled column values.
  * each roll prints as ONE line — the template's markdown line breaks
    collapse to single spaces.
  * `-o md` prints a pregenerated markdown table instead: a bold #
    column plus ONE column of each roll's full result (the tables'
    sentences concatenated with a space — exactly what txt mode prints),
    one row per roll; the second column's header is the given tables'
    meta headers joined. Rendered in the pocketfold's pretty format
    (build_brew's renderer), so it is paste-ready for a brew.
  * single-column tables (Pop!'s Next Scene: no printed # column) print the
    row's own value — a face i indexes row i (plain 1..N order).
  * a table directory may ship its own roll.py next to the meta
    (tables/<tid>/roll.py with a roll(vdir, tid, meta, die_choice)
    function) to take over the roll procedure entirely — used by Pop!'s
    Name, whose first roll picks a pattern that dictates how the rest
    of the table is rolled (pop/tables/name/roll.py).
  * hierarchical tables (Pop!'s Treasure, with its `^` marker rows) are
    rolled by hand from the brew.
"""

import argparse
import importlib.util
import json
import random
import re
import sys
from pathlib import Path

from build_brew import render_table


def load(vdir, name, tid=None):
    # name is a full file name: a meta ("quest.json" -> tables/quest/quest.json)
    # or a column ref ("quest_1.json" -> tables/quest/json/quest_1.json —
    # pass its table's tid)
    if tid is None:  # a meta: tables/<tid>/<tid>.json
        p = vdir / "tables" / name[:-5] / name
    else:  # a content column: tables/<tid>/json/<ref>
        p = vdir / "tables" / tid / "json" / name
    if not p.suffix:
        p = p.with_suffix(".json")
    return json.loads(p.read_text(encoding="utf-8"))


def roll_hook(vdir, tid, meta, die_choice):
    """A table directory may ship its own roll.py next to the meta
    (tables/<tid>/roll.py) with a roll(vdir, tid, meta, die_choice)
    -> [(header, value), …] function, for tables whose roll procedure
    is an algorithm the standard model can't express (Pop!'s Name
    pattern method). Returns the hook's result, or None if the table
    has no hook."""
    p = vdir / "tables" / tid / "roll.py"
    if not p.exists():
        return None
    spec = importlib.util.spec_from_file_location(f"roll_hook_{tid}", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.roll(vdir, tid, meta, die_choice)


def n_rows(meta, tid, vdir):
    for ref in meta["rows"]:
        if ref == "*":
            continue
        if isinstance(ref, list):
            return len(ref)
        return len(load(vdir, ref, tid)["rows"])
    return 0


def face_map(meta, tid, vdir):
    """face -> row index, from the table's number columns."""
    mapping = {}
    for i, ref in enumerate(meta["rows"]):
        if ref == "*":
            values = [str(i + 1) for i in range(n_rows(meta, tid, vdir))]
        elif isinstance(ref, list):
            values = [v.replace("*", "") for v in ref]
            if any(v == "^" for v in values):
                continue  # hierarchical rows (Treasure) — rolled by hand
        else:
            continue  # content columns don't map faces
        if all(v == "" or v.isdigit() for v in values):
            for k, v in enumerate(values):
                if v == "":
                    continue
                if v == "0":
                    # d10-style column: 1..N-1 plus 0, where 0 is face N
                    face = sum(1 for x in values if x != "0") + 1
                else:
                    face = int(v)
                mapping.setdefault(face, k)
        else:
            # a non-numeric column in the number slot (Next Scene: the
            # table's only column, no printed #) — face i indexes row i
            for k, v in enumerate(values):
                if v != "":
                    mapping.setdefault(k + 1, k)
    return mapping


def content_cols(meta, tid, vdir):
    """[(header, rows), …] for the table's content columns, in order."""
    out = []
    for i, ref in enumerate(meta["rows"]):
        if isinstance(ref, str) and ref != "*":
            out.append((meta["columns"][i], load(vdir, ref, tid)["rows"]))
    return out


def roll_table(vdir, tid, meta, die_choice):
    """Roll one table, per content column -> [(header, raw_value), …] in
    column order (a list, not a dict: two columns may share a header,
    e.g. Pop!'s Color)."""
    dice = meta["dice"]
    if dice.startswith("1d"):
        hi = int(dice[2:])

        def roll_face():
            return random.randint(1, hi)
    elif dice == "2d6":

        def roll_face():
            d1, d2 = random.randint(1, 6), random.randint(1, 6)
            return {"left": d1, "highest": max(d1, d2),
                    "lowest": min(d1, d2)}[die_choice]
    else:
        sys.exit(f"{meta['header']}: unsupported dice {dice!r}")
    fmap = face_map(meta, tid, vdir)
    vals = []
    for header, rows in content_cols(meta, tid, vdir):
        face = roll_face()
        idx = fmap.get(face)
        if idx is None:
            sys.exit(f"{meta['header'] or meta['dice']}: no row for face {face}")
        vals.append((header, rows[idx]))
    if not vals:
        # a single-column table (Next Scene): the column's own values are the
        # result — roll the die, take that row's value
        for i, ref in enumerate(meta["rows"]):
            if isinstance(ref, list):
                face = roll_face()
                idx = fmap.get(face)
                if idx is None:
                    sys.exit(f"{meta['header'] or meta['dice']}: no row for face {face}")
                vals.append((meta["columns"][i], ref[idx]))
                break
    return vals


def marker_value(marker, merged, aliases):
    """The value a marker names, or None if it can't be resolved."""
    if marker in merged:
        return merged[marker]
    header = aliases.get(marker)
    if header is not None and header in merged:
        return merged[header]
    return None


def render_rolls(rolls, text_header):
    """A pregenerated markdown table: a bold # column plus one column
    holding each roll's full result text, one row per roll. Rendered by
    build_brew.render_table, so the formatting is exactly the brew's
    (aligned pipes, centered cells, tight separator) — paste-ready."""
    meta = {"header": "rolls"}
    cols = [("#", [f"**{i + 1}**" for i in range(len(rolls))], True),
            (text_header, rolls, False)]
    return render_table(meta, cols)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("version_dir")
    ap.add_argument("tables", nargs="+", help="table id(s); one roll each")
    ap.add_argument("-c", type=int, default=1, help="number of rolls")
    ap.add_argument("--die", default="left",
                    choices=["left", "highest", "lowest"],
                    help="which die of the 2d6 roll indexes the row")
    ap.add_argument("-o", "--output", default="txt", choices=["txt", "md"],
                    help="txt (default): one filled sentence per roll; "
                         "md: a pretty markdown table of the rolled values "
                         "(the pocketfold format), one row per roll")
    args = ap.parse_args()

    vdir = Path(args.version_dir)
    index = json.loads((vdir / "tables" / "index.json").read_text(encoding="utf-8"))
    known = {name[:-5]: name for name in index}
    metas = []
    for t in args.tables:
        tid = t[:-5] if t.endswith(".json") else t
        if tid not in known:
            sys.exit(f"unknown table {tid!r}; index has: {sorted(known)}")
        metas.append(load(vdir, known[tid]))

    # name -> tables that own it (by column header or alias), index order.
    # A table that has two columns with the same header (Pop!'s Color) owns
    # the name once.
    all_metas = {name[:-5]: load(vdir, name) for name in index}
    owners = {}
    for tid, m in all_metas.items():
        for h in m["columns"]:
            if tid not in owners.setdefault(h, []):
                owners[h].append(tid)
        for a in m.get("aliases", {}):
            if tid not in owners.setdefault(a, []):
                owners[a].append(tid)

    # the md table's second-column header: the given tables' meta headers
    # joined (" / "); one table -> just its header
    md_header = " / ".join(
        (m.get("header") or (t[:-5] if t.endswith(".json") else t))
        for t, m in zip(args.tables, metas))

    rolls = []
    for _ in range(args.c):
        merged = {}
        aliases = {}
        rolled_ids = []
        for i, meta in enumerate(metas):
            tid = args.tables[i][:-5] if args.tables[i].endswith(".json") \
                else args.tables[i]
            pairs = roll_hook(vdir, tid, meta, args.die)
            if pairs is None:
                pairs = roll_table(vdir, tid, meta, args.die)
            merged.update(dict(pairs))
            aliases.update(meta.get("aliases", {}))
            rolled_ids.append(tid)

        texts = []
        for meta in metas:
            if meta.get("template"):
                # a marker this table's template can't resolve from what is
                # already rolled, but exactly one un-rolled table owns, rolls
                # that table too
                for mk in dict.fromkeys(re.findall(r"\*\*([^*]+)\*\*",
                                                  meta["template"])):
                    if marker_value(mk, merged, aliases) is not None:
                        continue
                    owning = [t for t in owners.get(mk, [])
                              if t not in rolled_ids]
                    if len(owning) == 1:
                        am = all_metas[owning[0]]
                        pairs = roll_table(vdir, owning[0], am, args.die)
                        merged.update(dict(pairs))
                        aliases.update(am.get("aliases", {}))
                        rolled_ids.append(owning[0])

                def fill(m):
                    v = marker_value(m.group(1), merged, aliases)
                    return m.group(0) if v is None else v.replace("*", "")
                # [**X**] is the placeholder syntax; **X** also fills.
                text = re.sub(r"\[\*\*([^*]+)\*\*\]", fill, meta["template"])
                text = re.sub(r"\*\*([^*]+)\*\*", fill, text)
            else:
                # no template: this table's own rolled values
                text = "  ".join(v.replace("*", "") for _, v in pairs)
            # markdown line breaks collapse to single spaces, so each
            # table's result is one line
            texts.append(re.sub(r"\s+", " ", text).strip())
        if args.output == "md":
            # the table row is the same concatenated text the txt mode
            # would print
            rolls.append(" ".join(texts))
        else:
            # multiple tables print one line each, concatenated with a space
            print(" ".join(texts))
    if args.output == "md":
        print(render_rolls(rolls, md_header))


if __name__ == "__main__":
    main()
