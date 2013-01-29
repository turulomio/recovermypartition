#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os, sys, time,  string,  math,  calendar,  datetime, gettext,subprocess
from subprocess import *
from optparse import OptionParser

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
    
    def resetColor(self, ):
        return self.codes["reset"]
    def ctext(self, color,text):
        return self.codes[ctext]+text+self.codes["reset"]
    def bold(self, text):
        return self.codes["bold"]+text+self.codes["reset"]
    def white(self, text):
        return bold(text)
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

#
#def endslash (path):
#    """Esta función hace que el path pasado como parametro acabe en una barra
#    Por ejemplo endslash('/home/pepe') devuelve /home/pepe/"""
#    if path[len(path)-1]=="/":
#        return path
#    else:
#        return path +"/"


def contador(puntpasosdesdecero, totalpasos, tiempo_inicio_contador_parcial):
    """
        Función que devuelve segundos estimados
    """        
    tiempoactual=time.time()
    resultado=(totalpasos-puntpasosdesdecero)*(tiempoactual-tiempo_inicio_contador_parcial)/puntpasosdesdecero
    return resultado



def path2sleuthkit(cadena):
    """Que sustituya por _ cuando se saca un listado sleuthkit y
    nosotros generamos el sistema de ficheros.
    """
    todelete=('?','!','¡','"')
    for caracter in todelete:
        cadena=string.replace(cadena,caracter,'_')
    return cadena

def segundos2fechastring(segundos):
    dias=int(segundos/(24*60*60))
    segundosquedan=math.fmod(segundos,24*60*60)
    horas=int(segundosquedan/(60*60))
    segundosquedan=math.fmod(segundosquedan,60*60)
    minutos=int(segundosquedan/60)
    segundosquedan=math.fmod(segundosquedan,60)
    segundos=int(segundosquedan)
    #return str(dias)+ "d "+ str(horas) + "h " + str(minutos) + "m " + str(segundos) +"s"
    return "{0:d}d {1}h {2}m {3}s".format(dias,  horas,  minutos, segundos)

def string2time(cadena):
    try:
        t= time.strptime(cadena,"%Y-%m-%d %H:%M:%S (%Z)")
#        print (t)#parece que lo hace bien
    except:
        return None
    return t 


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
            return _("Virtual")+"/"+self.name
        elif self.deleted==True:
            return _("Deleted")+"/"+self.name
        return _("Files") +"/"+ self.name
      
    def isCriticalError(self):
        "Devuelve si hay un error crítico, es decir menor que 20"
        if len(self.errors)==0:
            return False
            
        for e in self.errors:
            if e<20:
                return True
        return False
      
    def save(self):
        if self.inode==0:
            self.errors.append(1)
            
        fullpath=options.output+"/" +self.path()
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
            errores=errores +"Inodo vale 0, "
        if 5 in self.errors:
            errores=errores +"No he podido crear el directorio para fichero directorio, "
        if 10 in self.errors:
            errores=errores +"No he podido crear el fichero, icat exception"
        if 11 in self.errors:
            errores=errores +"No he podido crear el fichero, icat error >0"
        if 15 in self.errors:
            errores=errores +"No he podido crear el directorio para este fichero, "
        if 20 in self.errors:
            errores=errores +"Hora acceso no recuperada, "
        if 25 in self.errors:
            errores=errores +"Hora modificación no recuperada, "
        if 30 in self.errors:
            errores=errores +"Hora acceso y modificación no recreada, "
            
        return """
Name: """ + self.name +"""
i-node: """ + self.inode +"""
Deleted: """ + str(self.deleted) + """
Reallocated: """ + str(self.reallocated) + """
Type: """+ self.type+"/"+self.type_metadata+"""
Access time: """+ str(self.acc_time)+"""
Modification time: """+str(self.mod_time)+"""
Change time: """+str(self.chg_time)+"""
Creation time: """+str(self.cre_time)+"""
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
            directoriotemporaltrabajo+'/csa/particion.' + idparticion + '
        """
        try:
            os.makedirs(path)
        except:
            pass
        comando='blkls -s %s  > %s'%(path_evidencia, path_salida_dd)
        os.popen(comando)



    
gettext.bindtextdomain('recovermypartition','/usr/share/locale/')
gettext.textdomain('recovermypartition')

def _(cadena):
    return gettext.gettext(cadena)

num_total_ficheros=0 # Numero de ficheros en la lista de recuperacion
num_positivos_nsrl=0 #Numero de ficheros que dan positivo en nsrl
num_recuperados=0
version="20130128"
    
