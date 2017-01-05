
PYTHON = python
TESTS  = test/koeterberg test/codepage test/singlepoint test/overflow

check:
	@status=0; \
	for test in $(TESTS); do \
		fail=0; \
		$(PYTHON) ./gpx2epp.py $$test.gpx      > $$test.test.epp && \
		hexdump -C             $$test.test.epp > $$test.test.hex && \
		diff -u                $$test.hex        $$test.test.hex && \
		$(PYTHON) ./eppread.py $$test.test.epp > $$test.test.txt && \
		diff -u                $$test.txt        $$test.test.txt || \
		fail=1; \
		[ $$fail -eq 1 ] && echo "$$test: FAILED"; \
		[ $$fail -eq 0 ] && echo "$$test: OK";     \
		status=$$(( status + fail )); \
	done; \
	exit $$status;

testdata:
	@for test in $(TESTS); do \
		$(PYTHON) ./gpx2epp.py $$test.gpx > $$test.epp; \
		$(PYTHON) ./eppread.py $$test.epp > $$test.txt; \
		hexdump -C             $$test.epp > $$test.hex; \
	done
