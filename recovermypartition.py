#!/usr/bin/env python
#-*- coding: utf-8 -*- 
import os, sys, time,  string,  math,  calendar,  datetime
from subprocess import *
from optparse import OptionParser
from gettext import *

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
    dias=int(segundos)/int(24*60*60)
    segundosquedan=math.fmod(segundos,24*60*60)
    horas=int(segundosquedan)/int(60*60)
    segundosquedan=math.fmod(segundosquedan,60*60)
    minutos=int(segundosquedan)/int(60)
    segundosquedan=math.fmod(segundosquedan,60)
    segundos=int(segundosquedan)
    return str(dias)+ "d "+ str(horas) + "h " + str(minutos) + "m " + str(segundos) +"s"

def string2time(cadena):
    try:
        t= time.strptime(cadena,"%Y-%m-%d %H:%M:%S (%Z)")
    except:
        return None
    return t 

class Sleuthkit:      
    def fls2arr(self,l):
        """
            Si el inodo vale 0 devuelve None
            file_type inode file_name mod_time acc_time chg_time cre_time size uid gid
        """
        arr={}
        arr['reallocated']=False
        arr['deleted']=False
        if l.split(chr(9))[0].find("(realloc)")>-1:
            arr['reallocated']=True
            arr['deleted']=True
            arr['inode']= l.split(chr(9))[0].split(" ")[2][:-10]
        elif l.split(chr(9))[0].find("*")>-1:
            arr['deleted']=True
            arr['inode']= l.split(chr(9))[0].split(" ")[2][:-1]
        else:
            arr['inode']= l.split(chr(9))[0].split(" ")[1][:-1]
        arr['type_filename']=l[0]
        arr['type_metadata']=l[2]
        if arr['inode']==0:
            return None
        arr['file_name']=l.split(chr(9))[1]
        arr['mod_time']=string2time(l.split(chr(9))[2])
        arr['acc_time']=string2time(l.split(chr(9))[3])
        arr['chg_time']=string2time(l.split(chr(9))[4])
        arr['cre_time']=string2time(l.split(chr(9))[5])
        arr['size']=int(l.split(chr(9))[6])
        arr['uid']=int(l.split(chr(9))[7])
        arr['gid']=int(l.split(chr(9))[8])
        
        ##Curiosidades
        if arr['file_name']=="$OrphanFiles" and arr['type_filename']=="d":
            arr['deleted']=True
        return arr
    
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
        sal=os.popen(comando)


    def icat(self, lineasleuthkit):
        """
            Funcion que partiendo de una linea sin el caracter de retorno sleut
            y lo coloca en su directorio, 
            
            Devuelve un booleano si ha tenido exito o no la recuperacion
        """
        def salida():
            if arr['type_filename']=="v":
                return options.output+ arr['file_name']
            if arr['deleted']==True:
                return dir_deleted+ arr['file_name']
            else:
                return dir_files+ arr['file_name']

        arr=self.fls2arr(lineasleuthkit)
        if arr==None:
            return False
            
        if arr['type_filename']=="d":       
            try:
                os.makedirs(salida())
            except OSError:
                pass            
        else:
            try:
                os.makedirs(os.path.dirname(salida()))
            except OSError:
                pass
            p = Popen('icat -r ' + options.partition + ' ' +str(arr['inode']) +" > /tmp/recovermypartition", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
            strerror=p.stderr.read()[:-1]
            if len(strerror)>0:
                error.write (str(datetime.datetime.now()) + "\t" +  lineasleuthkit.split(chr(9))[0]+ "\t"+ salida()+ "\ticat. " +  strerror + "\n")            
            os.rename ("/tmp/recovermypartition",  salida())


        try:
            accesed=calendar.timegm(arr['acc_time'])
        except:
            error.write (str(datetime.datetime.now())+ "\t" +  lineasleuthkit.split(chr(9))[0] + "\t" + salida()+ "\t"+_("No se ha podido modificar la fecha de acceso")+"\n" )
            accesed=0
    
        try:
            modified=calendar.timegm(dic_atr['mod_time'])
        except:
            error.write (str(datetime.datetime.now())+ "\t" +  lineasleuthkit.split(chr(9))[0] + "\t" + salida()+ "\t"+_("No se ha podido modificar la fecha de modificación")+"\n")
            modified=0
        os.utime(salida(),(accesed,modified))
        return True

    
bindtextdomain('recovermypartition','/usr/share/locale/')
textdomain('recovermypartition')

def _(cadena):
    return gettext(cadena)

num_total_ficheros=0 # Numero de ficheros en la lista de recuperacion
num_positivos_nsrl=0 #Numero de ficheros que dan positivo en nsrl
num_recuperados=0
version="20100520"
    
parser = OptionParser(version=version,  description=_("Recupera los ficheros, los ficheros borrados de una particion"))
parser.add_option( "--no-files", action="store_true", default=False, dest="nofiles", help=_(u"No extrae ficheros normales"))
parser.add_option( "--no-deleted", action="store_true", default=False, dest="nodeleted", help=_(u"No extrae ficheros borrados"))
parser.add_option( "--csa", action="store_true", default=False, dest="csa", help=_(u"Analiza los clusters sin asignar con foremost"))
parser.add_option( "--nsrl", action="store_true", default=False, dest="nsrl", help=_(u"Chequea contra la base de datos nrsl"))
parser.add_option( "--partition", action="store", dest="partition", help=_(u"Partición o imagen a analizar"))
parser.add_option( "--output", action="store",  dest="output", default="output/",  help=_(u"Directorio de salida (Default output)"))
(options, args) = parser.parse_args()

try:
    dir_files=options.output+_('Ficheros')+'/'
    dir_deleted=options.output+_('Borrados')+'/'
    dir_uac=options.output+_('CSA')+'/'
    os.makedirs(options.output)
    os.makedirs(dir_files)
    os.makedirs(dir_deleted)
    os.makedirs(dir_uac)
except OSError:
    print (_("Ha habido problemas al crear los directorios de salida. Compruebe que no existe"))
    sys.exit()
    
error=open(options.output+"recovermypartition.error", "w")
log=open(options.output + "/recovermypartition.log", "w")
tiempo_contador_parcial=time.time()
log.write(_("La recuperación comenzó") + ": " + str(datetime.datetime.now()) +"\n")
    
if options.nofiles==False and options.nodeleted==False:
    print (Color().red(_(u"Generando lista para todos los ficheros, incluidos borrados")))
    fls=os.popen("fls -prl " + options.partition ).readlines()
elif options.nofiles==True and options.nodeleted==False:
    print (Color().red(_(u"Generando lista sólo para ficheros borrados")))
    fls=os.popen("fls -prdl " + options.partition ).readlines()
elif options.nofiles==False and options.nodeleted==True:
    print (Color().red(_(u"Generando lista sólo para ficheros normales")))
    fls=os.popen("fls -prul " + options.partition ).readlines()
    
print (Color().fuchsia(_(u"Particion o imagen a analizar")+": ") + options.partition)
print (Color().fuchsia(_(u"Directorio de salida")+":          ") + options.output)

num_total_ficheros=len(fls)
puntnumerototalficheros=num_total_ficheros

print (Color().green("+ "+_("Recuperando")+ " " +  str(num_total_ficheros) + " " + _(u"ficheros de la partición. Este proceso puede tardar bastante")))

for linea in fls:
    if options.nsrl==True:
        sys.stdout.write (_("No desarrollado todavía"))
    else:
        if Sleuthkit().icat(linea[:-1])==True:
            num_recuperados=num_recuperados+1
        puntnumerototalficheros=puntnumerototalficheros-1
        cadena= _(u"  - Quedan ") + str(puntnumerototalficheros) + _(u" de ") + str(num_total_ficheros) + _(u". [ Recuperados: ")+Color().green(str(num_recuperados))+_(u" ]. T.Est: ") + Color().yellow(segundos2fechastring(contador(num_total_ficheros-puntnumerototalficheros,num_total_ficheros,tiempo_contador_parcial)) ) + "  "
        
        
    sys.stdout.write("\b"*(len(cadena)+5)) 
    sys.stdout.write (cadena)   
    sys.stdout.flush()  

if options.csa==True:
    print Color().green("\n+ "+ _("Generando imagen dd de los clusters sin asignar"))
    Sleuthkit().blkls(options.partition, options.output +_('csa')+'.dd' )
    
    os.system('foremost -o '+ dir_uac+ ' -i ' +  options.output +_('csa')+'.dd')
error.close()
print 

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
