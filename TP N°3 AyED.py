#TP N°3 ALgoritmos y estructuras de datos
# Fausto Bustos, Santiago Gerez, Fernando Pellegrini y Lara Varrenti
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
        self.ubiLocal = ""
        self.rubroLocal = ""
        self.codUsuario = 0
        self.codLocal = 0
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
    rUsu.codUsuario = str(rUsu.codUsuario)
    
def formatearLocales(rLoc):
    rLoc.nombreLocal = str(rLoc.nombreLocal)
    rLoc.nombreLocal = rLoc.nombreLocal.ljust(50, ' ') 
    rLoc.ubiLocal = str(rLoc.ubiLocal)
    rLoc.ubiLocal = rLoc.ubiLocal.ljust(50, ' ')
    rLoc.rubroLocal = str(rLoc.rubroLocal)
    rLoc.rubroLocal = rLoc.rubroLocal.ljust(50, ' ')
    rLoc.codLocal = str(rLoc.codLocal)
    rLoc.codUsuario = str(rLoc.codUsuario)
    
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
def crearUsuariosTipoCliente():
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
        print("Usuario tipo cliente creado exitosamente")# estaria bueno poner una validacion corte ingrese de nuevo su contraseña para confirmar
    else:
        print("El usuario ya existe.") 
             
# def obtenerUltCod(file):
#     file.seek(0)  # Me posiciono en el primer registro
#     aux = pickle.load(file)  # Lo traigo a memoria
#     tamReg = file.tell()  # Obtengo el peso en bytes del registro (todos pesan lo mismo)

#     file.seek(-tamReg, 2)  # Me posiciono en el final y me muevo hacia atrás un registro (tamreg)
#     aux = pickle.load(file)  # Traigo a memoria el último registro cargado
#     cod = aux.codUsuario  # Obtengo el código del último registro cargado
#     return int(cod)  # Lo devuelvo para luego ir aumentando uno en uno cada vez que se cree uno nuevo

def codUser():
    alUsuarios.seek(0) # me posiciono en el primer registro
    aux = pickle.load(alUsuarios) # lo traigo a memoria
    tamReg = alUsuarios.tell() # obtengo el peso en bytes del registro(todos pesan lo mismo)
    
    alUsuarios.seek(-tamReg, 2) # me posiciono en el final, y me muevo hacia atras un registro(tamreg)
    aux = pickle.load(alUsuarios)# traigo a memoria el ultimo registro cargado
    cod = aux.codUsuario # obtengo el codigo del ultimo registro cargado
    return int(cod) # lo devuelvo para luego ir aumentando uno en uno cada vez que se cree uno nuevo

def codLocal():
    alLocales.seek(0) # me posiciono en el primer registro
    aux = pickle.load(alLocales) # lo traigo a memoria
    tamReg = alLocales.tell() # obtengo el peso en bytes del registro(todos pesan lo mismo)
    
    alLocales.seek(-tamReg, 2) # me posiciono en el final, y me muevo hacia atras un registro(tamreg)
    aux = pickle.load(alLocales)# traigo a memoria el ultimo registro cargado
    cod = aux.codUsuario # obtengo el codigo del ultimo registro cargado
    return int(cod) # lo devuelvo para luego ir aumentando uno en uno cada vez que se cree uno nuevo

#------------------------------------------------------------------------------------------------------------------------------------------#
def ingresoUsuarios(): # recordar INACTIVOS
    mail = str(input("ingrese su nombre de usuario: "))
    contra = pwinput.pwinput("Ingrese una contraseña. Recuerde que son exactamente 8 caracteres: ")

    # si es -1, quiere decir que el usuario no existe, si es otro numero, muestra la posicion del registro q lo contiene
    pos = buscaSec(mail)
    if pos != -1:

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

def ordenamiento():
    global afLocales, alLocales
    alLocales.seek(0)
    aux = pickle.load(alLocales)
    tamReg = alLocales.tell()
    tamArch = os.path.getsize(afLocales)
    cantReg = tamArch // tamReg
    for i in range(0 , cantReg-1):
        for j in range(i+1, cantReg):
            alLocales.seek(i*tamReg, 0)
            auxi = pickle.load(alLocales)
            alLocales.seek(j*tamReg,0)
            auxj = pickle.load(alLocales)
            if auxi.nombreLocal > auxj.nombreLocal:
                alLocales.seek(i*tamReg,0)
                pickle.dump (auxj, alLocales)
                alLocales. seek (j*tamReg, 0)
                pickle.dump(auxi,alLocales)