parser = OptionParser(version=version,  description=_("Recupera los ficheros, los ficheros borrados de una partición"))
parser.add_option( "--no-files", action="store_true", default=False, dest="nofiles", help=_("No extrae ficheros normales"))
parser.add_option( "--no-deleted", action="store_true", default=False, dest="nodeleted", help=_("No extrae ficheros borrados"))
parser.add_option( "--csa", action="store_true", default=False, dest="csa", help=_("Analiza los clusters sin asignar con foremost"))
parser.add_option( "--nsrl", action="store_true", default=False, dest="nsrl", help=_("Chequea contra la base de datos nrsl"))
parser.add_option( "--partition", action="store", dest="partition", help=_("Partición o imagen a analizar"))
output="recovermypartition_{0}/".format(str(datetime.datetime.now())[:19]).replace(" ","_").replace(":","").replace("-","")
parser.add_option( "--output", action="store",  dest="output", default=output,  help=_("Directorio de salida"))
(options, args) = parser.parse_args()

try:
    dir_uac=options.output+_('CSA')+'/'
    os.makedirs(options.output)
    os.makedirs(dir_uac)
except OSError:
    print (_("Ha habido problemas al crear los directorios de salida. Compruebe que no existe"))
    sys.exit()
    
error=open(options.output+"recovermypartition.error", "w")
log=open(options.output + "/recovermypartition.log", "w")
tiempo_contador_parcial=time.time()
log.write(_("La recuperación comenzó") + ": " + str(datetime.datetime.now()) +"\n")
    
if options.partition==None:
    print (_("No se ha especificado la partición"))
    sys.exit(190)

if options.nofiles==False and options.nodeleted==False:
    print (Color().red(_("Generando lista para todos los ficheros, incluidos borrados")))
    fls=os.popen("fls -prl " + options.partition ).readlines()
elif options.nofiles==True and options.nodeleted==False:
    print (Color().red(_("Generando lista sólo para ficheros borrados")))
    fls=os.popen("fls -prdl " + options.partition ).readlines()
elif options.nofiles==False and options.nodeleted==True:
    print (Color().red(_("Generando lista sólo para ficheros normales")))
    fls=os.popen("fls -prul " + options.partition ).readlines()



##CREA FICHERO SLEUTHKIT
f=open(options.output + "/recovermypartition.sleuthkit", "w")
for line in fls:
    f.write(line)
f.close()

##ARRANCA    
print (Color().fuchsia(_("Particion o imagen a analizar")+": ") + options.partition)
print (Color().fuchsia(_("Directorio de salida")+":          ") + options.output)

num_total_ficheros=len(fls)
puntnumerototalficheros=num_total_ficheros
print (Color().green( _("+ Recuperando {0} ficheros de la partición. Este proceso puede tardar bastante.".format(num_total_ficheros  ))))
for linea in fls:
    if options.nsrl==True:
        sys.stdout.write (_("No desarrollado todavía"))
    else:
        f=File(linea)
        f.save()
        if f.isCriticalError()==False:
            num_recuperados=num_recuperados+1
        else:
            print (f, f.isCriticalError(), f.errors)
        puntnumerototalficheros=puntnumerototalficheros-1
        #cadena= _("  - Quedan ") + str(puntnumerototalficheros) + _(" de ") + str(num_total_ficheros) + _(". [ Recuperados: ")+Color().green(str(num_recuperados))+_(" ]. T.Est: ") + Color().yellow(segundos2fechastring(contador(num_total_ficheros-puntnumerototalficheros,num_total_ficheros,tiempo_contador_parcial)) ) + "  "
        cadena= _("  - Quedan  {0} de {1}. [ Recuperados: {2}]. T.Est: {3}                     ".format(puntnumerototalficheros, num_total_ficheros,  Color().green(str(num_recuperados)), Color().yellow(segundos2fechastring(contador(num_total_ficheros-puntnumerototalficheros,num_total_ficheros,tiempo_contador_parcial)) ) ))
        
        
    sys.stdout.write("\b"*(len(cadena)+5)) 
    sys.stdout.write (cadena)   
    sys.stdout.flush()  

if options.csa==True:
    print (Color().green("\n+ "+ _("Generando imagen dd de los clusters sin asignar")))
    Sleuthkit().blkls(options.partition, options.output +_('csa')+'.dd' )

    os.system('foremost -o '+ dir_uac+ ' -i ' +  options.output +_('csa')+'.dd')
error.close()
print ("\n")

##CREA FICHERO SLEUTHKIT
f=open(options.output + "/recovermypartition.sleuthkit", "w")
for line in fls:
    f.write(line)
f.close()

##CREA FICHERO LOG
log.write(_("La recuperación finalizó") + ": " + str(datetime.datetime.now()) +"\n")
log.write(_("Número de ficheros analizados") + ": " + str(len(fls)) +"\n")
log.write(_("Número de ficheros recuperados") + ": " + str(num_recuperados) +"\n")
log.close()


##MUESTRA TIEMPO DEL PROCESO
print (Color().green("+ "+_("El proceso ha durado" )+ " "+segundos2fechastring(time.time()-tiempo_contador_parcial) ))
