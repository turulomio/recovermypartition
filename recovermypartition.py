#!/usr/bin/python3
import os, sys, time, math,  calendar,  datetime, subprocess
from PyQt5.QtCore import *
from optparse import OptionParser

version="0.3"

class Color:
    esc_seq = "\x1b["
    codes={}
    codes["reset"]     = esc_seq + "39;49;00m"
    codes["bold"]      = esc_seq + "01m"
    codes["faint"]     = esc_seq + "02m"
    codes["standout"]  = esc_seq + "03m"
    codes["underline"] = esc_seq + "04m"
    codes["blink"]     = esc_seq + "05m"
    codes["overline"]  = esc_seq + "06m"  # Who made this up? Seriously.
    codes["teal"]      = esc_seq + "36m"
    codes["turquoise"] = esc_seq + "36;01m"
    codes["fuchsia"]   = esc_seq + "35;01m"
    codes["purple"]    = esc_seq + "35m"
    codes["blue"]      = esc_seq + "34;01m"
    codes["darkblue"]  = esc_seq + "34m"
    codes["green"]     = esc_seq + "32;01m"
    codes["darkgreen"] = esc_seq + "32m"
    codes["yellow"]    = esc_seq + "33;01m"
    codes["brown"]     = esc_seq + "33m"
    codes["red"]       = esc_seq + "31;01m"
    codes["darkred"]   = esc_seq + "31m"
    
    def resetColor(self, text):
        return self.codes["reset"] + text
    def ctext(self, color,text):
        return self.codes[ctext]+text+self.codes["reset"]
    def bold(self, text):
        return self.codes["bold"]+text+self.codes["reset"]
    def white(self, text):
        return self.bold(text)
    def teal(self, text):
        return self.codes["teal"]+text+self.codes["reset"]
    def turquoise(self, text):
        return self.codes["turquoise"]+text+self.codes["reset"]
    def darkteal(self, text):
        return turquoise(text)
    def fuchsia(self, text):
        return self.codes["fuchsia"]+text+self.codes["reset"]
    def purple(self, text):
        return self.codes["purple"]+text+self.codes["reset"]
    def blue(self, text):
        return self.codes["blue"]+text+self.codes["reset"]
    def darkblue(self, text):
        return self.codes["darkblue"]+text+self.codes["reset"]
    def green(self, text):
        return self.codes["green"]+text+self.codes["reset"]
    def darkgreen(self, text):
        return self.codes["darkgreen"]+text+self.codes["reset"]
    def yellow(self, text):
        return self.codes["yellow"]+text+self.codes["reset"]
    def brown(self, text):
        return self.codes["brown"]+text+self.codes["reset"]
    def darkyellow(self, text):
        return brown(text)
    def red(self, text):
        return self.codes["red"]+text+self.codes["reset"]
    def darkred(self, text):
        return self.codes["darkred"]+text+self.codes["reset"]

def contador(puntpasosdesdecero, totalpasos, tiempo_inicio_contador_parcial):
    """
        Función que devuelve segundos estimados
    """        
    tiempoactual=time.time()
    resultado=(totalpasos-puntpasosdesdecero)*(tiempoactual-tiempo_inicio_contador_parcial)/puntpasosdesdecero
    return resultado



def segundos2fechastring(segundos):
    dias=int(segundos/(24*60*60))
    segundosquedan=math.fmod(segundos,24*60*60)
    horas=int(segundosquedan/(60*60))
    segundosquedan=math.fmod(segundosquedan,60*60)
    minutos=int(segundosquedan/60)
    segundosquedan=math.fmod(segundosquedan,60)
    segundos=int(segundosquedan)
    return "{0}d {1}h {2}m {3}s".format(dias,  horas,  minutos, segundos)

def string2time(cadena):
    try:
        t= time.strptime(cadena,"%Y-%m-%d %H:%M:%S (%Z)")
    except:
        return None
    return t 

def time2string(t):
    """Creo que no hace bien el zone"""
    if t==None:
        return "None"
    return time.strftime("%Y-%m-%d %H:%M:%S %z (%Z)", t)

