# Regenerate the Homebrewery brews from their table JSONs + templates.
#
# Each version builds every template/ x layout/ combination that exists:
#   homebrewery/template/<name>.md.j2  x  homebrewery/layout/<paper>.json
#       -> homebrewery/output/<name>_<paper>.md
#   (e.g. pocketfold x usletter -> output/pocketfold_usletter.md; a new
#    template/screen.md.j2 is picked up automatically)
#   a variant may also carry homebrewery/patches/<name>_<paper>.patch —
#   applied to the render before writing (paper-only tweaks); the build
#   fails if the patch no longer matches (regenerate with --no-patch)
#   make pop / make smoothie / make pregen — one version;  make — all
#   pregen/ is the pregenerated adventure: same mechanism, but its
#   sections.json runs scripts/roll.py per section, so every make writes
#   a NEW random pregen (non-deterministic by design)

PYTHON ?= python3

.PHONY: all pop smoothie pregen

all: pop smoothie pregen

pop:
	$(PYTHON) scripts/build_brew.py pop --version juice_pop --all

smoothie:
	$(PYTHON) scripts/build_brew.py smoothie --version juice_smoothie --all

pregen:
	$(PYTHON) scripts/build_pregen.py pregen --all
