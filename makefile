PYTHON := python3
SRC := main.py

.PHONY: run clean

run:
	$(PYTHON) $(SRC)

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +