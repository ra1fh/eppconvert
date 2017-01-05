
PYTHON = python2.7
TESTS  = test/koeterberg test/codepage test/singlepoint

check:
	@for test in $(TESTS); do \
		$(PYTHON) gpx2epp.py $$test.gpx      > $$test.test.epp && \
		hexdump -C           $$test.test.epp > $$test.test.hex && \
		diff -u              $$test.hex        $$test.test.hex && \
		$(PYTHON) eppread.py $$test.test.epp > $$test.test.txt && \
		diff -u              $$test.txt        $$test.test.txt && \
		echo "$$test: OK" || echo "$$test: FAILED"; \
	done

testdata:
	@for test in $(TESTS); do \
		$(PYTHON) gpx2epp.py $$test.gpx > $$test.epp; \
		$(PYTHON) eppread.py $$test.epp > $$test.txt; \
		hexdump -C           $$test.epp > $$test.hex; \
	done