def busquedaDicotomica(a):
    global afLocales, alLocales

    alLocales.seek(0, 0)
    aux = pickle.load(alLocales)

    tamReg = alLocales.tell()
    tamArch = os.path.getsize(afLocales)
    cantReg = tamArch // tamReg

    desde = 0
    hasta = cantReg - 1
    medio = (desde + hasta)//2

    print(medio, desde, hasta, "medio,desde,hasta")
    alLocales.seek(medio*tamReg, 0)#2

    #sin espacios para comparar bien
    # SE = Sin Espacios
    vrLoc = pickle.load(alLocales)
    nombre1 = vrLoc.nombreLocal
    nombre1SE = nombre1.strip()

    while nombre1SE != a and desde < hasta:

        if a < nombre1SE:
            hasta = medio - 1
            print(hasta, "hastaa")
        else:
            desde = medio + 1
            print(desde, "desdeee")

        medio = (desde + hasta)//2

        print("medio:", medio)
        print("tamReg:", tamReg)

        alLocales.seek(medio*tamReg, 0)#33

        vrLoc = pickle.load(alLocales)

    if nombre1SE == a:
        return medio*tamReg
    else:
        return -1

def crearDuenios():
    os.system("cls")

    print("Creación de cuenta para dueños")

    mail = str(input("Ingrese una dirección de correo electrónico <máx. 100 caracteres>: "))
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
        regUsu.tipoUsuario = "duenioDeLocal"
        formatearUsuario(regUsu)# es para que todos los registros tengan las mismas longitudes en todos los campos, por tanto todos tendran el mismo peso
        pickle.dump(regUsu, alUsuarios)
        alUsuarios.flush()
        print("Usuario tipo duenio creado exitosamente")# estaria bueno poner una validacion corte ingrese de nuevo su contraseña para confirmar
    else:
        print("El usuario ya existe. Volviendo...") 

    os.system("pause")
#--------------------------------------------------------------------------------------------------------------------------------------------#
def pantalladueño():
    print("""
    	-----MENU PRINCIPAL-----

       1. Crear descuento 
       2. Reporte de uso de descuentos 
       3. Ver novedades 
       0. Salir  """)

#-----------------ADMINISTRADOR-----------------------------------------------------------------------------------------------------------#
def administrador():
    opc = -1
    while opc != 0:
        menuAdministrador()
        opc = input("Ingrese una opción [1-5]: ")
        while validaRangoEnteros(opc, 0, 5):
            opc = input(Fore.RED + "Incorrecto - Ingrese una opción [1-5]: " + Fore.RESET)
        opc = int(opc)
        if opc == 1:
            while opc != 0:
                menuGestionDeLocales()
                opc = input("Ingrese una opción [1-5]: ")
                while validaRangoEnteros(opc, 1, 5):
                    opc = input(Fore.RED + "Incorrecto - Ingrese una opción [1-5]: " + Fore.RESET)
                opc = int(opc)
                if opc == 1:
                    print("crear locales")
                    creacionDeLocales()
                    # mostrartodos
                elif opc == 2:
                    print("modificar local")
                elif opc == 3:
                    print("eliminar local")
                elif opc == 4:
                    print("Mapa locales")
                elif opc == 5:
                    print("volver")
        elif opc == 2:
            crearDuenios()
        elif opc == 3:
            print("3")
        elif opc == 4:
            print("4")
        elif opc == 5:
            print("5")
        elif opc == 0:
            print("salir")

def buscaSecCod(a):
    global afUsuarios, alUsuarios

    t = os.path.getsize(afUsuarios)
    alUsuarios.seek(0)  
    print(t, "tttttttttttttt")
    while alUsuarios.tell()<t:
        pos = alUsuarios.tell()
        vrTemp = pickle.load(alUsuarios)# traigo a memoria el registro del usuario

        codigo = vrTemp.codUsuario #guardo en una variable el codigo del usuario del 1er registro

        tipoUser = vrTemp.tipoUsuario #guardo de una variable el tipo de usuario del 1er registro
        tipoUserSE = tipoUser.strip() # ahora sin espacios

        print(codigo, a, "acaaaaaaaaaa")
        if int(codigo) == int(a) and tipoUserSE == "duenioDeLocal": # si el codigo coincide con el ingresado y si ademas el codigo pertenece a un dueño de local, retorna la posicion
            return pos
    return -1

