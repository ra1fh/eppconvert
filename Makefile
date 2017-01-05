
PYTHON=python2.7
TESTDATA=test/koeterberg
CODEPAGE=test/codepage

check:
	$(PYTHON) gpx2epp.py $(TESTDATA).gpx      > $(TESTDATA).test.epp
	hexdump -C           $(TESTDATA).test.epp > $(TESTDATA).test.hex
	diff -u              $(TESTDATA).hex        $(TESTDATA).test.hex
	$(PYTHON) eppread.py $(TESTDATA).test.epp > $(TESTDATA).test.txt
	diff -u              $(TESTDATA).txt        $(TESTDATA).test.txt
	$(PYTHON) gpx2epp.py $(CODEPAGE).gpx      > $(CODEPAGE).test.epp
	hexdump -C           $(CODEPAGE).test.epp > $(CODEPAGE).test.hex
	diff -u              $(CODEPAGE).hex        $(CODEPAGE).test.hex
	$(PYTHON) eppread.py $(CODEPAGE).test.epp > $(CODEPAGE).test.txt
	diff -u              $(CODEPAGE).txt        $(CODEPAGE).test.txt
	@echo "make check: OK"

testdata:
	$(PYTHON) gpx2epp.py $(TESTDATA).gpx > $(TESTDATA).epp
	$(PYTHON) eppread.py $(TESTDATA).epp > $(TESTDATA).txt
	hexdump -C           $(TESTDATA).epp > $(TESTDATA).hex
	$(PYTHON) gpx2epp.py $(CODEPAGE).gpx > $(CODEPAGE).epp
	$(PYTHON) eppread.py $(CODEPAGE).epp > $(CODEPAGE).txt
	hexdump -C           $(CODEPAGE).epp > $(CODEPAGE).hex
