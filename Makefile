#
# Makefile to build standalone `cmongo2sql` Unix-like executable program.
#

FREEZE = cxfreeze
SOURCE = cmongo2sql.py
TARGET = cmongo2sql

make:
	$(FREEZE) $(SOURCE) --target-dir dist
	
dependencies:
	pip -q install cx_Freeze
	
test:
	sudo mv dist/${TARGET} /usr/bin 
	$(TARGET) -l -f sample.json -d dummydb

clean:
	rm -r -f dist
	rm -r -f $(TARGET)
