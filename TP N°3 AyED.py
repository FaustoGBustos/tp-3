#TP N°3 ALgoritmos y estructuras de datos
# Fausto Bustos, Santiago Gerez, Fernando Pellegrini y Lara Varrenti
import textwrap                   #acorta el texto para que entre en una columna
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
cantuso = 0

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
        self.diasSemana = [0]*7
        self.estado = ""
        self.codLocal = 0


class uso_promociones:
    def __init__(self):
        self.codCliente = 0
        self.codPromo = 0
        self.fechaUsoPromo = None

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
    rLoc.codLocal = rLoc.codLocal.ljust(10, ' ')
    rLoc.codUsuario = str(rLoc.codUsuario)
    rLoc.codUsuario = rLoc.codUsuario.ljust(10, ' ')

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

def codUser():
    alUsuarios.seek(0) # me posiciono en el primer registro
    aux = pickle.load(alUsuarios) # lo traigo a memoria
    tamReg = alUsuarios.tell() # obtengo el peso en bytes del registro(todos pesan lo mismo)
    
    alUsuarios.seek(-tamReg, 2) # me posiciono en el final, y me muevo hacia atras un registro(tamreg)
    aux = pickle.load(alUsuarios)# traigo a memoria el ultimo registro cargado
    cod = aux.codUsuario # obtengo el codigo del ultimo registro cargado
    return int(cod) # lo devuelvo para luego ir aumentando uno en uno cada vez que se cree uno nuevo

def codLocal():
    global afLocales, alLocales
    t = os.path.getsize(afLocales)
    alLocales.seek(0)
    max = 0

    while alLocales.tell()<t:
        vrTemp = pickle.load(alLocales)
        vrTempsinesp = vrTemp.codLocal #Esto lo hago porque debido al formateo uno tiene espacios y el otro no, entonces para que la comparacion funcione, le saco los espacios
        vrTempor = int(vrTempsinesp)
        if (vrTempor) > max:
            max = vrTempor
    return max + 1

def codPromo():
    global afPromociones, alPromociones
    t = os.path.getsize(afPromociones)
    alPromociones.seek(0)
    max = 0

    while alPromociones.tell()<t:
        vrTemp = pickle.load(alPromociones)
        vrTempsinesp = vrTemp.codPromo #Esto lo hago porque debido al formateo uno tiene espacios y el otro no, entonces para que la comparacion funcione, le saco los espacios
        vrTempor = int(vrTempsinesp)
        if (vrTempor) > max:
            max = vrTempor
    return max + 1
