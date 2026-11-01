#!/usr/bin/env python3
"""roll.py — roll one (or more) of a version's tables, Juice-style.

A playtest companion to build_brew.py: it reads the same table files the
generator uses and prints the result using the table's template from its
meta:

  python3 scripts/roll.py smoothie wilderness -c 5
  python3 scripts/roll.py smoothie conversation
  python3 scripts/roll.py pop quest            # the full quest sentence
  python3 scripts/roll.py pop oracle --die highest
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
  * single-column tables (Pop!'s Next Scene: no printed # column) print the
    row's own value — a face i indexes row i (plain 1..N order).
  * hierarchical tables (Pop!'s Treasure, with its `^` marker rows) are
    rolled by hand from the brew.
"""

import argparse
import json
import random
import re
import sys
from pathlib import Path


def load(vdir, name):
    # name is a full file name: a meta ("quest.json") or a column ref ("quest_1.json")
    p = vdir / "tables" / name
    if not p.suffix:
        p = p.with_suffix(".json")
    return json.loads(p.read_text(encoding="utf-8"))


def n_rows(meta, vdir):
    for ref in meta["rows"]:
        if ref == "*":
            continue
        if isinstance(ref, list):
            return len(ref)
        return len(load(vdir, ref)["rows"])
    return 0


def face_map(meta, vdir):
    """face -> row index, from the table's number columns."""
    mapping = {}
    for i, ref in enumerate(meta["rows"]):
        if ref == "*":
            values = [str(i + 1) for i in range(n_rows(meta, vdir))]
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


def content_cols(meta, vdir):
    """[(header, rows), …] for the table's content columns, in order."""
    out = []
    for i, ref in enumerate(meta["rows"]):
        if isinstance(ref, str) and ref != "*":
            out.append((meta["columns"][i], load(vdir, ref)["rows"]))
    return out


def roll_table(vdir, meta, die_choice):
    """Roll one table, per content column -> {header: raw_value}."""
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
    fmap = face_map(meta, vdir)
    vals = {}
    for header, rows in content_cols(meta, vdir):
        face = roll_face()
        idx = fmap.get(face)
        if idx is None:
            sys.exit(f"{meta['header'] or meta['dice']}: no row for face {face}")
        vals[header] = rows[idx]
    if not vals:
        # a single-column table (Next Scene): the column's own values are the
        # result — roll the die, take that row's value
        for i, ref in enumerate(meta["rows"]):
            if isinstance(ref, list):
                face = roll_face()
                idx = fmap.get(face)
                if idx is None:
                    sys.exit(f"{meta['header'] or meta['dice']}: no row for face {face}")
                vals[meta["columns"][i]] = ref[idx]
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("version_dir")
    ap.add_argument("tables", nargs="+", help="table id(s); one roll each")
    ap.add_argument("-c", type=int, default=1, help="number of rolls")
    ap.add_argument("--die", default="left",
                    choices=["left", "highest", "lowest"],
                    help="which die of the 2d6 roll indexes the row")
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

    for _ in range(args.c):
        merged = {}
        aliases = {}
        rolled_ids = []
        for i, meta in enumerate(metas):
            merged.update(roll_table(vdir, meta, args.die))
            aliases.update(meta.get("aliases", {}))
            rolled_ids.append(args.tables[i][:-5] if args.tables[i].endswith(".json")
                              else args.tables[i])

        template = metas[0].get("template", "")
        if template:
            for mk in dict.fromkeys(re.findall(r"\*\*([^*]+)\*\*", template)):
                if marker_value(mk, merged, aliases) is not None:
                    continue
                owning = [t for t in owners.get(mk, []) if t not in rolled_ids]
                if len(owning) == 1:
                    meta = all_metas[owning[0]]
                    merged.update(roll_table(vdir, meta, args.die))
                    aliases.update(meta.get("aliases", {}))
                    rolled_ids.append(owning[0])

            def fill(m):
                v = marker_value(m.group(1), merged, aliases)
                return m.group(0) if v is None else v.replace("*", "")
            # [**X**] is the placeholder syntax; **X** also fills.
            text = re.sub(r"\[\*\*([^*]+)\*\*\]", fill, template)
            text = re.sub(r"\*\*([^*]+)\*\*", fill, text)
        else:
            text = "  ".join(v.replace("*", "") for v in merged.values())
        # the template's markdown line breaks collapse to single spaces, so
        # each roll prints as one line
        print(re.sub(r"\s+", " ", text).strip())


if __name__ == "__main__":
    main()
