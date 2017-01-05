
PYTHON=python2.7
TESTDATA=test/koeterberg
CODEPAGE=test/codepage

check:
	$(PYTHON) gpx2epp.py $(TESTDATA).gpx      > $(TESTDATA).test.epp
	hexdump -C           $(TESTDATA).test.epp > $(TESTDATA).test.hex
	diff -u              $(TESTDATA).hex        $(TESTDATA).test.hex
	$(PYTHON) eppread.py $(TESTDATA).test.epp > $(TESTDATA).test.txt
	diff -u              $(TESTDATA).txt        $(TESTDATA).test.txt
	$(PYTHON) eppread.py $(CODEPAGE).epp      > $(CODEPAGE).test.txt
	hexdump -C           $(CODEPAGE).test.txt > $(CODEPAGE).test.hex
	diff -u              $(CODEPAGE).hex        $(CODEPAGE).test.hex
	diff -u              $(CODEPAGE).txt        $(CODEPAGE).test.txt
	@echo "make check: OK"

testdata:
	$(PYTHON) gpx2epp.py $(TESTDATA).gpx > $(TESTDATA).epp
	$(PYTHON) eppread.py $(TESTDATA).epp > $(TESTDATA).txt
	hexdump -C           $(TESTDATA).epp > $(TESTDATA).hex
	$(PYTHON) eppread.py $(CODEPAGE).epp > $(CODEPAGE).txt
	hexdump -C           $(CODEPAGE).txt > $(CODEPAGE).hex
