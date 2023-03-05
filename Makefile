VENV           = ./venv
BIN            = $(VENV)/bin
VENV_PYTHON    = $(BIN)/python
SYSTEM_PYTHON  = $(or $(shell which python3), $(shell which python))
PYTHON         = $(or $(wildcard $(VENV_PYTHON)), $(SYSTEM_PYTHON))
MYPATH         = $(PWD)/lib:$(PATH)

init:
	rm -rf $(VENV)
	$(SYSTEM_PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -U setuptools wheel
	$(VENV_PYTHON) -m pip install -r requirements.txt
create:
	$(SYSTEM_PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -U setuptools wheel
install:
	$(SYSTEM_PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -U setuptools wheel
	$(VENV_PYTHON) -m pip install -r requirements.txt
build:
	$(SYSTEM_PYTHON) -m venv $(VENV)
	$(VENV)/bin/pyinstaller -F ./monitor.py 
	cp ./dist/monitor ./monitor-exector

clean:	
	rm -rf .tox *.egg-info dis venv __pycache__ logs build monitor.spec dist monitor-exector
.PHONY: clean
