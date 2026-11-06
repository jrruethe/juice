"""Custom roll for Pop!'s Immersion senses table.

One 1d10 roll does double duty, as the column headers encode:
  * the face picks the SENSE — which of the four sense columns applies
    (1-3 See, 4-6 Hear, 7-8 Smell, 9-0 Feel)
  * and the same face indexes that column's row — the Description
The template's [**Sense**] fills with the sense verb (see/hear/smell/
feel, from the column header) and [**Description**] with the cell; the
template's Location/Emotion/Reason markers then auto-roll
immersion_context through the standard machinery, so
`roll.py pop immersion_senses` prints the whole sentence alone.
"""

import json
import re
import sys


def sense_for(face, headers):
    """(sense, rows) of the column whose header range claims the face."""
    for header in headers:
        m = re.fullmatch(r"(\d+)-(\d+)<br>(\w+)", header)
        if not m:
            sys.exit(f"immersion_senses: header {header!r} is not a "
                     "'a-b<br>Sense' range")
        lo, hi, sense = int(m.group(1)), int(m.group(2)), m.group(3).lower()
        faces = range(lo, hi + 1) if lo <= hi else range(lo, 11)  # 9-0 wraps
        if face in faces:
            return sense, header
    sys.exit(f"immersion_senses: no sense column claims face {face}")


def roll(vdir, tid, meta, die):
    data = {}
    for i, ref in enumerate(meta["rows"]):
        if isinstance(ref, str) and ref != "*":
            p = vdir / "tables" / tid / "json" / ref
            data[meta["columns"][i]] = json.loads(p.read_text(encoding="utf-8"))["rows"]

    face = die.roll(10, "sense")  # all 10 sense faces in turn (deck mode)
    sense, header = sense_for(face, list(data))
    return [("Sense", sense), ("Description", data[header][face - 1])]