#------------------------------------------------------------------------------------------------------------------------------------------#
def ingresoUsuarios(): # recordar INACTIVOS
    global codCurrentUser
    mail = str(input("\nIngrese su nombre de usuario: "))
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
        mail = str(input("ingrese su nombre de usuario: "))
        pos = buscaSec(mail)
        if pos != -1:

            #nos posicionamos ahi
            alUsuarios.seek(pos, 0)
            #traemos a memoria el registro
            aux = pickle.load(alUsuarios)
            
            #de ese registro obtenemos la clave, y le sacamos los espacios para luego ver si coinciden con el usuario
            clave = aux.claveUsuario
            claveSinEspacios = clave.strip()

        contra = pwinput.pwinput("Ingrese una contraseña correcta: ")
        pos = buscaSec(mail)
        error += 1
        if error == 2:
            return "intentos maximos alcanzados"
        
    codCurrentUser = aux.codUsuario.strip()
    #es para luego obtener el codigo del dueño de local
    tipoyCod = [aux.tipoUsuario.strip(), aux.codUsuario.strip()]  
    # devuelve que tipo de usuario es para devolverle el menu correspondiente

    return tipoyCod

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
    os.system("cls")
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
    os.system("cls")
    menu_gestion_locales = """
    *******************************************
    *         1-GESTIÓN DE LOCALES               *
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
   
def menuDuenioDeLocal():
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
    auxi = pickle.load(alLocales)
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
    try:
        alLocales.seek(0, 0)
        vrLoc = pickle.load(alLocales)

        tamReg = alLocales.tell()
        tamArch = os.path.getsize(afLocales)
        cantReg = tamArch // tamReg

        desde = 0
        hasta = cantReg - 1
        medio = (desde + hasta)//2

        alLocales.seek(medio*tamReg, 0)#2

        #sin espacios para comparar bien
        # SE = Sin Espacios
        vrLoc = pickle.load(alLocales)

        while vrLoc.nombreLocal!= a and desde < hasta:

            if a < vrLoc.nombreLocal:
                hasta = medio - 1
            else:
                desde = medio + 1

            medio = (desde + hasta)//2

            alLocales.seek(medio*tamReg, 0)#33

            vrLoc = pickle.load(alLocales)

        if vrLoc.nombreLocal == a:
            return medio*tamReg
        else:
            return -1
    except OSError:
        return -1

def crearDuenios():
    os.system("cls")

    title = "Crear cuentas de dueños de locales"
    width = len(title) + 4
    border = "*" * width

    print("\n" + border)
    print(f"*  {title}  *")
    print(border + "\n")

    mail = input("Ingrese una dirección de correo electrónico <máx. 100 caracteres>, o ingrese '*' para salir: ")
    
    while mail != '*' and (len(mail) < 1 or len(mail) > 100):
        mail = input("Incorrecto! Su correo electrónico debe tener hasta 100 caracteres o ingrese '*' para salir: ")

    if mail != '*':
        regUsu = usuarios()
        if buscaSec(mail) == -1:
            regUsu.nombreUsuario = mail
            contra = pwinput.pwinput("Ingrese una contraseña. Debe tener exactamente 8 caracteres ")
            while len(contra) != 8:
                contra = pwinput.pwinput("Incorrecto! Su contraseña debe tener 8 caracteres. ")
            regUsu.claveUsuario = contra
            regUsu.codUsuario = codUser() + 1
            regUsu.tipoUsuario = "duenioDeLocal"
            formatearUsuario(regUsu)
            pickle.dump(regUsu, alUsuarios)
            alUsuarios.flush()
            print(Fore.GREEN + "\nUsuario tipo dueño creado exitosamente" + Fore.RESET)
        else:
            print(Fore.RED + "El usuario ya existe. Volviendo..." + Fore.RESET + "\n")
    
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
            while opc != 5:
                menuGestionDeLocales()
                opc = input("Ingrese una opción [1-5]: ")
                while validaRangoEnteros(opc, 1, 5):
                    opc = input(Fore.RED + "Incorrecto - Ingrese una opción [1-5]: " + Fore.RESET)
                opc = int(opc)
                if opc == 1:
                    creacionDeLocales()
                    os.system("pause")
                elif opc == 2:
                    modificacionDeLocales()
                    os.system("pause")

                elif opc == 3:
                    eliminandoLocal()
                    os.system("pause")

                elif opc == 4:
                    mapaLocal()
                    os.system("pause")

                elif opc == 5:
                    print("Volviendo..")
                    os.system("pause")

        elif opc == 2:
            crearDuenios()
            os.system("pause")

        elif opc == 3:
            aprobarDenegarSolicitud()
            os.system("pause")

        elif opc == 4:
            print("En chapin..")
            os.system("pause")
        elif opc == 5:
            reporteUsoDeDtos()
            os.system("pause")

        elif opc == 0:
            print("Saliendo..")
            os.system("pause")


############ CREACION DE LOCALES ################
def buscaSecCod(a):
    global afUsuarios, alUsuarios

    t = os.path.getsize(afUsuarios)
    alUsuarios.seek(0)  

    while alUsuarios.tell()<t:
        pos = alUsuarios.tell()
        vrTemp = pickle.load(alUsuarios)# traigo a memoria el registro del usuario

        codigo = vrTemp.codUsuario #guardo en una variable el codigo del usuario del 1er registro

        tipoUser = vrTemp.tipoUsuario #guardo de una variable el tipo de usuario del 1er registro
        tipoUserSE = tipoUser.strip() # ahora sin espacios

        if int(codigo) == int(a) and tipoUserSE == "duenioDeLocal": # si el codigo coincide con el ingresado y si ademas el codigo pertenece a un dueño de local, retorna la posicion
            return pos
    return -1

def creacionDeLocales():
    global alLocales, afLocales
    os.system("cls")
    print("-----------------------------------------")
    print("|        CREACION LOCALES               |")
    print("-----------------------------------------")

    nombreLocal = str(input("Ingrese el nombre del local <máx. 50 caracteres>. "))
    while len(nombreLocal)< 1 and len(nombreLocal) > 50:
        nombreLocal = input("Incorrecto! su correo electrónico debe tener hasta 50 caracteres. ")

    while nombreLocal != "0":

        t = os.path.getsize(afLocales)
    

        if t > 0: #si el archivo no cuenta con ningun registro, no hace el ordenamiento
            ordenamiento() # esto lo puedo solucionar haciendo una busqueda secuencial para el codigo del local, que busque y solo deje el mas grande
            nombreLocalformat = str(nombreLocal).ljust(50, " ")#lo convierto a string y lo completo para que el registro siga midiendo lo mismo
            busquedaDicotomica(nombreLocalformat) # realiza la busqueda dicotomica para ver si existe o no
        
            while busquedaDicotomica(nombreLocalformat) != -1:
                nombreLocal = input(Fore.RED + "Incorrecto! El nombre del local ya existe. Intente nuevamente: " + Fore.RESET)
                ordenamiento()
                nombreLocalformat = str(nombreLocal).ljust(50, " ")#lo convierto a string y lo completo para que el registro siga midiendo lo mismo
                busquedaDicotomica(nombreLocalformat)
        
        codUsuario = (input("Ingrese su codigo de usuario: "))

        pos = buscaSecCod(codUsuario)
        while pos == -1 and int(codUsuario) != 0:
            codUsuario = input(Fore.RED + "Incorrecto. Ingrese su código de usuario. Si quiere salir presione 0: " + Fore.RESET)

            
                
        if pos != -1:#verificar mediante una busqueda si el codigo del usuario corresponde a un dueño de local

            ubiLocal = str(input("Ingrese la ubi del local <máx. 50 caracteres>. "))

            while len(ubiLocal)< 1 and len(ubiLocal) > 50:
                ubiLocal = input(Fore.RED + "Incorrecto! Su ubicación debe tener hasta 50 caracteres. " + Fore.RESET)

            rubroLocal = str(input("Ingrese el rubro del local <indumentaria, perfumeria o comida>:  "))
            rubroLocalSE = rubroLocal.strip()# SE de Sin Espacios

            while rubroLocalSE != "" and rubroLocalSE not in ["indumentaria", "perfumeria", "comida"]:

                rubroLocal = input(Fore.RED + "Incorrecto! El rubro no coincide con las opciones disponibles. Ingrese una opción correcta <indumentaria, perfumería o comida>: " + Fore.RESET)

                rubroLocalSE = rubroLocal.strip()

            regLoc = locales()
            regLoc.nombreLocal = nombreLocal
            regLoc.ubiLocal = ubiLocal
            regLoc.rubroLocal = rubroLocalSE
            regLoc.codUsuario = codUsuario
            regLoc.codLocal = codLocal()
            regLoc.estado = "A"
            formatearLocales(regLoc)
            pickle.dump(regLoc, alLocales)
            alLocales.flush()
    
        nombreLocal = str(input("\nIngrese el nombre del local <máx. 50 caracteres>. Si quiere dejar de crear locales, ingrese 0: "))

            #puedo hacer un while mas grande y hacer un return con la lista de todos

    return cantDeRubros() #faltaria el listado

def ordenarRubros(rubros, tam):
    for i in range(tam - 1):
        for j in range(i + 1, tam):
            if rubros[i][1] < rubros[j][1]:
                aux = rubros[i]
                rubros[i] = rubros[j]
                rubros[j] = aux

    return rubros

def cantDeRubros():
    # maybe hacer una busqueda secuencial he ir contando los locales que hay y ponerlos en un arreglo
    global afLocales, alLocales, contadorRubro1, contadorRubro2, contadorRubro3
    t = os.path.getsize(afLocales)
    alLocales.seek(0)


    nombres_rubros = ['indumentaria', 'perfumeria', 'comida']

    contadorRubro1 = 0
    contadorRubro2 = 0
    contadorRubro3 = 0

    while alLocales.tell()<t:
        pos = alLocales.tell()
        vrTemp = pickle.load(alLocales)
        rubroLocal = vrTemp.rubroLocal
        
        if rubroLocal.strip() == nombres_rubros[0]:
            contadorRubro1 += 1
        elif rubroLocal.strip() == nombres_rubros[1].strip():
            contadorRubro2 += 1
        elif rubroLocal.strip() == nombres_rubros[2]:
            contadorRubro3 += 1

    rubros = [
        [nombres_rubros[0], contadorRubro1],
        [nombres_rubros[1], contadorRubro2],
        [nombres_rubros[2], contadorRubro3]
    ]

    rubros_ordenados = ordenarRubros(rubros, 3)
    print("\n")
    print("*" * 50)  # Línea decorativa superior
    print("Cantidad de locales por rubro:")
    print("*" * 50)  # Línea decorativa intermedia
    for rubro, cantidad in rubros_ordenados:
        print(f"{rubro.capitalize()}: {cantidad}")
    print("*" * 50)  # Línea decorativa inferior

############# MODIFICAR LOCALES ##############
def buscaSecCodLocal(a):
    global afLocales, alLocales

    t = os.path.getsize(afLocales)
    alLocales.seek(0)  

    while alLocales.tell()<t:
        pos = alLocales.tell() # guardo la posicion antes de que avance (el load hace que avance al principio del registro siguiente al que estaba)
        vrTemp = pickle.load(alLocales)# traigo a memoria el registro del usuario

        if int(vrTemp.codLocal) == int(a):# si el codigo coincide con el ingresado retorna la posicion
            return pos
    return -1

def mostrarLocal(a):
    print("Nombre del local:", a.nombreLocal)
    print("Ubicación del local:", a.ubiLocal)
    print("Rubro del local:", a.rubroLocal)
    print("Estado del local:", a.estado)
    print("codigo del local:", a.codLocal)
    print("codigo del user:", a.codUsuario)
    
def modificacionDeLocales():
    os.system('cls')
    global alLocales, afLocales
    print("---------------------------------------------")
    print("|        MODIFICACION LOCALES               |")
    print("---------------------------------------------")
    local = locales()

    t = os.path.getsize(afLocales)# medimos el archivo para ver si esta vacio 

    if t == 0:# si el archivo esta vacio, o sea tiene tamaño 0, el sistema avisa
        print("No hay locales cargados todavia")
        os.system('pause')
    else:
        codigoLocal = (input("Ingrese el codigo del local que quiere modificar. Con 0 sale de la opcion de modificar locales: "))

        codigoLocal = int(codigoLocal)

        while codigoLocal != 0:
            pos = buscaSecCodLocal(codigoLocal)

            if pos == -1:
                print ("El local no existe")

            else:
                local = locales()
                alLocales.seek(pos, 0)
                local = pickle.load(alLocales)

                if local.estado == "B":
                    print("El local esta dado de baja")
                else:
                    print("\nLocal a modificar: ")
                    mostrarLocal(local)
                    
                    print("\n-Actualice los campos")
                    nombreLocal = str(input("\nIngrese el nombre del local <máx. 50 caracteres>. "))
                    while len(nombreLocal)< 1 and len(nombreLocal) > 50:
                        nombreLocal = input("Incorrecto! El nombre debe tener hasta 50 caracteres. ")

                    if nombreLocal != "0":

                        t = os.path.getsize(afLocales)
                    
                        if t > 0: #si el archivo no cuenta con ningun registro, no hace el ordenamiento
                            ordenamiento() # esto lo puedo solucionar haciendo una busqueda secuencial para el codigo del local, que busque y solo deje el mas grande
                            nombreLocalformat = str(nombreLocal).ljust(50, " ")#lo convierto a string y lo completo para que el registro siga midiendo lo mismo
                            busquedaDicotomica(nombreLocalformat) # realiza la busqueda dicotomica para ver si existe o no
                        
                            while busquedaDicotomica(nombreLocalformat) != -1:
                                nombreLocal = input("Incorrecto! el nombre del Local ya existe. Intente nuevamente ")
                                ordenamiento()
                                nombreLocalformat = str(nombreLocal).ljust(50, " ")#lo convierto a string y lo completo para que el registro siga midiendo lo mismo
                                busquedaDicotomica(nombreLocalformat)

                            local.nombreLocal = str(nombreLocal).ljust(50, " ")

                        codUsuario = str(input("Ingrese su codigo de usuario: "))
                        
                        poscoduser = buscaSecCod(codUsuario)

                        if poscoduser != -1:#verificar mediante una busqueda si el codigo del usuario corresponde a un dueño de local

                            ubiLocal = str(input("Ingrese la ubi del local <máx. 50 caracteres>. "))

                            while len(ubiLocal)< 1 and len(ubiLocal) > 50:
                                ubiLocal = input("Incorrecto! su ubicacion debe tener hasta 50 caracteres. ")

                            local.ubiLocal = str(ubiLocal).ljust(50, " ")

                            rubroLocal = str(input("Ingrese el rubro del local <indumentaria, perfumeria o comida>:  "))
                            rubroLocalSE = rubroLocal.strip()# SE de Sin Espacios


                            while (rubroLocalSE != "") and (rubroLocalSE not in ["indumentaria", "perfumeria", "comida"]):

                                rubroLocal = input("Incorrecto! el rubro no coincide con las opciones disponibles. Ingrese una opcion correcta <indumentaria, perfumeria o comida>: ")
                                rubroLocalSE = rubroLocal.strip()

                            local.rubroLocal = str(rubroLocalSE).ljust(50, " ")

                            rta = input("\n-¿Confirma la modificacion? (Si o no): ")
                            rta = rta.strip()

                            while rta.lower() != "si" and rta.lower() != "no":
                                rta = input("Incorrecto. ¿Confirma la modificacion? (Si o no): ")
                                rta = rta.strip()

                            if rta.lower() == "si":
                                
                                alLocales.seek(pos, 0)
                                pickle.dump(local, alLocales)
                                alLocales.flush()

                                print(Fore.GREEN + "\nModificación exitosa" + Fore.RESET)
                                print("\nLos datos actualizados son: ")
                                mostrarLocal(local)

            codigoLocal = int(input("\nIngrese el codigo del local que quiere modificar. Si no quiere seguir modificando locales, ingrese 0: "))
            codigoLocal = int(codigoLocal)         

#=============== BAJA DE LOCALES ==========================

def eliminandoLocal():
    global afLocales, alLocales
    os.system("cls")

    print("+-------------------------------------------+")
    print("|         ELIMINAR LOCAL                   |")
    print("+-------------------------------------------+")

    t = os.path.getsize(afLocales)

    if t == 0:
        print("\nNo hay archivos para eliminar")
        os.system("pause")
    else:
        codigoLocal = int(input("\nIngrese el código del local que quiere eliminar. Con 0 sale del menú: "))
        
        while codigoLocal != 0:
            pos = buscaSecCodLocal(codigoLocal)
            
            if pos == -1:
                print("El código ingresado no existe")
            else:
                local = locales()
                alLocales.seek(pos, 0)
                local = pickle.load(alLocales)

                if local.estado == "B":
                    print("\nEl local ya está dado de baja")
                else:
                    print("\nDatos del local a eliminar: ")
                    mostrarLocal(local)

                    rta = input("¿Confirma la eliminación? (Si o no): ")
                    rta = rta.strip()

                    while rta.lower() != "si" and rta.lower() != "no":
                        rta = input("Incorrecto. ¿Confirma la eliminación? (Si o no): ")
                        rta = rta.strip()

                    if rta.lower() == "si":
                        local.estado = "B"
                        alLocales.seek(pos)
                        pickle.dump(local, alLocales)
                        alLocales.flush()

                        print(Fore.GREEN + "\nEliminación exitosa" + Fore.RESET)

                        print("\nLos datos actualizados son: ")
                        mostrarLocal(local)

            codigoLocal = int(input("\nIngrese el código del local que quiere eliminar. Con 0 sale del menú: "))

#================ MAPA DE LOCALES ===============

def mapaLocal():
    global afLocales, alLocales
    os.system("cls")

    print("+-------------------------------------------+")
    print("|          MAPA DE LOCALES                 |")
    print("+-------------------------------------------+")

    t = os.path.getsize(afLocales)

    if t> 0:
        ordenamiento()

        alLocales.seek(0)
        codigos_locales = []
        i = 0
        while alLocales.tell() < t and i < 50:
            vrTemp = pickle.load(alLocales)
            codigos_locales.append(vrTemp.codLocal.strip())  # Elimina espacios en blanco
            i += 1

        # Crear un arreglo nuevo con los locales ordenados alfabéticamente por su nombre
        localesordenadosalfabeticamente = list(codigos_locales)  # Guarda una copia de la lista

        # Inicializar una lista de códigos de locales
        codigos_locales = [0] * 50

        # Iterar sobre la matriz y obtener los códigos de la primera columna
        for i in range(50):
            # Se nos pide que en los lugares no ocupados esté el número 0
            if i >= len(localesordenadosalfabeticamente) or localesordenadosalfabeticamente[i] == "":
                codigoint = 0
            else:
                codigoint = int(localesordenadosalfabeticamente[i])
            codigos_locales[i] = codigoint

        # Crear el mapa a partir de las condiciones dadas
        filas = 10
        columnas = 5

        # Crear la cuadrícula utilizando un bucle for
        for i in range(filas):
            print("+--+--+--+--+--+")
            for j in range(columnas):
                # Calcular el índice adecuado en base a la fila y columna actual
                index = i * columnas + j
                # Convertir en cadena y dar formato al número
                num_str = str(codigos_locales[index])
                # Agregar espacio si el número tiene solo un dígito
                if len(num_str) == 1:
                    num_str = " " + num_str
                print(f"|{num_str}", end="")
            print("|")

        print("+--+--+--+--+--+")
    else:
        print(Fore.RED + "\nNo hay locales registrados todavía." + Fore.RESET)

#================== DUEÑO DE LOCALES ======================
def duenioDeLocal():
    os.system("cls")
    menuDuenioDeLocal()
    opc = str(input("Opción? <0-3>: "))
    while opc < "0" or opc > "3":
        opc = str(input("Incorrecto!: Opción? <0-3>: "))
    while opc > "0" and opc <= "3":
        match opc:
            case "1": CrearPromos()
            case "2": Reporte()
            case "3": pantallachapin()
        os.system("cls")
        menuDuenioDeLocal()
        opc = str(input("Opción? <0-3>: "))
        while opc < "0" or opc > "3":
            opc = str(input("Incorrecto!: Opción? <0-3>: "))

#================== CREAR PROMOS ========================
def CrearPromos():
    global alLocales, alPromociones
    os.system("cls")


    titulo_crear_descuento = """
    *******************************************
    *           CREAR DESCUENTO               *
    *******************************************
    """

    print(titulo_crear_descuento)
    rlp = promociones()
    
    
    mostrarpromos2()
    codigo = input("\nIngrese el codigo del local al que le creará la promoción: ")
    pos = buscaSecCodLocal(codigo)

    while pos == -1 and int(codigo) !=0:
        codigo = input("Incorrecto! Ingrese un codigo de local existente.\n")
        pos = buscaSecCodLocal(codigo)

    if pos != -1:

        rlp.textoPromo = input("\nIngrese la descripción de la promocion: \n")


        band = True

        while band: # valida el ingreso de fechas


            rlp.fechaDesdePromo = input("Ingresa la fecha de inicio de la promoción (año-mes-día): ")


            try:
                rlp.fechaDesdePromo = datetime.strptime(rlp.fechaDesdePromo, "%Y-%m-%d").date()
                band = False


            except ValueError:
                print("La fecha ingresada no tiene el formato correcto (año-mes-día).")


        band = True
        while band: # valida el ingreso de fechas
            rlp.fechaHastaPromo = input("Ingresa la fecha de finalizacion de la promoción (año-mes-día): ")


            try:
                rlp.fechaHastaPromo = datetime.strptime(rlp.fechaHastaPromo, "%Y-%m-%d").date()
                band = False

            except ValueError:
                print("La fecha ingresada no tiene el formato correcto (año-mes-día).")


        dias_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        print("Ingrese un 1 si la oferta es valida ese día y un 0 si no lo es. ")


        for i in range (7):
            rlp.diasSemana[i] = input(dias_semana[i] + ": ")


        rlp.estado = "pendiente"
        print("El estado de su nueva promoción será pendiente hasta que esta sea aprobada.")
        rlp.codUsuario = codCurrentUser
        rlp.codLocal = codigo
        rlp.codPromo = codPromo()

        formatearpromos(rlp)

        alPromociones.seek(0,2)
        pickle.dump(rlp, alPromociones)

        print("---------------------------")
        print("Promoción cargada con éxito")
        print("---------------------------")
        alPromociones.flush()

        os.system("pause")

def mostrarpromos2():
        rll = locales()
        rlp = promociones()
        pos = buscaSecDue2(codCurrentUser,0) # busco si el dueño tiene locales/en q posición (¡¡codigo_usu_duenio tiene que guardarse al iniciar sesion!!)
        alLocales.seek(pos,0)          # paro el puntero en la posición del codigo del local (en archivo locales)
        rll = pickle.load(alLocales)   # traigo archivo a memoria
        hola = str(rll.estado)
        if str(rll.estado) == "A": # si el local esta activo, muestra.
            pospromo = buscaSecLoc2(rll.codLocal, 0) # busco promociones que pertenecen al local señalado
            tamañoprom = os.path.getsize(afPromociones)
            while int(pospromo) != (-1) and alPromociones.tell()<tamañoprom: # itera mostrando todas las promos
                alPromociones.seek(pospromo,0)  # paro el puntero en la promocion
                rlp = pickle.load(alPromociones)  # traigo archivo a memoria
                print(f"{Fore.BLUE}Promo n° {int(rlp.codPromo)}:{Fore.RESET} {(rlp.textoPromo).strip()}. {Fore.BLUE}Estado:{Fore.RESET} {rlp.estado} {Fore.BLUE}Cod. Local:{Fore.RESET} {rlp.codLocal}")                
                
                saltosA = alPromociones.tell()
                pospromo = buscaSecLoc2(rll.codLocal,saltosA)

def buscaSecLoc2(cod_loc, p):
    global afPromociones, alPromociones
    t = os.path.getsize(afPromociones) #asigno a t el tamaño del archivo

    alPromociones.seek(0)
    try: 
        rlp = pickle.load(alPromociones) #si lo intercambio de lugar con alpromociones.seek se rompe pospromo
        
        alPromociones.seek(p, 0) #posiciono el puntero al inicio

        if t>0: #si el tamaño es 0 el arcihvo esta vacio
            r = alPromociones.tell()
            while (alPromociones.tell()<=t): 
                h = rlp.codLocal
                if int(rlp.codLocal) == int(cod_loc):        
                    pos = alPromociones.tell()
                    return pos
                else:
                    rlp = pickle.load(alPromociones)
        else:
            print('-----------------')
            print("Archivo sin datos")
            print('-----------------')
            input()
    except EOFError:
        return -1

def buscaSecDue2(cod_due,p):
    global afLocales, alLocales
    rll = locales()
    alLocales.seek(0)
    try:
        t = os.path.getsize(afLocales) #asigno a t el tamaño del archivo
        
        rll = pickle.load(alLocales) #cargo primer registro
        
        alLocales.seek(p, 0) #posiciono el puntero al inicio


        pi = alLocales.tell()

        while t>0: #si el tamaño es 0 el arcihvo esta vacio
            try: 
                pi2 = alLocales.tell()

                while (alLocales.tell()<t):

                    if int(rll.codUsuario) == int(cod_due):        
                        pos = alLocales.tell()
                        return pos
                    
                    rll= pickle.load(alLocales)
                return -1
            except EOFError:
                return -1
    except EOFError:
        return -1

#===============REPORTE DE USO DE DTOS =============#
def cant(cod):
    global alUsoPromos
    rlup = uso_promociones()
    rll = promociones()
    alUsoPromos.seek(0,0)
    t = os.path.getsize(afUsoPromos)
    cont = 0 
    if t == 0:
        cont = 0
    else:
        while alUsoPromos < t:
            rlup = pickle.load(alUsoPromos)
            if int(rlup.codPromo) == int(cod):
                cont = cont + 1
    return cont

def Reporte():
    global codCurrentUser
    rlu = usuarios() # registro logico usuarios 
    rlup = uso_promociones()  
    rlp = promociones() 
    rll = locales()  
    os.system("cls")
    print("Ingrese el rango de fechas para ver las promociones válidas.")
    fecha_desde = input("Ingrese la fecha desde <año-mes-día>: ")
    fecha_hasta =input("Ingrese la fecha hasta <año-mes-día>: ")
    fecha_desde = datetime.strptime(fecha_desde, "%Y-%m-%d").date()
    fecha_hasta = datetime.strptime(fecha_hasta, "%Y-%m-%d").date()
    
    pos = buscaSecDue2(codCurrentUser, 0) #busco si el dueño tiene locales/en q posicion (¡¡codigo_usu_duenio tiene que guardarse al iniciar sesion!!)
    while int(pos) != (-1):  #itera mostrando todos los locales
        rll = pickle.load(alLocales)   #traigo archivo a memoria
        alLocales.seek(pos,0)          #paro el puntero en la posición del codigo del local (en archivo locales)
        

        
        pospromo = buscaSecLoc2(int(rll.codLocal),0) # busco promociones que pertenecen al local señalado
        if int(pospromo) != -1: #muestro el encabezado del reporte
            print("Local N° " + rll.codLocal + ": " + rll.nombreLocal)
            print("Fecha desde: " , rlp.fechaDesdePromo , "     Fecha hasta: " , rlp.fechaHastaPromo)
            linea = "+----------------------------------------------------------------------------+"
            print(linea)
            print("|Codigo promo|        Texto         | Fecha desde | Fecha hasta |Cant. de uso|")
            print(linea)

        while pospromo != (-1): #itera mostrando todas las promos

            rlp = pickle.load(alPromociones)    #traigo archivo a memoria
            alPromociones.seek(pospromo,0)  # paro el puntero en la promocion



            if (str(rlp.estado) == "aprobado") and (fecha_desde >= rlp.fechaDesdePromo) and (fecha_hasta <= rlp.fechaHastaPromo):     
                formato = "| {:<10} | {:<20} | {:<11} | {:<11} | {:<10} |"  # Formato con columnas de longitud fija           
                lineas_texto = textwrap.wrap(rlp.textoPromo, width=20) # Divide el texto en líneas más cortas para ajustarse a la columna
                codigo_promo = rlp.codPromo
                linea_texto = rlp.textoPromo
                fecha_desde = rlp.fechaDesdePromo
                fecha_hasta = rlp.fechaHastaPromo
                cantidad = cant(codigo_promo)
                # Imprime los datos con el formato 
                for linea_texto in lineas_texto:
                    print(formato.format(codigo_promo, linea_texto, fecha_desde, fecha_hasta, cantidad))
                    codigo_promo = ""
                    fecha_desde = ""
                    fecha_hasta = ""
                    cantidad_de_uso = ""
                print(linea)
                os.system("pause")
            saltos = pospromo
            pospromo = buscaSecLoc2(rll.codLocal,saltos) # el segundo parametro es para que comience a buscar desde la posición donde encontro la primer promo
        
        
        saltosB = pos
        pos = buscaSecDue2(codCurrentUser, saltosB) # el segundo parametro es para que comience a buscar desde la posición donde encontro el primer local

def validarcod(cod):
    rll = locales()
    alLocales.seek(0,0) 
    t = os.path.getsize(afLocales)
    rll = pickle.load(alLocales)
    while alLocales.tell() < t and int(rll.codLocal) != int(cod):  
        if int(rll.codLocal) == int(cod) and rll.estado == "A": # valido que existe y esta activo
            pos = alLocales.tell()
        else:
            pos = -1 
        rll = pickle.load(alLocales)  
    return pos

#===============MENUES DUEÑO DE LOCALES========================#
def pantallachapin():
    os.system("cls")
    print("-----------------------")
    print("  Resuelto en chapin   ")
    print("-----------------------")
    os.system("pause")

def pantalladueño():
    print("""
    	-----MENU PRINCIPAL-----

       1. Crear descuento 
       2. Reporte de uso de descuentos 
       3. Ver novedades 
       0. Salir  """)
#=============================================#

#=============FORMATEO PROMOS=================#
def formatearpromos(rlp):
    rlp.codPromo = str(rlp.codPromo)
    rlp.codPromo = rlp.codPromo.ljust(10, ' ')
    rlp.textoPromo = str(rlp.textoPromo)
    rlp.textoPromo = rlp.textoPromo.ljust(200, ' ')
    rlp.fechaDesdePromo = str(rlp.fechaDesdePromo)
    rlp.fechaDesdePromo = rlp.fechaDesdePromo.ljust(15,' ')
    rlp.fechaHastaPromo = str(rlp.fechaHastaPromo)
    rlp.fechaHastaPromo = rlp.fechaHastaPromo.ljust(15,' ')
    rlp.estado = str(rlp.estado)
    rlp.estado = rlp.estado.ljust(10, ' ')
    for i in range (6):
        rlp.diasSemana[i] = str(rlp.diasSemana[i])
        rlp.diasSemana[i] = rlp.diasSemana[i].ljust(1, ' ') # no se si justificarlo porque tiene un solo digito

#==========PUNTO 3 =======================#
def mostrar_promocion(promocion):
    salida = ''
    salida = salida + '{:<10}'.format(str(promocion.codPromo))
    salida = salida + '{:<200}'.format(promocion.textoPromo.strip())
    salida = salida + '{:<20}'.format(str(promocion.fechaDesdePromo))
    salida = salida + '{:<20}'.format(str(promocion.fechaHastaPromo))
    salida = salida + '{:<20}'.format(', '.join(map(str, promocion.diasSemana)))
    salida = salida + '{:<10}'.format(promocion.estado.strip())
    salida = salida + '{:<10}'.format(str(promocion.codLocal))
    
    print(salida)

def mostrarPromosPendientes():
    global afPromociones, alPromociones
    cont = 0
    t = os.path.getsize(afPromociones)
    if t == 0:
        print("No hay promociones registradas todavia")
    else:
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        encabezado = ''
        encabezado = encabezado + '{:<10}'.format("Código Promo|")
        encabezado = encabezado + '{:<200}'.format("Texto de Promoción")
        encabezado = encabezado + '{:<20}'.format("Fecha Desde")
        encabezado = encabezado + '{:<20}'.format("Fecha Hasta")
        encabezado = encabezado + '{:<20}'.format("Días de la Semana")
        encabezado = encabezado + '{:<10}'.format("Estado")
        encabezado = encabezado + '{:<10}'.format("Código Local")
        print(encabezado)
        print("------------------------------------------------------------------------------------------------------------------------------------------------------------")
        promo = promociones()
        alPromociones.seek(0)

        while alPromociones.tell()<t:
            promo = pickle.load(alPromociones)
            
            if (promo.estado).strip() == "pendiente":
                mostrar_promocion(promo)
                cont = 1
        
        if cont == 0:
            print(Fore.RED + "NO hay ninguna promoción pendiente" + Fore.RESET)
            
def buscaSecCodPromo(a):
    global afPromociones, alPromociones

    t = os.path.getsize(afPromociones)
    alPromociones.seek(0)  

    while alPromociones.tell()<t:
        pos = alPromociones.tell() # guardo la posicion antes de que avance (el load hace que avance al principio del registro siguiente al que estaba)
        vrTemp = pickle.load(alPromociones)# traigo a memoria el registro del usuario

        if int(vrTemp.codLocal) == int(a) and (vrTemp.estado).strip() == "pendiente":# si el codigo coincide con el ingresado retorna la posicion
            return pos
    return -1

def aprobarDenegarSolicitud():
    global afPromociones, alPromociones

    os.system("cls")
    print("="*50)
    print("{:^50}".format("Aprobar o Denegar Solicitudes"))
    print("="*50)

    mostrarPromosPendientes()

    promo = promociones()

    t = os.path.getsize(afPromociones)# medimos el archivo para ver si esta vacio 

    if t != 0:# si el archivo esta vacio, o sea tiene tamaño 0, el sistema avisa

        codigoPromo = (input("\nIngrese el codigo de la promocion que quiera aceptar. Con 0 sale del menu: "))

        codigoPromo = int(codigoPromo)

        while codigoPromo != 0:
            pos = buscaSecCodPromo(codigoPromo)

            if pos == -1:
                print ("La promocion no existe en pendientes")

            else:

                promo = promociones()
                alPromociones.seek(pos, 0)
                promo = pickle.load(alPromociones)


                rta = input("¿Confirma la modificacion? (Si o no): ")
                rta = rta.strip()

                while rta.lower() != "si" and rta.lower() != "no":
                    rta = input("Incorrecto. ¿Confirma la modificacion? (Si o no): ")
                    rta = rta.strip()

                if rta.lower() == "si":

                    promo.estado = str("aprobado").ljust(10, " ")

                    alPromociones.seek(pos, 0)

                    pickle.dump(promo, alPromociones)

                    alPromociones.flush()

                    print("Aprobacion exitosa")
                    mostrar_promocion(promo)
                
                        

            codigoPromo = int(input("Ingrese el codigo de la promocion que quiere aceptar. Ingrese 0 para volver: "))
            codigoPromo = int(codigoPromo)
    else:
        print("Archivo de promociones aun vacio")
#=====================PUNTO 5 ==================
def reporteUsoDeDtos():
    global afPromociones, alPromociones, cantuso, afUsoPromos, alUsoPromos
    cantuso = 0
    os.system("cls")

    print("+-------------------------------------------+")
    print("|  Reporte de Utilización de Descuentos    |")
    print("+-------------------------------------------+")

    print("Ingrese el rango de fechas para ver las promociones válidas.")
    fecha_desde = input("Ingrese la fecha desde <año-mes-día>: ")
    fecha_hasta =input("Ingrese la fecha hasta <año-mes-día>: ")
    fecha_desde = datetime.strptime(fecha_desde, "%Y-%m-%d").date()
    fecha_hasta = datetime.strptime(fecha_hasta, "%Y-%m-%d").date()

    cont = 0
    t = os.path.getsize(afPromociones)
    if t == 0:
        print("\nNo hay promociones registradas todavia")
    else:
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        encabezado = ''
        encabezado = encabezado + '{:<10}'.format("Código Promo|")
        encabezado = encabezado + '{:<200}'.format("Texto de Promoción")
        encabezado = encabezado + '{:<20}'.format("Fecha Desde")
        encabezado = encabezado + '{:<20}'.format("Fecha Hasta")
        encabezado = encabezado + '{:<20}'.format("Días de la Semana")
        encabezado = encabezado + '{:<10}'.format("Estado")
        encabezado = encabezado + '{:<10}'.format("Código Local")
        encabezado = encabezado + '{:<50}'.format("Cant. de Uso")
        print(encabezado)
        print("------------------------------------------------------------------------------------------------------------------------------------------------------------")
        promo = promociones()
        alPromociones.seek(0)

        while alPromociones.tell()<t:
            promo = pickle.load(alPromociones)
            fecha_desde_promo = datetime.strptime((promo.fechaDesdePromo).strip(), "%Y-%m-%d").date()
            fecha_hasta_promo = datetime.strptime((promo.fechaHastaPromo).strip(), "%Y-%m-%d").date()

            if (promo.estado).strip() == "aprobado" and (fecha_desde_promo>= fecha_desde) and ( fecha_hasta_promo <= fecha_hasta):
                cont = 1

                teta = os.path.getsize(afUsoPromos)
                alUsoPromos.seek(0)  

                while alUsoPromos.tell()<teta:
                    vrTemp = pickle.load(alUsoPromos)# traigo a memoria el registro del usuario

                    if int(vrTemp.codPromo) == int(promo.codPromo) and fecha_desde_promo <= vrTemp.fechaUsoPromo and vrTemp.fechaUsoPromo<= fecha_hasta_promo:

                        cantuso += 1 
        
                mostrar_promocion(promo)
        if cont == 0:
            print(Fore.RED + "NO hay ninguna promoción aprobada en esa fecha o simplemente no existe" + Fore.RESET)

        os.system("pause")
        
def mostrar_promocion(promocion):
    global cantuso
    salida = ''
    salida = salida + '{:<10}'.format(str(promocion.codPromo))
    salida = salida + '{:<200}'.format(promocion.textoPromo.strip())
    salida = salida + '{:<20}'.format(str(promocion.fechaDesdePromo))
    salida = salida + '{:<20}'.format(str(promocion.fechaHastaPromo))
    salida = salida + '{:<20}'.format(', '.join(map(str, promocion.diasSemana)))
    salida = salida + '{:<10}'.format(promocion.estado.strip())
    salida = salida + '{:<10}'.format(str(promocion.codLocal))
    salida = salida + '{:<10}'.format(str(cantuso))
    
    print(salida)        

def buscaSecCodPromo(a):
    global afPromociones, alPromociones

    t = os.path.getsize(afPromociones)
    alPromociones.seek(0)  

    while alPromociones.tell()<t:
        pos = alPromociones.tell() # guardo la posicion antes de que avance (el load hace que avance al principio del registro siguiente al que estaba)
        vrTemp = pickle.load(alPromociones)# traigo a memoria el registro del usuario

        if int(vrTemp.codLocal) == int(a) and (vrTemp.estado).strip() == "pendiente":# si el codigo coincide con el ingresado retorna la posicion
            return pos
    return -1

#======================CLIENTE====================#
def cliente():
    os.system("cls")
    menuCliente()
    opc = str(input("Opción? <0-3>: "))
    while opc < "0" or opc > "3":
        opc = str(input("Incorrecto!: Opción? <0-3>: "))
    while opc > "0" and opc <= "3":
        match opc:
            case "1": buscarDTOS()
            case "2": solicitarDTOS()
            case "3": pantallachapin()
        opc = str(input("Opción? <0-3>: "))
        while opc < "0" or opc > "3":
            opc = str(input("Incorrecto!: Opción? <0-3>: "))

def menu_cliente():
        print("MENU CLIENTE")
        print("1. Buscar descuentos en local")
        print("2. Solicitar descuento")
        print("3. Ver novedades")
        print("0. Salir")
#=================== BUSCAR DTO ===================
def buscarDTOS():
    global alPromociones, afPromociones, alLocales, afLocales, afUsoPromos, alUsoPromos
    os.system("cls")

    print("+-------------------------------------------+")
    print("|      Buscar Descuentos Disponibles      |")
    print("+-------------------------------------------+")


    codigoLocal = (input("\nIngrese el codigo del local que tiene promocion. Con 0 sale del menu: "))

    codigoLocal = int(codigoLocal)

    fecha_cli = input("Ingrese una fecha que cuente desde hoy en adelante <año-mes-día>: ")
    fecha_cli = datetime.strptime(fecha_cli, "%Y-%m-%d").date()

    fecha_hoy = date.today()

    cont = 0
    t = os.path.getsize(afPromociones)
    if t == 0:
        print("No hay promociones registradas todavia")
    else:
        promo = promociones()
        alPromociones.seek(0)

        while alPromociones.tell()<t:

                
            promo = pickle.load(alPromociones)

            fecha_desde_promo = datetime.strptime((promo.fechaDesdePromo).strip(), "%Y-%m-%d").date()
            fecha_hasta_promo = datetime.strptime((promo.fechaHastaPromo).strip(), "%Y-%m-%d").date()

            if (promo.estado).strip() == "aprobado" and (fecha_hasta_promo>= fecha_cli) and ( fecha_desde_promo <= fecha_cli) and fecha_cli>= fecha_hoy and int(promo.diasSemana[fecha_hoy.weekday()]) == 1 and codigoLocal == int(promo.codLocal):
                print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
                encabezado = ''
                encabezado = encabezado + '{:<10}'.format("Código Promo|")
                encabezado = encabezado + '{:<200}'.format("Texto de Promoción")
                encabezado = encabezado + '{:<20}'.format("Fecha Desde")
                encabezado = encabezado + '{:<20}'.format("Fecha Hasta")

                print(encabezado)
                print("------------------------------------------------------------------------------------------------------------------------------------------------------------")
                
                mostrarDTO(promo)
                cont = 1# bandera para saber si entro

        
        if cont == 0:
            print(Fore.RED + "NO hay ninguna promoción aprobada en esa fecha o simplemente no existe" + Fore.RESET)

def mostrarDTO(promocion):
    salida = ''
    salida = salida + '{:<10}'.format(str(promocion.codPromo))
    salida = salida + '{:<200}'.format(promocion.textoPromo.strip())
    salida = salida + '{:<20}'.format(str(promocion.fechaDesdePromo))
    salida = salida + '{:<20}'.format(str(promocion.fechaHastaPromo))
    
    print(salida)        

def buscaSecCodPromoPunto2(a):
    global afPromociones, alPromociones

    t = os.path.getsize(afPromociones)
    alPromociones.seek(0)  

    while alPromociones.tell()<t:
        pos = alPromociones.tell() # guardo la posicion antes de que avance (el load hace que avance al principio del registro siguiente al que estaba)
        vrTemp = pickle.load(alPromociones)# traigo a memoria el registro del usuario


        if int(vrTemp.codPromo) == int(a) and (vrTemp.estado).strip() == "aprobado":# si el codigo coincide con el ingresado retorna la posicion
            return pos
    return -1

#================ SOLICITAR DTO ========================
def solicitarDTOS():
    global alPromociones, afPromociones, alLocales, afLocales
    os.system("cls")


    codPromocion = (input("Ingrese el codigo de promocion que quiere usar. Con 0 sale al menu: "))

    codPromocion = int(codPromocion)

    fecha_hoy = date.today()

    cont = 0
    t = os.path.getsize(afPromociones)
    if t == 0:
        print("No hay promociones registradas todavia")
    else:
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        encabezado = ''
        encabezado = encabezado + '{:<10}'.format("Código Promo")
        encabezado = encabezado + '{:<200}'.format("Texto")
        encabezado = encabezado + '{:<20}'.format("Fecha Desde")
        encabezado = encabezado + '{:<20}'.format("Fecha Hasta")
        print(encabezado)
        print("------------------------------------------------------------------------------------------------------------------------------------------------------------")
        
        alPromociones.seek(0)

        while alPromociones.tell()<t:
            vrTemp = pickle.load(alPromociones)# traigo a memoria el registro del usuario

            fecha_desde_promo = datetime.strptime((vrTemp.fechaDesdePromo).strip(), "%Y-%m-%d").date()
            fecha_hasta_promo = datetime.strptime((vrTemp.fechaHastaPromo).strip(), "%Y-%m-%d").date()

            if (vrTemp.estado).strip() == "aprobado" and (fecha_hasta_promo>= fecha_hoy) and ( fecha_desde_promo <= fecha_hoy) and int(vrTemp.diasSemana[fecha_hoy.weekday()]) == 1 and codPromocion == int(vrTemp.codPromo):
                cont = 1

                
                regUsoPro = uso_promociones()
                alUsoPromos.seek(0)
                regUsoPro.codCliente = codCurrentUser
                regUsoPro.codPromo = codPromocion
                regUsoPro.fechaUsoPromo = fecha_hoy
                formatearUsoPromos(regUsoPro)
                pickle.dump(regUsoPro, alUsoPromos)
                alUsoPromos.flush()

                print("Descuento utilizado exitosamente")
                

                
        
        if cont == 0:
            print(Fore.RED + "NO hay ninguna promoción aprobada en esa fecha o simplemente no existe" + Fore.RESET)


def formatearUsoPromos(a):
    a.codCliente = str(a.codCliente)
    a.codCliente = a.codCliente.ljust(10, ' ')
    a.codPromo = str(a.codPromo)
    a.codPromo = a.codPromo.ljust(10, ' ')


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
    os.system('cls')
    mostrarMenu()
    opc = input("Ingrese una opción [1-3]: ")
    while validaRangoEnteros(opc, 1, 3):
        opc = input(Fore.RED + "Incorrecto - Ingrese una opción [1-3]: " + Fore.RESET)
    opc = int(opc)
    if opc == 1:
        tipoUser = ingresoUsuarios()

        if tipoUser[0] == "administrador":
            menuAdministrador()
            administrador()
        elif tipoUser[0] == "cliente":
            menuCliente()
            cliente()
        elif tipoUser[0] == "duenioDeLocal":
            os.system("pause")
            pantalladueño()
            duenioDeLocal()
    elif opc == 2:
        crearUsuariosTipoCliente()
    elif opc == 3:
        print("\n\nGracias por visitarnos ...\n\n")

alUsuarios.close()
alLocales.close()
alPromociones.close()
alUsoPromos.close()