# Regenerate the Homebrewery brews from their table JSONs + templates.
#   make pop       -> pop/homebrewery/pocketfold.md
#   make smoothie  -> smoothie/homebrewery/pocketfold.md
#   make           -> both

PYTHON ?= python3

.PHONY: all pop smoothie

all: pop smoothie

pop:
	$(PYTHON) scripts/build_brew.py pop --version juice_pop

smoothie:
	$(PYTHON) scripts/build_brew.py smoothie --version juice_smoothie
