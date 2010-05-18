DESTDIR ?= /

PREFIXBIN=$(DESTDIR)/usr/bin
PREFIXPO=$(DESTDIR)/usr/share/locale
PREFIXSHARE=$(DESTDIR)/usr/share/recovermypartition 

install: 
	echo "Instalando en ${DESTDIR}"
	install -o root -d $(PREFIXBIN)
	install -o root -d $(PREFIXPO)
	install -d $(PREFIXBIN)
	install -m 755 -o root recovermypartition.py $(PREFIXBIN)/recovermypartition
	install -m 644 -o root po/es.mo $(PREFIXPO)/es/LC_MESSAGES/recovermypartition.mo
	install -m 644 -o root po/en.mo $(PREFIXPO)/en/LC_MESSAGES/recovermypartition.mo
	install -m 644 -o root GPL-3.txt  $(PREFIXSHARE)

uninstall:
	rm $(PREFIXBIN)/recovermypartition
	rm $(PREFIXPO)/es/LC_MESSAGES/recovermypartition.mo
	rm $(PREFIXPO)/en/LC_MESSAGES/recovermypartition.mo
	rm -fr $(PREFIXSHARE)
