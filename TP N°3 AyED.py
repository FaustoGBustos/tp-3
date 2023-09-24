#TP N°3 ALgoritmos y estructuras de datos
# Fausto Bustos, Santiago Gerez, Fernando Pelmailrini y Lara Varrenti

import os
from types import NoneType                        #realiza operaciones en el SO correspondiente
from pwinput import pwinput                   #censura la contraseña
import os.path                   #identifica rutas locales
import pickle                    #permite leer y escribir archivos
import io                        #permite acceder a archivos de forma directa
from datetime import datetime    #permite manejar variables tipo fecha y hora
from datetime import date        #permite manejar variables tipo fecha
from colorama import Fore, init  #para poner colores | EJ: print(Fore.GREEN + "holis")
init(autoreset=True)             #inicializamos los colores

#ARCHIVOS:
#   - 
#   -
#   -
#REGISTROS
#   - usuarios
#   - locales
#   - promociones
#   - uso_promociones
#   - novedades
#ARREGLOS
#   - diasSemana array [0..6] int
#   -
#   -
#------------------------------------------------------------------------------------------------------------------------------------------#
global afUsuarios, alUsuarios

class usuarios:
        def __init__(self):
            self.codUsuario = 0
            self.nombreUsuario = ""
            self.claveUsuario = ""
            self.tipoUsuario = ""
class locales:
    def __init__(self):
        self.nombreLocal = 0
        self.ubicLocal = ""
        self.rubroLocal = ""
        self.codUsuario = 0
        self.estado = ""
class promociones:
    def __init__(self):
        self.codPromo = 0
        self.textoPromo = ""
        self.fechaDesdePromo = None 
        self.fechaHastaPromo = None
        self.diasSemana = [0]*6
        self.estado = ""
        self.codLocal = 0
class uso_promociones:
    def __init__(self):
        self.codCliente = 0
        self.codPromo = 0
        self.fechaUsoPromo = None
class novedades:
    def __init__(self):
        self.codNovedades = 0
        self.textoNovedades = ""
        self.fechaDesdeNovedades = None
        self.fechaHastaNovedades = None
        self.tipoUsuario = ""
        self.estado = ""

def formatearUsuario (rUsu):
    rUsu.nombreUsuario = str(rUsu.nombreUsuario)
    rUsu.nombreUsuario = rUsu.nombreUsuario.ljust(100, ' ') 
    rUsu.claveUsuario = str(rUsu.claveUsuario)
    rUsu.claveUsuario = rUsu.claveUsuario.ljust(8, ' ')
    rUsu.tipoUsuario = str(rUsu.tipoUsuario)
    rUsu.tipoUsuario = rUsu.tipoUsuario.ljust(20, ' ')
#------------------------------------------------------------------------------------------------------------------------------------------#
def Buscasec(mail, regUsu):
    global afUsuarios, alUsuarios
    t = os.path.getsize(afUsuarios)
    pos = 0
    alUsuarios.seek(0, 0)  
    if t>0:
        regUsu = pickle.load(alUsuarios)
        while (alUsuarios.tell() < t) and (mail != regUsu.nombreUsuario):
            pos = alUsuarios.tell()
            regUsu = pickle.load(alUsuarios)
        if regUsu.nombreUsuario == mail:        
         return pos
        else:
         return -1
    else:
        print('-----------------')
        print("Archivo sin datos")
        print('-----------------')
        return -1
#------------------------------------------------------------------------------------------------------------------------------------------#
def crearUsuarios():
    global alUsuarios, afUsuarios
    os.system("cls")
    print("-----------------------------------------")
    print("|              REGISTRACIÓN             |")
    print("-----------------------------------------")
    regUsu = usuarios()
    mail = input("Ingrese su correo electrónico para su nombre de usuario <máx. 100 caracteres>. ")
    while len(mail)< 1 and len(mail) > 100:
        mail = input("Incorrecto! su correo electrónico debe tener hasta 100 caracteres. ")
    while Buscasec(mail, regUsu) == -1:
        print("\nCorreo ya registrado. Intente nuevamente:")
        mail = input()
        while len(mail)< 1 and len(mail) > 100:
            mail = input("Incorrecto! su correo electrónico debe tener hasta 100 caracteres. ")
    regUsu.nombreUsuario = mail
    
    os.system("cls")
    contra = input("Ingrese una contraseña. Debe tener 8 caracteres")
    while len(contra) != 8:
        contra = input("Incorrecto! su contraseña debe tener 8 caracteres. ")
    regUsu.claveUsuario = contra
    
    # regUsu.codUsuario =   tiene que ser consecutivo
    regUsu.tipoUsuario = "cliente"
    formatearUsuario(regUsu) 
    pickle.dump(regUsu, alUsuarios)
    alUsuarios.flush()
    os.system("cls")
    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print(" Registración exitosa")
    print("~~~~~~~~~~~~~~~~~~~~~~~")

    
#------------------------------------------------------------------------------------------------------------------------------------------#
def ingresoUsuarios():
    os.system("cls")
    print("-----------------------------------------")
    print("|           INICIO DE SESIÓN            |")
    print("-----------------------------------------")
    os.system("pause")
#------------------------------------------------------------------------------------------------------------------------------------------#
def validaRangoEnteros(nro, desde, hasta):
	try:              
		int(nro)      
		if int(nro) >= desde and int(nro) <= hasta:
			return False 
		else:
			return True  
	except:
		return True 
#------------------------------------------------------------------------------------------------------------------------------------------#
def mostrarMenu():
    os.system("cls")
    print(Fore.GREEN + "-----------------------------------------")
    print(Fore.GREEN + "|            MENU PRINCIPAL             |")
    print(Fore.GREEN + "-----------------------------------------")
    print("1. Ingresar con usuario registrado\n2. Registrarse como cliente \n3. Salir ")
#---------------Programa principal---------------------------------------------------------------------------------------------------------#
afUsuarios = "C:\\ayed\\usuarios.dat" 
if os.path.exists(afUsuarios):
     alUsuarios = open(afUsuarios,"r+b") #el archivo ya existe, el puntero va al inicio.
else:
    alUsuarios = open(afUsuarios,"w+b") #el archivo no existe, lo crea.
    rUsu = usuarios()
    rUsu.codUsuario = 1
    rUsu.nombreUsuario = "admin@shopping.com"
    rUsu.claveUsuario = "12345"
    rUsu.tipoUsuario = "administrador"
    formatearUsuario(rUsu) 
    pickle.dump(rUsu, alUsuarios)
    alUsuarios.flush()

opc = -1
while opc != 3:
	mostrarMenu()
	opc = input("Ingrese una opción [1-3]: ")
	while validaRangoEnteros(opc, 1, 3):
		opc = input(Fore.RED + "Incorrecto - Ingrese una opción [1-3]: " + Fore.RESET)
	opc = int(opc)
	if opc == 1:
		ingresoUsuarios()
	elif opc == 2:
		crearUsuarios()
	elif opc == 3:
		print("\n\nGracias por visitarnos ...\n\n")
alUsuarios.close() 