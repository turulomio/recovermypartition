DESTDIR ?= /

PREFIXBIN=$(DESTDIR)/usr/bin
PREFIXPO=$(DESTDIR)/usr/share/locale
PREFIXSHARE=$(DESTDIR)/usr/share/recovermypartition 


install:
	echo "Translating" 
	cd po; bash ./translate;cd ..
	echo "Instalando en ${DESTDIR}"
	install -o root -d $(PREFIXBIN)
	install -o root -d $(PREFIXPO)
	install -o root -d $(PREFIXPO)/en/LC_MESSAGES/
	install -o root -d $(PREFIXPO)/fr/LC_MESSAGES/
	install -o root -d $(PREFIXPO)/md/LC_MESSAGES/
	install -o root -d $(PREFIXPO)/ru/LC_MESSAGES/
	install -d $(PREFIXBIN)
	install -m 755 -o root recovermypartition.py $(PREFIXBIN)/recovermypartition
	install -m 644 -o root po/fr.mo $(PREFIXPO)/fr/LC_MESSAGES/recovermypartition.mo
	install -m 644 -o root po/en.mo $(PREFIXPO)/en/LC_MESSAGES/recovermypartition.mo
	install -m 644 -o root po/md.mo $(PREFIXPO)/md/LC_MESSAGES/recovermypartition.mo
	install -m 644 -o root po/ru.mo $(PREFIXPO)/ru/LC_MESSAGES/recovermypartition.mo
	install -m 644 -o root GPL-3.txt  $(PREFIXSHARE)

uninstall:
	rm $(PREFIXBIN)/recovermypartition
	rm $(PREFIXPO)/md/LC_MESSAGES/recovermypartition.mo
	rm $(PREFIXPO)/ru/LC_MESSAGES/recovermypartition.mo
	rm $(PREFIXPO)/fr/LC_MESSAGES/recovermypartition.mo
	rm $(PREFIXPO)/en/LC_MESSAGES/recovermypartition.mo
	rm -fr $(PREFIXSHARE)
