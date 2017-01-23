
PYTHON = python
TESTS  = test/koeterberg test/codepage test/singlepoint test/overflow
GPX2EPP = eppconvert/gpx2epp.py
EPPREAD = eppconvert/eppread.py

check:
	@status=0; \
	for test in $(TESTS); do \
		fail=0; \
		PYTHONPATH=. \
		$(PYTHON) $(GPX2EPP) -i $$test.gpx      -o $$test.test.epp && \
		$(PYTHON) -m hexdump    $$test.test.epp  > $$test.test.hex && \
		diff -u                 $$test.hex         $$test.test.hex && \
		PYTHONPATH=. \
		$(PYTHON) $(EPPREAD) -i $$test.test.epp -o $$test.test.txt && \
		diff -u                 $$test.txt         $$test.test.txt || \
		fail=1; \
		[ $$fail -eq 1 ] && echo "$$test: FAILED"; \
		[ $$fail -eq 0 ] && echo "$$test: OK";     \
		status=$$(( status + fail )); \
	done; \
	exit $$status;

testdata:
	@for test in $(TESTS); do \
		PYTHONPATH=. \
		$(PYTHON) $(GPX2EPP) -i $$test.gpx -o $$test.epp; \
        PYTHONPATH=. \
		$(PYTHON) $(EPPREAD) -i $$test.epp -o $$test.txt; \
		PYTHONPATH=. \
		$(PYTHON) -m hexdump    $$test.epp  > $$test.hex; \
	done
