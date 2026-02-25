# ==============================
# Configuration
# ==============================

PYTHON := python3
PIP := pip3
APP := a_maze_ing.py

MYPY_FLAGS := --warn-return-any \
              --warn-unused-ignores \
              --ignore-missing-imports \
              --disallow-untyped-defs \
              --check-untyped-defs

# ==============================
# Main Commands
# ==============================

run:
	$(PYTHON) $(APP) $(ARGS)

debug:
	$(PYTHON) -m pdb $(APP)

install:
	$(PIP) install mypy flake8

lint:
	flake8 .
	mypy . $(MYPY_FLAGS)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

all: lint run
