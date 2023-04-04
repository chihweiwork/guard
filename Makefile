VENV           = ./venv
BIN            = $(VENV)/bin
VENV_PYTHON    = $(BIN)/python
SYSTEM_PYTHON  = $(or $(shell which python3), $(shell which python))
PYTHON         = $(or $(wildcard $(VENV_PYTHON)), $(SYSTEM_PYTHON))
MYPATH         = $(PWD)/lib:$(PATH)

venv:
	$(SYSTEM_PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -U setuptools wheel
install:
	$(VENV_PYTHON) -m pip install -r requirements.txt
build:
	$(SYSTEM_PYTHON) -m venv $(VENV)
	$(VENV)/bin/pyinstaller -F ./monitor.py 
	cp ./dist/monitor ./monitor-exector

clean-venv:
	rm -rf venv
clean-build:
	rm -rf dist .tox *.egg-info 
clean-env:
	rm -rf __pycache__ logs

build: venv install
clean: clean-venv clean-build clean-env
.PHONY: clean venv install build
