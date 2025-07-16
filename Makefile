VENV := .venv
PYTHON := $(VENV)/Scripts/python
PIP := $(VENV)/Scripts/pip

MAIN_PATH := main

.PHONY: all venv install activate clean

all: venv install

venv:
	python -m venv $(VENV)

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

activate:
ifeq ($(OS), Windows_NT)
	@cmd /k ".venv\\Scripts\\activate.bat"
else
	source .venv/bin/activate
endif

run:
	$(PYTHON) -m $(MAIN_PATH)

clean:
ifeq ($(OS), Windows_NT)
	rmdir /S /Q $(VENV)
else
	rm -rf $(VENV)
endif
