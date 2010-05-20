#!/usr/bin/env python
#-*- coding: utf-8 -*- 
import os, sys, getopt, time,  string,  math,  calendar,  re
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


def endslash (path):
    """Esta función hace que el path pasado como parametro acabe en una barra
    Por ejemplo endslash('/home/pepe') devuelve /home/pepe/"""
    if path[len(path)-1]=="/":
        return path
    else:
        return path +"/"


def contador(puntpasosdesdecero, totalpasos, tiempo_inicio_contador_parcial):
    """
        Función que devuelve segundos estimados
    """        
    tiempoactual=time.time()
    resultado=(totalpasos-puntpasosdesdecero)*(tiempoactual-tiempo_inicio_contador_parcial)/puntpasosdesdecero
    return resultado

    
def path2shell(cadena):
    cadena=string.replace(cadena,'\\','\\\\')
    todelete=('?','$','#','"',"'",'`','(',')','[',']','|','{','}','~',' ', ';','=','&','!','¡')
    for caracter in todelete:
        subs=''
        subs=subs.join(('\\',caracter))
        cadena=string.replace(cadena,caracter,subs)
    return cadena

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
  
def ayuda():
    print "recoverpartition [opciones] -p dispositivofisico|imagen.dd"
    print "  Brief: Recupera los ficheros, los ficheros borrados de una particion"
    print "         e intenta recuperar ficheros desde los clusters sin asignar."  
    print "  Version: " + version
    print "  Opciones: "
    print "           -p particion: particion o imagen"
    print "           -h: muestra esta ayuda"
    print "           -f: saca solo los ficheros normales"
    print "           -b: saca solo los borrados"
    print "           -o: directorio de salida (Default: Current Directory)"        
    print "           -n directorio: ubicación de la base de datos NSRL)"        


class EspacioSinAsignar:      
    def GeneraImagenDD(self, path_evidencia ,  path_salida_dd):
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
        
class Sleuthkit:      
    def atributos_desde_linea_sleuthkit(self,l):
        """
            Si el inodo vale 0 devuelve None
            file_type inode file_name mod_time acc_time chg_time cre_time size uid gid
        """
        atributos={}
        atributos['reallocated']=False
	atributos['deleted']=False
        if l.split(chr(9))[0].find("(realloc)")>-1:
	    atributos['reallocated']=True
	    atributos['deleted']=True
	    atributos['inode']= l.split(chr(9))[0].split(" ")[2][:-10]
	elif l.split(chr(9))[0].find("*")>-1:
	    atributos['deleted']=True
	    atributos['inode']= l.split(chr(9))[0].split(" ")[2][:-1]
	else:
	    atributos['inode']= l.split(chr(9))[0].split(" ")[1][:-1]
        atributos['type_filename']=l[0]
        atributos['type_metadata']=l[2]
	if atributos['inode']==0:
            return None
        atributos['file_name']=l.split(chr(9))[1]
        atributos['mod_time']=string2time(l.split(chr(9))[2])
        atributos['acc_time']=string2time(l.split(chr(9))[3])
        atributos['chg_time']=string2time(l.split(chr(9))[4])
        atributos['cre_time']=string2time(l.split(chr(9))[5])
        atributos['size']=int(l.split(chr(9))[6])
        atributos['uid']=int(l.split(chr(9))[7])
        atributos['gid']=int(l.split(chr(9))[8])
        #print str(l) + str(atributos)
        return atributos
    
    def crear_listado_ficheros(self , path_salida, path_imagen):
        """
            Funcion que genera el listado de ficheros de una particion 
             normales
            
            Lo genera en el directorio temporal de trabajo pasado como 
            parametro y en 
        """
        os.popen('fls -prFul ' + path_imagen + ' > ' + path_salida )
        return self.numero_lineas_fichero(path_salida)    
        
    
    def crear_listado_ficheros_borrados(self , path_salida, path_imagen):
        """
            Funcion que genera el listado de ficheros de una particion 
            borrados y normales
            
            Lo genera en el directorio temporal de trabajo pasado como 
            parametro y en 
        """
        os.popen('fls -prFdl ' + path_imagen + ' > ' + path_salida )
        return self.numero_lineas_fichero(path_salida)
        
    def numero_lineas_fichero(self,path):
        dic=os.popen("wc -l "+path+" | cut -f1 -d' '")
        return int(dic.readline())
        
    def recupera_fichero(self, directoriocreacion,enlacefisico,lineasleut):
        """
            Funcion que partiendo de una linea sin el caracter de retorno sleut
            y lo coloca en su directorio, 
            
            Devuelve un booleano si ha tenido exito o no la recuperacion
        """
        dic_atr=self.atributos_desde_linea_sleuthkit(lineasleut)
        if dic_atr==None:
            return False
        salida=directoriocreacion+ path2sleuthkit(dic_atr['file_name'])
        #print salida, dic_atr
        #pathsincomillas=path2sleuthkit(dic_atr['file_name'])
        if dic_atr['type_filename']=="r" or dic_atr['type_filename']=="l" or dic_atr['type_filename']=="-":
            try:
                os.makedirs(os.path.dirname(salida))
            except OSError:
                pass
            comando= 'icat -r ' + enlacefisico + ' ' +str(dic_atr['inode'])
            fichero=os.popen('icat -r ' + enlacefisico + ' ' +str(dic_atr['inode'])).read()
            f=open(salida,"w")
            f.write(fichero)
            f.close()
        elif dic_atr['type_filename']=="d":
	    os.makedirs(os.path.dirname(salida))
	else:
	    print "\nFichero tipo ",  dic_atr['type_filename'], salida
	    return False

	try:
            accesed=calendar.timegm(dic_atr['acc_time'])
        except:
	    print "    - No se ha podido modificar la fecha de acceso de " + 
	    accesed=0
	try:
            modified=calendar.timegm(dic_atr['mod_time'])
	    print "    - No se ha podido modificar la fecha de modificación de " + str(dic_atr)
        except:
	    modified=0
	os.utime(salida,(accesed,modified))
 
        return True


