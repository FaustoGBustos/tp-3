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
import time
import pwinput

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
def buscaSec(mail):
    global afUsuarios, alUsuarios
    t = os.path.getsize(afUsuarios)
    alUsuarios.seek(0)  
    while alUsuarios.tell()<t:
        pos = alUsuarios.tell()
        vrTemp = pickle.load(alUsuarios)
        vrTempsinesp = vrTemp.nombreUsuario #Esto lo hago porque debido al formateo uno tiene espacios y el otro no, entonces para que la comparacion funcione, le saco los espacios
        vrTempor = vrTempsinesp.strip()
        if (vrTempor) == mail:
            return pos
    return -1
#------------------------------------------------------------------------------------------------------------------------------------------#
def crearUsuarios():
    global alUsuarios, afUsuarios
    print("-----------------------------------------")
    print("|              REGISTRACIÓN             |")
    print("-----------------------------------------")
    
    
    mail = str(input("Ingrese su correo electrónico para su nombre de usuario <máx. 100 caracteres>. "))
 
    while len(mail)< 1 and len(mail) > 100:
        mail = input("Incorrecto! su correo electrónico debe tener hasta 100 caracteres. ")
        
    regUsu = usuarios()
    if buscaSec(mail) == -1:
        regUsu.nombreUsuario = mail
        contra = pwinput.pwinput("Ingrese una contraseña. Debe tener exactamente 8 caracteres ")
        while len(contra) != 8:
            contra = pwinput.pwinput(("Incorrecto! su contraseña debe tener 8 caracteres. "))
        regUsu.claveUsuario = contra
        regUsu.codUsuario = codUser() + 1
        regUsu.tipoUsuario = "cliente"
        formatearUsuario(regUsu)# es para que todos los registros tengan las mismas longitudes en todos los campos, por tanto todos tendran el mismo peso
        pickle.dump(regUsu, alUsuarios)
        alUsuarios.flush()    
    else:
        print("El usuario ya existe.") 
             
def codUser():
    
    alUsuarios.seek(0) # me posiciono en el primer registro
    aux = pickle.load(alUsuarios) # lo traigo a memoria
    tamReg = alUsuarios.tell() # obtengo el peso en bytes del registro(todos pesan lo mismo)
    
    alUsuarios.seek(-tamReg, 2) # me posiciono en el final, y me muevo hacia atras un registro(tamreg)
    aux = pickle.load(alUsuarios)# traigo a memoria el ultimo registro cargado
    cod = aux.codUsuario # obtengo el codigo del ultimo registro cargado
    return int(cod) # lo devuelvo para luego ir aumentando uno en uno cada vez que se cree uno nuevo

#------------------------------------------------------------------------------------------------------------------------------------------#
def ingresoUsuarios(): # recordar INACTIVOS
    mail = str(input("ingrese su nombre de usuario"))
    contra = pwinput.pwinput("Ingrese una contraseña. Recuerde que son exactamente 8 caracteres ")

    # si es -1, quiere decir que el usuario no existe, si es otro numero, muestra la posicion del registro q lo contiene
    pos = buscaSec(mail)

    #nos posicionamos ahi
    alUsuarios.seek(pos, 0)
    #traemos a memoria el registro
    aux = pickle.load(alUsuarios)
    
    #de ese registro obtenemos la clave, y le sacamos los espacios para luego ver si coinciden con el usuario
    clave = aux.claveUsuario
    claveSinEspacios = clave.strip()

    # max 3 intentos
    error = 0
    while ((pos == -1) or (claveSinEspacios != contra)) and error != 2:
        print("El usuario y la contraseña no concide. Recuerden que son 3 intentos como maximo")
        mail = str(input("ingrese su nombre de usuario"))
        contra = pwinput.pwinput("Ingrese una contraseña correcta.")
        pos = buscaSec(mail)
        error += 1
        if error == 2:
            return "intentos maximos alcanzados"
        
    # devuelve que tipo de usuario es para devolverle el menu correspondiente
    return aux.tipoUsuario 

    #traer el registro y buscar la contraseña, con la pos accedemos a la ubicacion del registro

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
    print(Fore.GREEN + "-----------------------------------------")
    print(Fore.GREEN + "|            MENU PRINCIPAL             |")
    print(Fore.GREEN + "-----------------------------------------")
    print("1. Ingresar con usuario registrado\n2. Registrarse como cliente \n3. Salir ")

