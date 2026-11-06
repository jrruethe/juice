"""Custom roll for Pop!'s Immersion senses table (printed 5d10: one die
per column). The roller decks two levels:
  * the SENSES — see/hear/smell/feel in shuffled order, one of each
    before any sense repeats (the printed 1-3/4-6/7-8/9-0 face ranges
    are the table's way of assigning faces to senses)
  * and that sense column's 10 DESCRIPTION rows, decked per sense — so
    no (sense, description) pair repeats until that sense's 10 rows are
    all used
4 senses x 10 rows = 40 unique pairs, so the first repeat is roll 41.
The other three sense dice are never read. The template's [**Sense**]
fills with the sense verb and [**Description**] with the cell; the
template's Location/Emotion/Reason markers then auto-roll
immersion_context through the standard machinery, so
`roll.py pop immersion_senses` prints the whole sentence alone.
"""

import json
import re
import sys


def roll(vdir, tid, meta, die):
    data = {}
    sense_cols = []  # (sense, header) in printed column order
    for i, ref in enumerate(meta["rows"]):
        if isinstance(ref, str) and ref != "*":
            p = vdir / "tables" / tid / "json" / ref
            data[meta["columns"][i]] = json.loads(p.read_text(encoding="utf-8"))["rows"]
            m = re.fullmatch(r"(\d+)-(\d+)<br>(\w+)", meta["columns"][i])
            if not m:
                sys.exit(f"immersion_senses: header {meta['columns'][i]!r} "
                         f"is not a 'a-b<br>Sense' range")
            sense_cols.append((m.group(3).lower(), meta["columns"][i]))

    idx = die.roll(len(sense_cols), "sense")  # the 4-sense deck
    sense, header = sense_cols[idx - 1]
    row = die.roll(10, f"row-{sense}")  # that column's decked 10 rows
    return [("Sense", sense), ("Description", data[header][row - 1])]