path_imagen=None   #Cadena con el nombre del dispositivo fisico o imagen dd
dir_tmp=None       #Cadena con el directorio de ficheros temporales
dir_salida=None     
dir_csa=None
num_total_ficheros=0 # Numero de ficheros en la lista de recuperacion
num_positivos_nsrl=0 #Numero de ficheros que dan positivo en nsrl
num_recuperados=0
extraer_solo_borrados=False
extraer_solo_normales=False
usar_nsrl=False
version="20100518"
    
    

bindtextdomain('recovermypartition','/usr/share/locale/')
textdomain('recovermypartition')

def _(cadena):
    return gettext(cadena)
 
if (len(sys.argv)<=1): 
    ayuda()
    sys.exit(1)
    
try:
    opts,args=getopt.gnu_getopt(sys.argv[1:],'vfbo:n:p:')
except getopt.GetoptError:
    print _(u'Error en la lectura de argumentos')+'\n'
    sys.exit(2)

for o,a in opts:

    if o == '-b':
        extraer_solo_borrados=True

    if o == '-p':
        path_imagen=a

    if o == '-h':
        ayuda()
        sys.exit()

    if o == '-f':
        extraer_solo_normales=True
        
    if o == '-o':
        dir_tmp=endslash(a)

    if o== '-n':
        usar_nsrl=True


if path_imagen==None:
    print ("No se ha encontrado la imagen")
    ayuda()
    sys.exit()
    
if extraer_solo_borrados==True and extraer_solo_normales==True:
    extraer_solo_borrados=False
    extraer_solo_normales=False            

if dir_tmp==None:
    dir_tmp=endslash(os.getcwd())

try:
    dir_salida=dir_tmp+"output/"#Cadena con el directorio raiz donde se genera todo.
    dir_ficheros=dir_salida+_('Ficheros')+'/'
    dir_borrados=dir_salida+_('Borrados')+'/'
    dir_csa=dir_salida+_('CSA')+'/'
    dir_foremost=dir_salida+_('CSA')+'/'
    os.makedirs(dir_salida)
    os.makedirs(dir_ficheros)
    os.makedirs(dir_borrados)
    os.makedirs(dir_csa)
except OSError:
    print _("Ha habido problemas al crear los directorios de salida. Compruebe que no existe")
    sys.exit()
    
if extraer_solo_normales==True:
    print Color().red(_(u"Solo extrae los ficheros normales"))
elif extraer_solo_borrados==True:
    print Color().red(_(u"Solo extrae los ficheros borrados"))
    


print Color().fuchsia(_(u"Particion o imagen a analizar")+": ") + path_imagen
print Color().fuchsia(_(u"Directorio de salida")+":          ") + dir_salida

tiempo_contador_parcial=time.time()

