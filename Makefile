PY = python
PIP = pip

all:

benchmark::
	$(PY) ./test/perf.py

run::
	$(PY) app.py

installdeps::
	$(PIP) install -r requirements.txt  