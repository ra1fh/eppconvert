
PYTHON = python
TESTS  = test/koeterberg test/codepage test/singlepoint test/overflow
GPX2EPP = eppconvert/gpx2epp.py
EPPREAD = eppconvert/eppread.py

check:
	@status=0; \
	for test in $(TESTS); do \
		fail=0; \
		$(PYTHON) $(GPX2EPP) $$test.gpx      > $$test.test.epp && \
		hexdump -C           $$test.test.epp > $$test.test.hex && \
		diff -u              $$test.hex        $$test.test.hex && \
		$(PYTHON) $(EPPREAD) $$test.test.epp > $$test.test.txt && \
		diff -u              $$test.txt        $$test.test.txt || \
		fail=1; \
		[ $$fail -eq 1 ] && echo "$$test: FAILED"; \
		[ $$fail -eq 0 ] && echo "$$test: OK";     \
		status=$$(( status + fail )); \
	done; \
	exit $$status;

testdata:
	@for test in $(TESTS); do \
		$(PYTHON) $(GPX2EPP) $$test.gpx > $$test.epp; \
		$(PYTHON) $(EPPREAD) $$test.epp > $$test.txt; \
		hexdump -C           $$test.epp > $$test.hex; \
	done