print Color().green("+ "+_("Recuperando el sistema de ficheros"))
if extraer_solo_borrados==False:
    num_total_ficheros=Sleuthkit().crear_listado_ficheros(dir_tmp+'/recuperaparticion.listaficheros',path_imagen)
    puntnumerototalficheros=num_total_ficheros
    f=file(dir_tmp+'/recuperaparticion.listaficheros',"r")
    while True:   
        linea=f.readline()
        if linea=='':
            break
        if usar_nsrl==True:
            if Sleuthkit().recupera_fichero_sino_nsrl(dir_ficheros,path_imagen,linea[:-1])==True:
                num_recuperados=num_recuperados+1
            puntnumerototalficheros=puntnumerototalficheros-1
            cadena= _(u"  - Normales. Quedan ") + str(puntnumerototalficheros) + _(u" de ") + str(num_total_ficheros) + _(u". [ Recuperados: ")+Color().green(str(num_recuperados))+_(u"   NSRL: ")+Color().green(str(num_positivos_nsrl))+_(u" ]. T.Est: ") + segundos2fechastring(contador(num_total_ficheros-puntnumerototalficheros,num_total_ficheros,tiempo_contador_parcial))
        else:
            if Sleuthkit().recupera_fichero(dir_ficheros,path_imagen,linea[:-1])==True:
                num_recuperados=num_recuperados+1
            puntnumerototalficheros=puntnumerototalficheros-1
            cadena= _(u"  - Normales. Quedan ") + str(puntnumerototalficheros) + _(u" de ") + str(num_total_ficheros) + _(u". [ Recuperados: ")+Color().green(str(num_recuperados))+_(u" ]. T.Est: ") + Color().yellow(segundos2fechastring(contador(num_total_ficheros-puntnumerototalficheros,num_total_ficheros,tiempo_contador_parcial)) ) + "  "
            
            
        sys.stdout.write("\b"*(len(cadena)+5)) 
        sys.stdout.write (cadena)   
        sys.stdout.flush()  
    print ""


print Color().green("+ " + _("Recuperando ficheros borrados"))
if extraer_solo_normales==False : 
    num_total_ficheros=Sleuthkit().crear_listado_ficheros_borrados(dir_tmp+'/recuperaparticion.listaficherosborrados',path_imagen)
    puntnumerototalficheros=num_total_ficheros
    f=file(dir_tmp+'/recuperaparticion.listaficherosborrados',"r")
    while True:            
        linea=f.readline()
        if linea=='':
            break
        if usar_nsrl==True:
            if Sleuthkit().recupera_fichero_sino_nsrl(dir_borrados,path_imagen,linea[:-1])==True:
                num_recuperados=num_recuperados+1
            puntnumerototalficheros=puntnumerototalficheros-1
            cadena= _(u"  - Borrados. Quedan ") + str(puntnumerototalficheros) + _(u" de ") + str(num_total_ficheros) + _(". [ Recuperados: ")+Color().green(str(num_recuperados))+_(u"   NSRL: ")+Color().green(str(num_positivos_nsrl))+_(u" ]. [ Recuperados: ")+Color().green(str(num_recuperados))+_(u"   NSRL: ")+Color().green(str(num_positivos_nsrl))+_(u" ]. T.Est: ") + segundos2fechastring(contador(num_total_ficheros-puntnumerototalficheros,num_total_ficheros,tiempo_contador_parcial))
        else:
            if Sleuthkit().recupera_fichero(dir_borrados,path_imagen,linea[:-1])==True:
                num_recuperados=num_recuperados+1
            puntnumerototalficheros=puntnumerototalficheros-1
            cadena= _(u"  - Borrados. Quedan ") + str(puntnumerototalficheros) + _(u" de ") + str(num_total_ficheros) + _(". [ Recuperados: ")+Color().green(str(num_recuperados))+_(u" ]. T.Est: ") + Color().yellow(segundos2fechastring(contador(num_total_ficheros-puntnumerototalficheros,num_total_ficheros,tiempo_contador_parcial))) + "  "
        sys.stdout.write("\b"*(len(cadena)+5)) 
        sys.stdout.write (cadena)   
        sys.stdout.flush()  
    print ""
        
print Color().green("+ "+ _("Generando imagen dd de los clusters sin asignar"))
EspacioSinAsignar().GeneraImagenDD(path_imagen, dir_salida +_('csa')+'.dd' )

os.system('foremost -o '+ dir_foremost+ ' -i ' +  dir_salida +_('csa')+'.dd')

#comando='rm ' + dir_salida +_('csa')+'.dd'
#os.system(comando)

comando='rm ' +dir_tmp +'/recuperaparticion.listaficheros'
os.system(comando)

comando='rm ' +dir_tmp +'/recuperaparticion.listaficherosborrados'
os.system(comando)
