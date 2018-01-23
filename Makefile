DESTDIR ?= /usr

PREFIXBIN=$(DESTDIR)/bin
PREFIXSHARE=$(DESTDIR)/share/recovermypartition 

compile:
	echo "Translating" 
	pylupdate5 -noobsolete recovermypartition.pro
	lrelease recovermypartition.pro

install:
	echo "Instalando en $(DESTDIR)"
	install -o root -d $(PREFIXBIN)
	install -o root -d $(PREFIXSHARE)
	install -m 755 -o root recovermypartition.py $(PREFIXBIN)/recovermypartition
	install -m 644 -o root GPL-3.txt  $(PREFIXSHARE)
	install -m 644 -o root i18n/*.qm $(PREFIXSHARE)

uninstall:
	rm $(PREFIXBIN)/recovermypartition
	rm -fr $(PREFIXSHARE)
