# ==============================
# Configuration
# ==============================

PYTHON := python3
VENV := .venv
VENV_PYTHON := $(VENV)/bin/python
VENV_PIP := $(VENV)/bin/pip
SRC := parse_config_file.py visualize_colors.py visualize_display.py visualize_maze.py write_output.py

APP := a_maze_ing.py

MYPY_FLAGS := --warn-return-any \
              --warn-unused-ignores \
              --ignore-missing-imports \
              --disallow-untyped-defs \
              --check-untyped-defs

# ==============================
# Virtual Environment
# ==============================

$(VENV):
	$(PYTHON) -m venv $(VENV)
	$(VENV_PIP) install --upgrade pip

# ==============================
# Main Commands
# ==============================

run: install
	$(VENV_PYTHON) $(APP) $(ARGS)

debug: install
	$(VENV_PYTHON) -m pdb $(APP)

install: $(VENV)
	$(VENV_PIP) install dist/mazegen-1.0.0-py3-none-any.whl
	$(VENV_PIP) install mypy flake8

lint: install
	$(VENV)/bin/flake8 $(SRC)
	$(VENV)/bin/mypy $(MYPY_FLAGS) $(SRC)

lint-strict: install
	$(VENV)/bin/flake8 $(SRC)
	$(VENV)/bin/mypy $(MYPY_FLAGS) --strict $(SRC)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

fclean: clean
		rm -rf $(VENV)

all: lint run

.PHONY: install run debug clean fclean lint lint-strict all