def menuAdministrador():
    menu_administrador = """
    *******************************************
    *            MENU ADMINISTRADOR            *
    *******************************************
    1. Gestión de locales
    2. Crear cuentas de dueños de locales
    3. Aprobar / Denegar solicitud de descuento
    4. Gestión de Novedades
    5. Reporte de utilización de descuentos
    0. Salir
    *******************************************
    """
    print(menu_administrador)

def menuGestionDeLocales():
    menu_gestion_locales = """
    *******************************************
    *         GESTIÓN DE LOCALES               *
    *******************************************
    1. Gestión de Locales
    a) Crear locales
    b) Modificar local
    c) Eliminar local
    d) Mapa de locales
    e) Volver
    *******************************************
    """

    print(menu_gestion_locales)

def menuGestionDeNovedades():
    menu_gestion_novedades = """
    *******************************************
    *        GESTIÓN DE NOVEDADES (Chapin)     *
    *******************************************
    4. Gestión de novedades (solo chapin)
    a) Crear novedades
    b) Modificar novedad
    c) Eliminar novedad
    d) Volver
    *******************************************
    """

    print(menu_gestion_novedades)
   
def menuDuenoDeLocal():
    menu_dueno_de_local = """
    *******************************************
    *           MENU DUEÑO DE LOCAL           *
    *******************************************
    1. Crear descuento
    2. Reporte de uso de descuentos
    3. Ver novedades (solo chapin)
    0. Salir
    *******************************************
    """

    print(menu_dueno_de_local)

def menuCliente():
    menu_cliente = """
    *******************************************
    *               MENU CLIENTE               *
    *******************************************
    1. Buscar descuentos en local
    2. Solicitar descuento
    3. Ver novedades (solo chapin)
    0. Salir
    *******************************************
    """
    print(menu_cliente)

def creacionDeLocales():
    print("hola")
#---------------Programa principal---------------------------------------------------------------------------------------------------------#
afUsuarios = "C:\\ayed\\usuarios.dat" 

if os.path.exists(afUsuarios):
    alUsuarios = open(afUsuarios,"r+b") #el archivo ya existe, el puntero va al inicio.
else:
    alUsuarios = open(afUsuarios,"w+b") #el archivo no existe, lo crea.
    #precarga el primer usuario que debe aparecer una vez se inicie el archivo por primera vez
    rUsu = usuarios()
    rUsu.codUsuario = 1
    rUsu.nombreUsuario = "admin@shopping.com"
    rUsu.claveUsuario = "12345"
    rUsu.tipoUsuario = "administrador"
    formatearUsuario(rUsu) # es para que todos los registros tengan las mismas longitudes en todos los campos, por tanto todos tendran el mismo peso
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
        tipoUser = ingresoUsuarios()
        tipoUseraSE = tipoUser.strip()#poner sin espacios
        if tipoUseraSE == "administrador":
            menuAdministrador()
            opc = -1
            while opc != 0:
                opc = input("Ingrese una opción [1-5]: ")
                while validaRangoEnteros(opc, 1, 5):
                    opc = input(Fore.RED + "Incorrecto - Ingrese una opción [1-5]: " + Fore.RESET)
                opc = int(opc)
                if opc == 1:
                    menuGestionDeLocales()
                    while opc != 0:
                        opc = input("Ingrese una opción [1-5]: ")
                        while validaRangoEnteros(opc, 1, 5):
                            opc = input(Fore.RED + "Incorrecto - Ingrese una opción [1-5]: " + Fore.RESET)
                        opc = int(opc)
                        if opc == 1:
                            print("crear locales")
                            creacionDeLocales()
                        elif opc == 2:
                            print("modificar local")
                        elif opc == 3:
                            print("eliminar local")
                        elif opc == 4:
                            print("Mapa locales")
                        elif opc == 5:
                            print("volver")
                elif opc == 2:
                    print("crear cuentas de dueños de locales")
        elif tipoUseraSE == "cliente":
            menuCliente()
        elif tipoUseraSE == "dueñoDeLocal":
            menuDuenoDeLocal()
    elif opc == 2:
        crearUsuarios()
    elif opc == 3:
        print("\n\nGracias por visitarnos ...\n\n")
alUsuarios.close()