#~def dt(date, hour, zone):
#    """Función que devuleve un datetime con zone info"""    
#    z=pytz.timezone(zone)
#    a=datetime.datetime(date.year,  date.month,  date.day,  hour.hour,  hour.minute,  hour.second, hour.microsecond)
#a=z.localize(a)
#    return a

class SetFiles:
    def __init__(self):
        self.countinode0=0
        pass

class LogFile:
    def __init__(self, path):
        self.path=path
        self.file=open(path, "w")
    def __del__(self):
        #print(QCoreApplication.translate("recovermypartition","Logfile {0} closed").format(self.path))
        self.file.close()
        
    def append(self, string):
        self.file.write(string)
        

class File:
    def __init__(self,l):
        """l es una linea fls"""    
        self.flsline=l
        self.errors=[] #Van acumulando errores

        self.inode=self.getInode()
        self.type=self.flsline[0]
        self.type_metadata=self.flsline[2]
        self.name=self.flsline.split(chr(9))[1]
        self.mod_time=string2time(self.flsline.split(chr(9))[2])
        self.acc_time=string2time(self.flsline.split(chr(9))[3])
        self.chg_time=string2time(self.flsline.split(chr(9))[4])
        self.cre_time=string2time(self.flsline.split(chr(9))[5])
        self.size=int(self.flsline.split(chr(9))[6])
        self.uid=int(self.flsline.split(chr(9))[7])
        self.gid=int(self.flsline.split(chr(9))[8])
        
        self.reallocated=None#Se rellena con isDeleted
        self.deleted=self.isDeleted()

    def isDirectory(self):
        if self.type=="d" or self.type_metadata=="d":
            return True
        return False

    def isDeleted(self):
        self.reallocated=False
        if self.flsline.split(chr(9))[0].find("(realloc)")>-1:
            self.reallocated=True
            return True        
        elif self.flsline.split(chr(9))[0].find("*")>-1:
            return True
        if self.name.find("$OrphanFiles")>-1:
            return True
        return False

      
    def getInode(self):
        if self.flsline.split(chr(9))[0].find("(realloc)")>-1:
            return self.flsline.split(chr(9))[0].split(" ")[2][:-10]
        elif self.flsline.split(chr(9))[0].find("*")>-1:
            return self.flsline.split(chr(9))[0].split(" ")[2][:-1]
        else:
            return self.flsline.split(chr(9))[0].split(" ")[1][:-1]
        
    def path(self):
        """Devuelve el path relativo donde se grabará el fichero"""
        if self.type=="v":
            return QCoreApplication.translate("recovermypartition","Virtual")+"/"+self.name
        elif self.deleted==True:
            return QCoreApplication.translate("recovermypartition","Deleted")+"/"+self.name
        return QCoreApplication.translate("recovermypartition","Files") +"/"+ self.name
      
    def isCriticalError(self):
        "Devuelve si hay un error crítico, es decir menor que 20"
        if len(self.errors)==0:
            return False
            
        for e in self.errors:
            if e<20:
                return True
        return False
      
    def save(self):
        def path2sleuthkit(cadena):
            """Que sustituya por _ cuando se saca un listado sleuthkit y
            nosotros generamos el sistema de ficheros.
            """
            todelete=('?','!','¡','"', "'")
            for caracter in todelete:
                cadena=cadena.replace(caracter,'_')
            return cadena        
        if self.inode==0:
            self.errors.append(1)
            
        fullpath=options.output+"/" +path2sleuthkit(self.path())
        
        if self.isDirectory()==True:
            try:
                os.makedirs(fullpath)
            except:
                pass     #No se puede controlar el error
        else:
            try:
                os.makedirs(os.path.dirname(fullpath))
            except:
                pass
            try:
                if self.deleted==True:
                    p=subprocess.check_output("icat -r '{0}' {1} > '{2}'".format(options.partition,self.inode, fullpath),shell=True)
                else:
                    p=subprocess.check_output("icat '{0}' {1} > '{2}'".format(options.partition,self.inode, fullpath),shell=True)
                if len(p)>0:
                    self.errors.append(11)
            except:
                self.errors.append(10) 
            
        try:
            accesed=calendar.timegm(self.acc_time)
        except:
            self.errors.append(20) 
            accesed=0

        try:
            modified=calendar.timegm(self.mod_time)
        except:
            modified=0
            self.errors.append(25)
            
        try:
            os.utime(fullpath,(accesed,modified))
        except:
            self.errors.append(30)
        
        
        self.parseErrors()
        
    def __repr__(self):
        errores=""
        if 1 in self.errors:
            errores=errores +QCoreApplication.translate("recovermypartition","I-node is 0") + ", "
        if 10 in self.errors:
            errores=errores +QCoreApplication.translate("recovermypartition","I couldn't create file") + ", "
        if 11 in self.errors:
            errores=errores +QCoreApplication.translate("recovermypartition","I couldn't create file. Icat error string  greater than 0") + ", "
        if 20 in self.errors:
            errores=errores +QCoreApplication.translate("recovermypartition","Not recovered access time") + ", "
        if 25 in self.errors:
            errores=errores +QCoreApplication.translate("recovermypartition","Not recovered modification time") + ", "
        if 30 in self.errors:
            errores=errores +QCoreApplication.translate("recovermypartition","Access and modification time couldn't be rebuild") + ", "
        return """
Name: """ + self.name +"""
i-node: """ + self.inode +"""
Deleted: """ + str(self.deleted) + """
Reallocated: """ + str(self.reallocated) + """
Type: """+ self.type+"/"+self.type_metadata+"""
Access time: """+ time2string(self.acc_time)+"""
Modification time: """+time2string(self.mod_time)+"""
Change time: """+time2string(self.chg_time)+"""
Creation time: """+ time2string(self.cre_time)+"""
Size: """+ str(self.size) + """
Errores: """ + errores[:-2] + """
FLS: """ + self.flsline 
      
      
    def parseErrors(self):
        #################################
        if self.name=="$OrphanFiles" and self.type=="d" and self.type_metadata=="d":
            self.errors.remove(20)
            self.errors.remove(25)

