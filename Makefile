# randrn.py Makefile
# 

all: randrn del
# readme

# Create randrn executable
randrn:
	pyinstaller randrn.py -F
	mv dist/randrn .

# Remove files created by pyinstaller
del:
	rm -rf ./dist/ ./build/ ./*.spec ./*.pyc ./*.log randrn.spec dist/

# Clear pyinstall cache and delete file
clean:
	pyinstaller --clean randrn.py
	rm -rf ./dist/ ./build/ ./*.spec ./*.pyc ./*.log randrn.spec dist/

PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin

install:
	mkdir -p $(DESTDIR)$(BINDIR)
	install -m755 randrn $(DESTDIR)$(BINDIR)/eb
