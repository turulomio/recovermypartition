DESTDIR ?= /

PREFIXBIN=$(DESTDIR)/usr/bin
PREFIXSHARE=$(DESTDIR)/usr/share/recovermypartition 

install:
	echo "Translating" 
	pylupdate4 -noobsolete recovermypartition.pro
	lrelease recovermypartition.pro

	echo "Instalando en ${DESTDIR}"
	install -o root -d $(PREFIXBIN)
	install -o root -d $(PREFIXSHARE)
	install -m 755 -o root recovermypartition.py $(PREFIXBIN)/recovermypartition
	install -m 644 -o root GPL-3.txt  $(PREFIXSHARE)
	install -m 644 -o root i18n/*.qm $(PREFIXSHARE)

uninstall:
	rm $(PREFIXBIN)/recovermypartition
	rm -fr $(PREFIXSHARE)
