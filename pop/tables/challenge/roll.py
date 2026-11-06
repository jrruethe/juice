"""Custom roll for Pop!'s Creating a Challenge table.

The printed table's two # columns say the mechanic: one 1d20 picks the
Skill — faces 1-10 index the Physical Skill column (Medicine..Athletics),
faces 11-20 index the Mental Skill column (Tool..Insight, face − 10).
The standard model rolls each column on its own die, so the single
[**Skill**] marker could never be filled from it; the hook rolls the
1d20 and returns the chosen skill under the marker's name ("Skill").
Obstacle/Action/Target roll the usual way (one die per column), and
[**Consequence**] still auto-rolls the consequence table through the
standard machinery.
"""

import json
import random
import sys


def roll(vdir, tid, meta, die_choice):
    cols = {}
    for i, ref in enumerate(meta["rows"]):
        if isinstance(ref, str) and ref != "*":
            p = vdir / "tables" / tid / "json" / ref
            cols[meta["columns"][i]] = json.loads(p.read_text(encoding="utf-8"))["rows"]

    for name in ("Physical Skill", "Mental Skill"):
        if len(cols[name]) != 10:
            sys.exit(f"challenge: {name} must have 10 rows, has {len(cols[name])}")

    face = random.randint(1, 20)
    if face <= 10:
        skill = cols["Physical Skill"][face - 1]
    else:
        skill = cols["Mental Skill"][face - 11]

    vals = [("Skill", skill)]
    for name in ("Obstacle", "Action", "Target"):
        vals.append((name, random.choice(cols[name])))
    return vals
