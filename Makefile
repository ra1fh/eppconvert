
PYTHON=python2.7
TESTDATA=test/koeterberg

check:
	$(PYTHON) gpx2epp.py $(TESTDATA).gpx      > $(TESTDATA).test.epp
	hexdump -C           $(TESTDATA).test.epp > $(TESTDATA).test.hex
	diff -u              $(TESTDATA).hex        $(TESTDATA).test.hex
	$(PYTHON) eppread.py $(TESTDATA).test.epp > $(TESTDATA).test.txt
	diff -u              $(TESTDATA).txt        $(TESTDATA).test.txt
	@echo "make check: OK"

testdata:
	$(PYTHON) gpx2epp.py $(TESTDATA).gpx > $(TESTDATA).epp
	$(PYTHON) eppread.py $(TESTDATA).epp > $(TESTDATA).txt
	hexdump -C           $(TESTDATA).epp > $(TESTDATA).hex
