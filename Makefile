PYTHON = python3
SCRIPT = a_maze_ing.py
CONFIG = config.txt

.PHONY: install run debug clean lint

install:
	pip install flake8 mypy

run:
	$(PYTHON) $(SCRIPT) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(SCRIPT) $(CONFIG)

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
