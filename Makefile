VENV := .venv

ifeq ($(OS), Windows_NT)
	PYTHON := $(VENV)/Scripts/python
	PIP := $(VENV)/Scripts/pip
	ACTIVATE := $(VENV)\\Scripts\\activate.bat
else
	PYTHON := $(VENV)/bin/python
	PIP := $(VENV)/bin/pip
	ACTIVATE := source $(VENV)/bin/activate
endif

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
	@cmd /k "$(ACTIVATE)"
else
	@bash -c '$(ACTIVATE) && exec $$SHELL'
endif

run:
	$(PYTHON) -m $(MAIN_PATH)

clean:
ifeq ($(OS), Windows_NT)
	rmdir /S /Q $(VENV)
else
	rm -rf $(VENV)
endif
