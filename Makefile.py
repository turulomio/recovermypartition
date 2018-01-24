#!/usr/bin/python3
import argparse
import datetime
import os
import sys
from subprocess import call
from colorama import Style, Fore
from multiprocessing import cpu_count
from libmangenerator import Man
from PyQt5.QtCore import QCoreApplication, QTranslator

def shell(*args):
    print(" ".join(args))
    call(args,shell=True)

def change_language( language):  
    """language es un string"""
    urls= ["i18n/recovermypartition_" + language + ".qm","/usr/share/recovermypartition/recovermypartition_" + language + ".qm"]
    for url in urls:
        if os.path.exists(url)==True:
            translator.load(url)
            QCoreApplication.installTranslator(translator)
            print(QCoreApplication.translate("recovermypartition","Language changed to {} using {}".format(language, url)))
            return
    if language!="en":
        print(Style.BRIGHT+ Fore.CYAN+ QCoreApplication.translate("recovermypartition","Language ({}) couldn't be loaded in {}. Using default (en).".format(language, urls)))
def makefile_dist_sources():
    shell("{} setup.py sdist".format(args.python))

def makefile_doc():
    shell("pylupdate5 -noobsolete -verbose recovermypartition.pro")
    shell("lrelease -qt5 recovermypartition.pro")
    for language in ["en", "fr", "ro", "ru", "es"]:
        mangenerator(language)

def makefile_install():
        shell("install -o root -d "+ prefixbin)
        shell("install -o root -d "+ prefixshare)
        shell("install -o root -d "+ prefixman+"/man1")
        shell("install -o root -d "+ prefixman+"/es/man1")
        shell("install -o root -d "+ prefixman+"/fr/man1")
        shell("install -o root -d "+ prefixman+"/ro/man1")
        shell("install -o root -d "+ prefixman+"/ru/man1")

        shell("install -m 755 -o root recovermypartition.py "+ prefixbin+"/recovermypartition")
        shell("install -m 644 -o root i18n/*.qm " + prefixshare)
        shell("install -m 644 -o root GPL-3.txt CHANGELOG.txt AUTHORS.txt INSTALL.txt "+ prefixshare)
        shell("install -m 644 -o root doc/recovermypartition.en.1 "+ prefixman+"/man1/recovermypartition.1")
        shell("install -m 644 -o root doc/recovermypartition.es.1 "+ prefixman+"/es/man1/recovermypartition.1")
        shell("install -m 644 -o root doc/recovermypartition.fr.1 "+ prefixman+"/fr/man1/recovermypartition.1")
        shell("install -m 644 -o root doc/recovermypartition.ro.1 "+ prefixman+"/ro/man1/recovermypartition.1")
        shell("install -m 644 -o root doc/recovermypartition.ru.1 "+ prefixman+"/ru/man1/recovermypartition.1")

def makefile_uninstall():
    shell("rm " + prefixbin + "/recovermypartition")
    shell("rm -Rf " + prefixshare)
    shell("rm -Rf {}/man1/recovermypartition.1".format(prefixman))
    shell("rm -Rf {}/es/man1/recovermypartition.1".format(prefixman))
    shell("rm -Rf {}/fr/man1/recovermypartition.1".format(prefixman))
    shell("rm -Rf {}/ro/man1/recovermypartition.1".format(prefixman))
    shell("rm -Rf {}/ru/man1/recovermypartition.1".format(prefixman))

def mangenerator(language):
    """
        Create man pages for parameter language
    """
    change_language(language)
    print("DESCRIPTION in {} is {}".format(language, QCoreApplication.translate("recovermypartition", "DESCRIPTION")))

    man=Man("doc/recovermypartition.{}".format(language))
    man.setMetadata("recovermypartition",  1,   datetime.date.today(), "Mariano Muñoz", QCoreApplication.translate("recovermypartition","Recover normal files and delete files from a partition."))
    man.setSynopsis("[--help] [--version] [--nofiles] [ --nodeleted| --partition| --output ]")

    man.header(QCoreApplication.translate("recovermypartition","DESCRIPTION"), 1)
    man.paragraph(QCoreApplication.translate("recovermypartition","This app has the following parameters."), 1)
    man.paragraph("--nofiles", 2, True)
    man.paragraph(QCoreApplication.translate("recovermypartition","Scans the net of the interface parameter and prints a list of the detected devices."), 3)
    man.paragraph(QCoreApplication.translate("recovermypartition","If a device is not known, it will be showed in red. Devices in green are trusted devices."), 3)
    man.paragraph("--nodeleted", 2, True)
    man.paragraph(QCoreApplication.translate("recovermypartition","Allows to add a known device from console."), 3)
    man.paragraph("--partition", 2, True)
    man.paragraph(QCoreApplication.translate("recovermypartition","Allows to remove a known device from console."), 3)
    man.paragraph("--output", 2, True)
    man.paragraph(QCoreApplication.translate("recovermypartition","Shows all known devices in database from console."), 3)
    man.save()
    ########################################################################

if __name__ == '__main__':
    start=datetime.datetime.now()
    parser=argparse.ArgumentParser(prog='Makefile.py', description='Makefile in python', epilog="Developed by Mariano Muñoz", formatter_class=argparse.RawTextHelpFormatter)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--doc', help="Generate docs and i18n",action="store_true",default=False)
    group.add_argument('--install', help="Directory to install app. / recomended",action="store", metavar="PATH", default=None)
    group.add_argument('--uninstall', help="Uninstall. / recomended",action="store", metavar="PATH", default=None)
    group.add_argument('--dist_sources', help="Make a sources tar", action="store_true",default=False)
    parser.add_argument('--python', help="Python path", action="store",default='/usr/bin/python3')
    args=parser.parse_args()

    app=QCoreApplication(sys.argv)#Needed for man generator
    app.setOrganizationName("recovermypartition")
    app.setOrganizationDomain("recovermypartit.sourceforge.net")
    app.setApplicationName("recovermypartition_makefile")
    translator=QTranslator(app)

    if args.install or args.uninstall:
        if args.install:
            destdir=args.install
        elif args.uninstall:
            destdir=args.uninstall

        prefixbin=destdir+"/usr/bin"
        prefixshare=destdir+"/usr/share/recovermypartition"
        prefixman=destdir+"/usr/share/man"

        if args.install:
            makefile_install()
        if args.uninstall:
            makefile_uninstall()

    elif args.doc==True:
        makefile_doc()
    elif args.dist_sources==True:
        makefile_dist_sources()

    print ("*** Process took {} using {} processors ***".format(datetime.datetime.now()-start , cpu_count()))