class Sleuthkit:          
    def blkls(self, path_evidencia ,  path_salida_dd):
        """
            Funcion que genera un fichero texto partiendo de los clusters
            sin asignar de una determinada imagen
            
            Devuelve un booleano dependiendo del exito en la finalizacion de 
            la operacion.
            
            El fichero se genera en 
            directoriotemporaltrabajo+)'/csa/particion.' + idparticion + '
        """
        try:
            os.makedirs(path)
        except:
            pass
        comando='blkls -s %s  > %s'%(path_evidencia, path_salida_dd)
        os.popen(comando)


######################################################################
######################################################################


if __name__ == "__main__":
    a=QCoreApplication(sys.argv)
    language=QLocale().name().split("_")[0]
    translator=QTranslator()
    translator.load("/usr/share/recovermypartition/recovermypartition_" + language + ".qm")
    a.installTranslator(translator);    
        
    parser = OptionParser(version=version,  description=QCoreApplication.translate("recovermypartition","Recover files and deleted files from a device or image"))
    parser.add_option( "--no-files", action="store_true", default=False, dest="nofiles", help=QCoreApplication.translate("recovermypartition","Don't recover normal files"))
    parser.add_option( "--no-deleted", action="store_true", default=False, dest="nodeleted", help=QCoreApplication.translate("recovermypartition","Don't recover deleted files"))
    parser.add_option( "--partition", action="store", dest="partition", help=QCoreApplication.translate("recovermypartition","Device or imagen to analyze"))
    output="recovermypartition_{0}/".format(str(datetime.datetime.now())[:19]).replace(" ","_").replace(":","").replace("-","")
    parser.add_option( "--output", action="store",  dest="output", default=output,  help=QCoreApplication.translate("recovermypartition","Output directory"))

    (options, args) = parser.parse_args()
        
    if options.partition==None:
        parser.error (QCoreApplication.translate("recovermypartition","You need to pass --partition parameter"))
        sys.exit(190)
        
    try:
        os.makedirs(options.output)
    except OSError:
        parser.error (QCoreApplication.translate("recovermypartition","Output directory creating problem. Check it doesn't exist"))
        sys.exit()
        
    error=LogFile(options.output+"recovermypartition.error")
    log=LogFile(options.output + "/recovermypartition.log")
    sleuthkit=LogFile(options.output+"/recovermypartition.sleuthkit")
    tiempo_contador_parcial=time.time()
    log.append(QCoreApplication.translate("recovermypartition","Partition: {0}\n".format(options.partition)))
    log.append(QCoreApplication.translate("recovermypartition","Recovery started: {0}\n".format(str(datetime.datetime.now()))))


    try:
        if options.nofiles==False and options.nodeleted==False:
            print (Color().red(QCoreApplication.translate("recovermypartition","Generating all files list, including deleted")))
            #fls=os.popen("fls -prl " + options.partition ).readlines()
            fls=subprocess.check_output(["fls", "-prl", options.partition], stderr=subprocess.STDOUT).split(b"\n")
        elif options.nofiles==True and options.nodeleted==False:
            print (Color().red(QCoreApplication.translate("recovermypartition","Generating deleted files list")))
            fls=os.popen("fls -prdl " + options.partition ).readlines()
        elif options.nofiles==False and options.nodeleted==True:
            print (Color().red(QCoreApplication.translate("recovermypartition","Generating normal files list")))
            fls=os.popen("fls -prul " + options.partition ).readlines()
    except:
        print (Color().fuchsia(QCoreApplication.translate("recovermypartition", "I couldn't read the partition")))
        sys.exit(250)

    #Quita lineas en blanco se genera con check_output
    try:
        fls.remove(b"")
    except:
        pass

    ##CREA FICHERO SLEUTHKIT
    for line in fls:
        sleuthkit.append(line.decode('UTF-8')+"\n")
    del sleuthkit

    ##ARRANCA    
    print (Color().fuchsia(QCoreApplication.translate( "recovermypartition","Partition or image to analyze: ")) + options.partition)
    print (Color().fuchsia(QCoreApplication.translate("recovermypartition","Output directory")+":          ") + options.output)

    num_recuperados=0
    num_total_ficheros=len(fls)
    puntnumerototalficheros=num_total_ficheros

    print (Color().green( QCoreApplication.translate("recovermypartition","+ Recovering {0} files from partition. Process could take long time.").format(num_total_ficheros  )))
    for linea in fls:
        linea=linea.decode('UTF-8')
        f=File(linea)
        f.save()
        if f.isCriticalError()==False:
            num_recuperados=num_recuperados+1
        else:
            print (f)
            error.append(linea)
        puntnumerototalficheros=puntnumerototalficheros-1
        cadena= QCoreApplication.translate("recovermypartition","  - Left {0} of {1}. [ Recovered: {2} ]. ETA: {3}                     ").format(puntnumerototalficheros, num_total_ficheros,  Color().green(str(num_recuperados)), Color().yellow(segundos2fechastring(contador(num_total_ficheros-puntnumerototalficheros,num_total_ficheros,tiempo_contador_parcial))))
            
        sys.stdout.write("\b"*(len(cadena)+5)) 
        sys.stdout.write (cadena)   
        sys.stdout.flush()  

    print("")
    ##CREA FICHERO LOG
    log.append(QCoreApplication.translate("recovermypartition","Recovery ended: {0}\n").format(str(datetime.datetime.now())))
    log.append(QCoreApplication.translate("recovermypartition","Analyzed files number: {0}\n").format(str(len(fls))))
    log.append(QCoreApplication.translate("recovermypartition","Recovery files number: {0}\n").format(str(num_recuperados)))
    del log
    del error

    ##MUESTRA TIEMPO DEL PROCESO
    print (Color().green("+ "+QCoreApplication.translate("recovermypartition","Recovery took: {0}").format(segundos2fechastring(time.time()-tiempo_contador_parcial) )))
