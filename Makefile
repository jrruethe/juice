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
#   make pop / make smoothie — one version;  make — both

PYTHON ?= python3

.PHONY: all pop smoothie

all: pop smoothie

pop:
	$(PYTHON) scripts/build_brew.py pop --version juice_pop --all

smoothie:
	$(PYTHON) scripts/build_brew.py smoothie --version juice_smoothie --all
