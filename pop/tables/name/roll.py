"""Custom roll procedure for Pop!'s Name table (the pattern method).

roll.py delegates to this file because it sits next to the table's meta
(pop/tables/name/roll.py): the standard "one die per content column"
model can't express that the FIRST roll picks a row whose Template cell
dictates how the rest of the table is rolled.

The procedure:
  1. roll 1d20 -> a row; that row's Template cell is the pattern
     (e.g. `123-i`)
  2. the pattern's digits = which columns to roll, in order (1d20 each;
     digits may repeat — `111` rolls column 1 three times)
  3. a trailing - or + (only ever on the last digit, a 3): that column
     is rolled with 1d10 instead — - the top half (rows 1-10,
     face -> row), + the bottom half (rows 11-20, face -> row 10+f)
  4. a trailing o/a/i (combinable: `23-o`): append that letter
  5. column 1, rows 1-5 carry a parenthesized consonant — `(f)a`:
     the vowel only when the chunk STARTS the name, consonant included
     when it sits mid/end
  6. concatenate without spaces; capitalize the first letter
"""

import json
import re
import sys


def parse_pattern(code):
    """'123-i' -> (['1', '2', '3'], '-', 'i'); '12o' -> (['1', '2'], '', 'o')."""
    m = re.fullmatch(r"([123]+)([-+]?)\s*([oai]?)", code.strip().strip("`").strip())
    if not m:
        sys.exit(f"Name: unrecognized pattern {code!r}")
    return list(m.group(1)), m.group(2), m.group(3)


def assemble(chunks, suffix):
    """chunks = [(column, value), …] in roll order -> the final name
    (a column-1 chunk's parenthesized consonant is dropped only when
    the chunk starts the name)."""
    out = []
    for k, (_, c) in enumerate(chunks):
        pm = re.fullmatch(r"\((.)\)(.*)", c)
        if pm:
            c = pm.group(2) if k == 0 else pm.group(1) + pm.group(2)
        out.append(c)
    name = "".join(out) + suffix
    return name.capitalize() if name else ""


def roll(vdir, tid, meta, die):
    data = {}
    for i, ref in enumerate(meta["rows"]):
        if isinstance(ref, str) and ref != "*":
            p = vdir / "tables" / tid / "json" / ref
            data[meta["columns"][i]] = json.loads(p.read_text(encoding="utf-8"))["rows"]

    row = die.roll(20, "row")  # each of the 20 patterns in turn (deck mode)
    code = data["Template"][row - 1]
    digits, half, suffix = parse_pattern(code)
    if half and digits[-1] != "3":
        sys.exit(f"Name: pattern {code!r} — +/- applies only to a 3")

    chunks = []
    for k, d in enumerate(digits):
        if half and d == "3" and k == len(digits) - 1:
            face = die.roll(10, f"half{d}")
            r = face if half == "-" else 10 + face
        else:
            r = die.roll(20, f"col{d}")
        chunks.append((d, data[d][r - 1]))

    name = assemble(chunks, suffix)
    if not name:
        sys.exit(f"Name: pattern {code!r} produced no name")
    return [(meta["header"] or "", name)]