def creacionDeLocales():
    global alLocales, afLocales
    print("-----------------------------------------")
    print("|        CREACION LOCALES               |")
    print("-----------------------------------------")

    nombreLocal = str(input("Ingrese el nombre del local <máx. 50 caracteres>. "))
    while len(nombreLocal)< 1 and len(nombreLocal) > 50:
        nombreLocal = input("Incorrecto! su correo electrónico debe tener hasta 50 caracteres. ")

    while nombreLocal != "0":

        t = os.path.getsize(afLocales)
    

        if t > 0:# si el archivo no cuenta con ningun registro, no hace el ordenamiento
            ordenamiento()
            busquedaDicotomica(nombreLocal) # realiza la busqueda dicotomica para ver si existe o no
        
            while busquedaDicotomica(nombreLocal) != -1:
                nombreLocal = input("Incorrecto! el nombre del Local ya existe. Intente nuevamente ")
                if nombreLocal == "0":
                    return "saliendo.." #faltaria el listado
                ordenamiento()
                busquedaDicotomica(nombreLocal)

        codUsuario = str(input("Ingrese suuuu codigo de usuario: "))
        
        pos = buscaSecCod(codUsuario)
        print(pos)
        while pos != -1:#verificar mediante una busqueda si el codigo del usuario corresponde a un dueño de local

            ubiLocal = str(input("Ingrese la ubi del local <máx. 50 caracteres>. "))

            while len(ubiLocal)< 1 and len(ubiLocal) > 50:
                ubiLocal = input("Incorrecto! su ubicacion debe tener hasta 50 caracteres. ")

            rubroLocal = str(input("Ingrese el rubro del local <indumentaria, perfumeria o comida>:  "))

            while len(rubroLocal)< 1 and len(rubroLocal) > 50:
                rubroLocal = input("Incorrecto! su correo electrónico debe tener hasta 50 caracteres:  ")

            regLoc = locales()
            regLoc.nombreLocal = nombreLocal
            regLoc.ubicLocal = ubiLocal
            regLoc.rubroLocal = rubroLocal
            regLoc.codUsuario = codUsuario
            regLoc.codLocal = codLocal() + 1
            regLoc.estado = "A"
            formatearLocales(regLoc)
            pickle.dump(regLoc, alLocales)
            alLocales.flush()

            #puedo hacer un while mas grande y hacer un return con la lista de todos
        #nombreLocal = str(input("Ingrese el nombre del local <máx. 50 caracteres>. "))

   # return 1 #faltaria el listado


#---------------Programa principal---------------------------------------------------------------------------------------------------------#
afUsuarios = "C:\\ayed\\usuarios.dat" 
afLocales = "C:\\ayed\\locales.dat"
afUsoPromos = "C:\\ayed\\uso_promociones.dat"
afPromociones = "C:\\ayed\\promociones.dat"




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

if os.path.exists(afLocales): #Inicializo el registro locales
    alLocales = open (afLocales, "r+b")
else:
    alLocales = open (afLocales, "w+b")
if os.path.exists(afUsoPromos): #Inicializo el registro uso_promociones
    alUsoPromos = open (afUsoPromos, "r+b")
else:
    alUsoPromos = open (afUsoPromos, "w+b")
if os.path.exists(afPromociones): #Inicializo el registro promociones
    alPromociones = open (afPromociones, "r+b")
else:
    alPromociones= open (afPromociones, "w+b")

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
            administrador()
        elif tipoUseraSE == "cliente":
            menuCliente()
        elif tipoUseraSE == "dueñoDeLocal":
            menuDuenoDeLocal()
    elif opc == 2:
        crearUsuariosTipoCliente()
    elif opc == 3:
        print("\n\nGracias por visitarnos ...\n\n")




alUsuarios.close()
alLocales.close()
alPromociones.close()
alUsoPromos.close()