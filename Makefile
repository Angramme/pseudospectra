PY = python
PIP = pip

all:

benchmark::
	$(PY) ./test/perf.py > ./test/perf.log

run::
	$(PY) app.py

installdeps::
	$(PIP) install -r requirements.txt  