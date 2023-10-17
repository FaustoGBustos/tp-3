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
from colorama import Back, Fore, init  #para poner colores | EJ: print(Fore.GREEN + "holis")
import time
import pwinput


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

#--------VALIDACIONES----------------------------------------------------------------------------------------------------------------------------------#
def validaChar(opc,A,B): #s,s,n
    try:
        if type(opc) == str:
            opc = opc.lower()
        if type(A) == str:
            A = A.lower()
        if type(B) == str:
            B = B.lower()

        if opc == A or opc == B:
            return False
        else:
            return True
    except:
        return True

def validaRangoEntero(nro, min,max):
    try:              
        nro = int(nro)      
        if nro >= min and nro <= max:
            return False 
        else:
            return True  
    except:
        return True   

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
    print(Fore.CYAN+"-----------------------------------------")
    print("|              REGISTRACIÓN             |")
    print("-----------------------------------------"+Fore.RESET)
    
    
    mail = str(input("Ingrese su correo electrónico para su nombre de usuario <máx. 100 caracteres>. "))
 
    while validaRangoEntero(len(mail),1,100):
        mail = input(Fore.RED+"Incorrecto! su correo electrónico debe tener hasta 100 caracteres. "+Fore.RESET)
        
    regUsu = usuarios()
    if buscaSec(mail) == -1:
        regUsu.nombreUsuario = mail
        contra = pwinput.pwinput("Ingrese una contraseña. Debe tener exactamente 8 caracteres ")
        while len(contra) != 8:
            contra = pwinput.pwinput((Fore.RED+"Incorrecto! su contraseña debe tener 8 caracteres. "+Fore.RESET))
        regUsu.claveUsuario = contra
        regUsu.codUsuario = codUser() + 1
        regUsu.tipoUsuario = "cliente"
        formatearUsuario(regUsu)# es para que todos los registros tengan las mismas longitudes en todos los campos, por tanto todos tendran el mismo peso
        pickle.dump(regUsu, alUsuarios)
        alUsuarios.flush()
        print(Fore.GREEN+"Usuario tipo cliente creado exitosamente"+Fore.RESET)# estaria bueno poner una validacion corte ingrese de nuevo su contraseña para confirmar
        time.sleep(2)
    else:
        print(Fore.YELLOW+"El usuario ya existe."+Fore.RESET) 
        time.sleep(2)

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
    
    print(Fore.CYAN+"-----------------------------------------")
    print("|           INICIO DE SESIÓN            |")
    print("-----------------------------------------"+Fore.RESET)
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

        print(Fore.RED+"El usuario y la contraseña no concide. Recuerden que son 3 intentos como maximo"+Fore.RESET)
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
            return (Fore.RED+"intentos maximos alcanzados"+Fore.RESET)
        
    codCurrentUser = aux.codUsuario.strip()
    #es para luego obtener el codigo del dueño de local
    tipoyCod = [aux.tipoUsuario.strip(), aux.codUsuario.strip()]  
    # devuelve que tipo de usuario es para devolverle el menu correspondiente
    os.system("cls")
    return tipoyCod

    #traer el registro y buscar la contraseña, con la pos accedemos a la ubicacion del registro

#------------------------------------------------------------------------------------------------------------------------------------------#
def mostrarMenu():
    print(Fore.CYAN + "-----------------------------------------")
    print("|            MENU PRINCIPAL             |")
    print("-----------------------------------------"+Fore.RESET)
    print("1. Ingresar con usuario registrado\n2. Registrarse como cliente \n3. Salir ")

def menuAdministrador():
    os.system("cls")
    menu_administrador = """
    ********************************************
    *            MENU ADMINISTRADOR            *
    ********************************************
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
    ********************************************
    *            GESTIÓN DE LOCALES            *
    ********************************************
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
    *        GESTIÓN DE NOVEDADES (Chapin)    *
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
    *               MENU CLIENTE              *
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
    width = len(title) + 6
    border = "*" * width

    print("\n" + border)
    print(f"*  {title}  *")
    print(border + "\n")

    mail = input("Ingrese una dirección de correo electrónico <máx. 100 caracteres>, o ingrese '*' para salir: ")
    
    while mail != '*' and validaRangoEntero(len(mail),1,100):
        mail = input(Fore.RED+"Incorrecto! Su correo electrónico debe tener hasta 100 caracteres o ingrese '*' para salir: "+Fore.RESET)

    if mail != '*':
        regUsu = usuarios()
        if buscaSec(mail) == -1:
            regUsu.nombreUsuario = mail
            contra = pwinput.pwinput("Ingrese una contraseña. Debe tener exactamente 8 caracteres ")
            while len(contra) != 8:
                contra = pwinput.pwinput(Fore.RED+"Incorrecto! Su contraseña debe tener 8 caracteres. "+Fore.RESET)
            regUsu.claveUsuario = contra
            regUsu.codUsuario = codUser() + 1
            regUsu.tipoUsuario = "duenioDeLocal"
            formatearUsuario(regUsu)
            pickle.dump(regUsu, alUsuarios)
            alUsuarios.flush()
            os.system("cls")
            print(Fore.GREEN + "\nUsuario tipo dueño creado exitosamente:" + Fore.RESET)
            print("- Usuario:",regUsu.nombreUsuario)
            print("- Contraseña: ********")
            print("- Codigo de usuario: ",regUsu.codUsuario)
            print("- Tipo de usuario:", regUsu.tipoUsuario)
        else:
            print(Fore.YELLOW + "El usuario ya existe. Volviendo..." + Fore.RESET + "\n")
            

#-----------------ADMINISTRADOR-----------------------------------------------------------------------------------------------------------#
def administrador():
    opc = -1
    while opc != 0:
        menuAdministrador()
        opc = input("Ingrese una opción [1-5]: ")
        while validaRangoEntero(opc, 0, 5):
            opc = input(Fore.RED + "Incorrecto - Ingrese una opción [1-5]: " + Fore.RESET)
        opc = int(opc)
        if opc == 1:
            while opc != "e":
                menuGestionDeLocales()
                opc = str(input("Ingrese una opción [a-e]: "))
                while (validaChar(opc,"a","a") and validaChar(opc,"b","b") and validaChar(opc,"c","c") and validaChar(opc,"d","d") and validaChar(opc,"e","e")):
                    opc = input(Fore.RED + "Incorrecto - Ingrese una opción [a-e]: " + Fore.RESET)
                opc = str(opc)
                if opc == "a":
                    creacionDeLocales()
                    os.system("pause")
                elif opc == "b":
                    modificacionDeLocales()
                    os.system("pause")

                elif opc == "c":
                    eliminandoLocal()
                    os.system("pause")

                elif opc == "d":
                    mapaLocal()
                    os.system("pause")

                elif opc == "e":
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
    print(Fore.CYAN+"-----------------------------------------")
    print("|          CREACION LOCALES             |")
    print("-----------------------------------------"+Fore.RESET)

    nombreLocal = str(input("Ingrese el nombre del local <máx. 50 caracteres>. "))
    while len(nombreLocal)< 1 and len(nombreLocal) > 50:
        nombreLocal = input(Fore.RED+"Incorrecto! su correo electrónico debe tener hasta 50 caracteres. "+Fore.RESET)

    while nombreLocal != "0":

        t = os.path.getsize(afLocales)
    

        if t > 0: #si el archivo no cuenta con ningun registro, no hace el ordenamiento
            ordenamiento() # esto lo puedo solucionar haciendo una busqueda secuencial para el codigo del local, que busque y solo deje el mas grande
            nombreLocalformat = str(nombreLocal).ljust(50, " ")#lo convierto a string y lo completo para que el registro siga midiendo lo mismo
            busquedaDicotomica(nombreLocalformat) # realiza la busqueda dicotomica para ver si existe o no
        
            while busquedaDicotomica(nombreLocalformat) != -1 and nombreLocalformat != "0":
                nombreLocal = input(Fore.RED + "Incorrecto! El nombre del local ya existe. Intente nuevamente. Con 0 vuelve hacia atras: " + Fore.RESET)
                ordenamiento()
                nombreLocalformat = str(nombreLocal).ljust(50, " ")#lo convierto a string y lo completo para que el registro siga midiendo lo mismo
                busquedaDicotomica(nombreLocalformat)
                
        if nombreLocal.strip() != "0":
            codUsuario = (input("Ingrese su codigo de usuario: "))
            pos = buscaSecCod(codUsuario)
            
            while pos == -1 and int(codUsuario) != 0:
                codUsuario = input(Fore.RED + "Incorrecto. Ingrese su código de usuario. Si quiere salir presione 0: " + Fore.RESET)
                if codUsuario != 0: # si no ingreso un 0 es porque envio un nuevo codigo para verificar
                    pos = buscaSecCod(codUsuario) # busca el nuevo codigo
        else:
            pos = -1

        if pos != -1: # verificar mediante una busqueda si el codigo del usuario corresponde a un dueño de local

            ubiLocal = str(input("Ingrese la ubicación del local <máx. 50 caracteres>. "))

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
            os.system("cls")
            print(Fore.GREEN + "Local creado exitosamente:" + Fore.RESET)
            print("- Nombre:",regLoc.nombreLocal)
            print("- Ubicación:",regLoc.ubiLocal)
            print("- Rubro:",regLoc.rubroLocal)
            print("- Código Local:",regLoc.codLocal)
            print("- Estado: Activo")
    
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

    os.system("cls")
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

def buscaSecCodLocal2(a):
    global afLocales, alLocales

    t = os.path.getsize(afLocales)
    alLocales.seek(0)  

    while alLocales.tell()<t:
        pos = alLocales.tell() # guardo la posicion antes de que avance (el load hace que avance al principio del registro siguiente al que estaba)
        vrTemp = pickle.load(alLocales)# traigo a memoria el registro del usuario

        if int(vrTemp.codLocal) == int(a) and int(vrTemp.codUsuario) == int(codCurrentUser):# si el codigo coincide con el ingresado retorna la posicion
            mostrarLocal(vrTemp)
            return pos
    return -1

def mostrarLocal(a):
    print("- Nombre:", a.nombreLocal)
    print("- Ubicación:", a.ubiLocal)
    print("- Rubro:", a.rubroLocal)
    print("- Estado:", a.estado)
    print("- Codigo del local:", a.codLocal)
    print("- Codigo del usuario:", a.codUsuario)

def mostrarPromo(a):
    print("- Cod promo:", a.codPromo)
    print("- Ubicación:", a.textoPromo)
    print("- Codigo del local:", a.codLocal)
    
def modificacionDeLocales():
    os.system('cls')
    global alLocales, afLocales
    print(Fore.CYAN+"---------------------------------------------")
    print("|        MODIFICACION LOCALES               |")
    print("---------------------------------------------"+Fore.RESET)
    local = locales()

    t = os.path.getsize(afLocales)# medimos el archivo para ver si esta vacio 

    if t == 0:# si el archivo esta vacio, o sea tiene tamaño 0, el sistema avisa
        print(Fore.YELLOW+"No hay locales cargados todavia"+Fore.RESET)
        os.system('pause')
    else:
        codigoLocal = (input("Ingrese el codigo del local que quiere modificar. Con 0 sale de la opcion de modificar locales: "))

        codigoLocal = int(codigoLocal)

        while codigoLocal != 0:
            pos = buscaSecCodLocal(codigoLocal)

            if pos == -1:
                print (Fore.YELLOW+"El local no existe"+Fore.RESET)

            else:
                local = locales()
                alLocales.seek(pos, 0)
                local = pickle.load(alLocales)

                if local.estado == "B":
                    print(Fore.YELLOW+"El local esta dado de baja"+Fore.RESET)
                    rta = input("\n-¿Desea restaurarlo? (Si o no): ")
                    rta = rta.strip()

                    while rta != "si" and rta != "no":
                        rta = input(Fore.RED+"Incorrecto respete el ingreso. ¿Desea restaurarlo? (Si o No): "+Fore.RESET)
                        rta = rta.strip()
                    
                    if rta.lower() == "si":

                        local.estado = "A"
                        alLocales.seek(pos, 0)
                                
                        pickle.dump(local, alLocales)
                        alLocales.flush()

                        os.system("cls")
                        print(Fore.GREEN + "****************************************")
                        print("*         Modificación exitosa         *")
                        print("****************************************" + Fore.RESET)
                        print("Los datos actualizados son: ")
                        mostrarLocal(local)


                else:
                    print(Fore.BLUE+"\nLocal a modificar: "+Fore.RESET)
                    mostrarLocal(local)
                    
                    print("\n-Actualice los campos")
                    nombreLocal = str(input("\nIngrese el nombre del local <máx. 50 caracteres>. Con 0 vuelve hacia atras: "))
                    while validaRangoEntero(len(nombreLocal),1,50):
                        nombreLocal = input(Fore.RED+"Incorrecto! El nombre debe tener hasta 50 caracteres. "+Fore.RESET)

                    if nombreLocal != "0":

                        t = os.path.getsize(afLocales)
                    
                        if t > 0: #si el archivo no cuenta con ningun registro, no hace el ordenamiento
                            ordenamiento() # esto lo puedo solucionar haciendo una busqueda secuencial para el codigo del local, que busque y solo deje el mas grande
                            nombreLocalformat = str(nombreLocal).ljust(50, " ")#lo convierto a string y lo completo para que el registro siga midiendo lo mismo
                            busquedaDicotomica(nombreLocalformat) # realiza la busqueda dicotomica para ver si existe o no
                        
                            while busquedaDicotomica(nombreLocalformat) != -1:
                                nombreLocal = input(Fore.RED+"Incorrecto! el nombre del Local ya existe. Intente nuevamente "+Fore.RESET)
                                ordenamiento()
                                nombreLocalformat = str(nombreLocal).ljust(50, " ")#lo convierto a string y lo completo para que el registro siga midiendo lo mismo
                                busquedaDicotomica(nombreLocalformat)

                            local.nombreLocal = str(nombreLocal).ljust(50, " ")

                            ubiLocal = str(input("Ingrese la ubi del local <máx. 50 caracteres>. "))

                            while validaRangoEntero(len(ubiLocal),1,50):
                                ubiLocal = input(Fore.RED+"Incorrecto! su ubicacion debe tener hasta 50 caracteres. "+Fore.RESET)

                            local.ubiLocal = str(ubiLocal).ljust(50, " ")

                            rubroLocal = str(input("Ingrese el rubro del local <indumentaria, perfumeria o comida>:  "))
                            rubroLocalSE = rubroLocal.strip()# SE de Sin Espacios


                            while (rubroLocalSE != "") and (rubroLocalSE not in ["indumentaria", "perfumeria", "comida"]):

                                rubroLocal = input(Fore.RED+"Incorrecto! el rubro no coincide con las opciones disponibles. Ingrese una opcion correcta <indumentaria, perfumeria o comida>: "+Fore.RESET)
                                rubroLocalSE = rubroLocal.strip()

                            local.rubroLocal = str(rubroLocalSE).ljust(50, " ")

                            # estadoLocal = input("Ingrese el estado del local [A/B] <solo puede dar de alta en esta sección>: ")
                            # while str(estadoLocal).lower() != "a":
                            #     if str(estadoLocal).lower() == "b":
                            #         estadoLocal = input(Fore.RED+"Incorrecto! No puede dar de baja locales en esta sección."+Fore.RESET)
                            #     else:
                            #         estadoLocal = input(Fore.RED+"Incorrecto! Ingrese A si quiere dar de alta el local "+Fore.RESET)
                            
                            # local.estado = str(estadoLocal)

                            rta = input("\n-¿Confirma la modificacion? (Si o no): ")
                            rta = rta.strip()

                            while validaChar(rta,"si","no"):
                                rta = input(Fore.RED+"Incorrecto. ¿Confirma la modificacion? (Si o no): "+Fore.RESET)
                                rta = rta.strip()

                            if rta.lower() == "si":
                                
                                alLocales.seek(pos, 0)
                                pickle.dump(local, alLocales)
                                alLocales.flush()

                                os.system("cls")
                                print(Fore.GREEN + "****************************************")
                                print("*         Modificación exitosa         *")
                                print("****************************************" + Fore.RESET)
                                print("Los datos actualizados son: ")
                                mostrarLocal(local)

            codigoLocal = int(input("\nIngrese el codigo del local que quiere modificar. Si no quiere seguir modificando locales, ingrese 0: "))
            codigoLocal = int(codigoLocal)         

#=============== BAJA DE LOCALES ==========================
def eliminandoLocal():
    global afLocales, alLocales
    os.system("cls")

    print(Fore.CYAN+"-----------------------------------------")
    print("|           ELIMINAR LOCALES            |")
    print("-----------------------------------------"+Fore.RESET)

    t = os.path.getsize(afLocales)

    if t == 0:
        print(Fore.YELLOW+"\nNo hay archivos para eliminar"+Fore.RESET)
        os.system("pause")
    else:
        codigoLocal = int(input("\nIngrese el código del local que quiere eliminar. Con 0 sale del menú: "))
        
        while codigoLocal != 0:
            pos = buscaSecCodLocal(codigoLocal)
            
            if pos == -1:
                print(Fore.YELLOW+"El código ingresado no existe"+Fore.RESET)
            else:
                local = locales()
                alLocales.seek(pos, 0)
                local = pickle.load(alLocales)

                if local.estado == "B":
                    print(Fore.YELLOW+"\nEl local ya está dado de baja"+Fore.RESET)
                else:
                    print("\nDatos del local a eliminar: ")
                    mostrarLocal(local)

                    rta = input("¿Confirma la eliminación? (Si o no): ")
                    rtaSE = rta.strip()

                    while (rtaSE != "si" and rtaSE != "no"):
                        rta = input(Fore.RED+"Incorrecto. ¿Confirma la eliminación? (Si o no): "+Fore.RESET)
                        rtaSE = rta.strip()

                    if rta.lower() == "si":
                        local.estado = "B"
                        alLocales.seek(pos)
                        pickle.dump(local, alLocales)
                        alLocales.flush()

                        os.system("cls")
                        print(Fore.GREEN + "****************************************")
                        print("*         Eliminación exitosa         *")
                        print("****************************************" + Fore.RESET)
                        print("\nLos datos actualizados son: ")
                        mostrarLocal(local)

            codigoLocal = int(input("\nIngrese el código del local que quiere eliminar. Con 0 sale del menú: "))

#================ MAPA DE LOCALES ===============
def mapaLocal():
    global afLocales, alLocales
    os.system("cls")

    print(Fore.CYAN+"---------------------------------------------")
    print("|             MAPA DE LOCALES               |")
    print("---------------------------------------------"+Fore.RESET)

    t = os.path.getsize(afLocales)

    if t> 0:
        ordenamiento()

        alLocales.seek(0)
        # Inicializar una lista de códigos de locales
        codigos_locales = ["0"] * 50
        i = 0
        while alLocales.tell() < t and i < 50:
            vrTemp = pickle.load(alLocales)
            if vrTemp.estado == "B":
                codigos_locales[i] =  Fore.RED+"0"+(vrTemp.codLocal.strip()) + Fore.RESET # Elimina espacios en blanco
            else:
                codigos_locales[i] = (vrTemp.codLocal.strip())  # Elimina espacios en blanco

            i += 1

        # Crear un arreglo nuevo con los locales ordenados alfabéticamente por su nombre
        localesordenadosalfabeticamente = list(codigos_locales)  # Guarda una copia de la lista


        # Iterar sobre la matriz y obtener los códigos de la primera columna
        for i in range(50):
            # Se nos pide que en los lugares no ocupados esté el número 0
            if i >= len(localesordenadosalfabeticamente) or localesordenadosalfabeticamente[i] == "":
                codigoint = "0"
            else:
                codigoint = (localesordenadosalfabeticamente[i]).strip()
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
        print(Fore.YELLOW + "\nNo hay locales registrados todavía." + Fore.RESET)

def validaRangoEnteros(nro, desde, hasta):
	try:              
		int(nro)      
		if int(nro) >= desde and int(nro) <= hasta:
			return False 
		else:
			return True  
	except:
		return True 
#===================================== DUEÑO DE LOCALES ========================================================
def duenioDeLocal():
    os.system("cls")
    opc = -1
    while opc != 0:
        menuDuenioDeLocal()
        opc = input("Ingrese opción [0-3]: ")
        while validaRangoEnteros(opc, 0, 3):
            opc = input(Fore.RED+"Incorrecto - Ingrese opción [0-3]: "+Fore.RESET)
        opc = int(opc)
        if opc == 1:
            CrearPromos()
        elif opc == 2:
            Reporte()
        elif opc == 3:
            pantallachapin()
        else:
            print("\n\nSaliendo ...\n\n")
    '''menuDuenioDeLocal()
    opc = str(input("Opción? <0-3>: "))
    while opc < "0" and opc >"3":
        opc = str(input(Fore.RED+"Incorrecto!: Opción? <0-3>: "+Fore.RESET))
    while (opc >= "0" and opc <="3") and opc != 0:
        match opc:
            case "1": CrearPromos()
            case "2": Reporte()
            case "3": pantallachapin()
        
        menuDuenioDeLocal()
        opc = str(input("Opción? <0-3>: "))
        while opc < "0" and opc >"3":
            opc = str(input(Fore.RED+"Incorrecto!: Opción? <0-3>: "+Fore.RESET))'''

#================== CREAR PROMOS ========================
def CrearPromos():
    global alLocales, alPromociones
    os.system("cls")
    print( """
    *******************************************
    *           CREAR DESCUENTO               *
    *******************************************
    """)

    rlp = promociones()
    
    mostrarpromos2()
    codigo = input("\nIngrese el codigo del local al que le creará la promoción: ")
    pos = buscaSecCodLocal2(codigo)

    while pos == -1 and int(codigo) !=0:
        codigo = input(Fore.RED+"Incorrecto! El local no existe o el codigo no coincide con el usuario actual o el local esta dado de baja." +Fore.RESET+" \nIngrese un nuevo codigo: ")
        pos = buscaSecCodLocal2(codigo)
    
    if pos != -1:

        rlp.textoPromo = input("\nIngrese la descripción de la promocion: \n")


        band = True

        while band: # valida el ingreso de fechas


            rlp.fechaDesdePromo = input("Ingresa la fecha de inicio de la promoción (año-mes-día): ")


            try:
                rlp.fechaDesdePromo = datetime.strptime(rlp.fechaDesdePromo, "%Y-%m-%d").date()
                band = False


            except ValueError:
                print(Fore.RED+"La fecha ingresada no tiene el formato correcto (año-mes-día)."+Fore.RESET)


        band = True
        while band: # valida el ingreso de fechas
            rlp.fechaHastaPromo = input("Ingresa la fecha de finalizacion de la promoción (año-mes-día): ")


            try:
                rlp.fechaHastaPromo = datetime.strptime(rlp.fechaHastaPromo, "%Y-%m-%d").date()
                band = False

            except ValueError:
                print(Fore.RED+"La fecha ingresada no tiene el formato correcto (año-mes-día)."+Fore.RESET)


        dias_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        print("Ingrese un 1 si la oferta es valida ese día y un 0 si no lo es. ")


        for i in range (7):
            rlp.diasSemana[i] = input(dias_semana[i] + ": ")
            while str(rlp.diasSemana[i]) != "0" and str(rlp.diasSemana[i]) != "1":
                rlp.diasSemana[i] = input(Fore.RED+"Incorrecto! Ingrese un 0 o un 1: "+Fore.RESET)



        rlp.estado = "pendiente"
        print("El estado de su nueva promoción será pendiente hasta que esta sea aprobada.")
        time.sleep(3)
        rlp.codUsuario = codCurrentUser
        rlp.codLocal = codigo
        rlp.codPromo = codPromo()

        formatearpromos(rlp)

        alPromociones.seek(0,2)
        pickle.dump(rlp, alPromociones)
        alPromociones.flush()

        os.system("cls")
        print(Fore.GREEN + "*****************************************")
        print("*      Promocion cargada con éxito      *")
        print("*****************************************" + Fore.RESET)
        os.system("pause")
    os.system("pause")
    os.system("cls")
def buscaSecCodLocal2(a):
    global afLocales, alLocales

    t = os.path.getsize(afLocales)
    alLocales.seek(0)  

    while alLocales.tell()<t:
        pos = alLocales.tell() # guardo la posicion antes de que avance (el load hace que avance al principio del registro siguiente al que estaba)
        vrTemp = pickle.load(alLocales)# traigo a memoria el registro del usuario

        if int(vrTemp.codLocal) == int(a) and int(vrTemp.codUsuario) == int(codCurrentUser) and (vrTemp.estado).strip() == "A":# si el codigo coincide con el ingresado retorna la posicion
            print("\n Local al cual se le creara una promocion: ")
            mostrarLocal(vrTemp)
            return pos
    return -1

def mostrarpromos2():
        rll = locales()
        rlp = promociones()
        pos = buscaSecDue2(codCurrentUser,0) # busco si el dueño tiene locales/en q posición 
        while pos != -1:
            alLocales.seek(pos,0)          # paro el puntero en la posición del codigo del local (en archivo locales)
            rll = pickle.load(alLocales)   # traigo archivo a memoria
            print("Local N°" + (rll.codLocal).strip() + " : " + rll.nombreLocal )
            hola = str(rll.estado)
            if hola == "A": # si el local esta activo, muestra.
                pospromo = buscaSecLoc2(rll.codLocal, 0) # busco promociones que pertenecen al local señalado
                if pospromo == -1:
                    print("No hay promos para este local")
                t = os.path.getsize(afPromociones)
                if t>0:
                    while int(pospromo) != (-1): # itera mostrando todas las promos
                        alPromociones.seek(pospromo,0)  # paro el puntero en la promocion
                        rlp = pickle.load(alPromociones)  # traigo archivo a memoria
                        print(f"Promo n° {int(rlp.codPromo)}: {(rlp.textoPromo).strip()}. Estado: {rlp.estado} Cod. Local: {rlp.codLocal}")                
                        
                        saltosA = alPromociones.tell()
                        pospromo = buscaSecLoc2(rll.codLocal,saltosA)
            saltoB = alLocales.tell()
            pos = buscaSecDue2(codCurrentUser, saltoB)
        
def buscaSecLoc2(cod_loc, pos_inicial):
    global afPromociones, alPromociones
    rlp = promociones() # antes estaba rlp = locales(), no se por que
    t = os.path.getsize(afPromociones)
    alPromociones.seek(pos_inicial, 0) # comienza desde pos_inicial
    encontrado = False
    try:
        while alPromociones.tell()<t and not encontrado:
            pos = alPromociones.tell()
            rlp = pickle.load(alPromociones)
            if int(rlp.codLocal) == int(cod_loc):
                encontrado = True
        if encontrado:
            return pos
        else:
            return -1
    except EOFError:
        return -1

def buscaSecDue2(cod_due, pos_inicial):
    global afLocales, alLocales
    rll = locales()
    t = os.path.getsize(afLocales)
    alLocales.seek(pos_inicial, 0) # comienza desde pos_inicial
    encontrado = False
    try:
        while alLocales.tell()<t and not encontrado:
            pos = alLocales.tell()
            rll = pickle.load(alLocales)
            if int(rll.codUsuario) == int(cod_due):
                encontrado = True
        if encontrado:
            return pos
        else:
            return -1
    except EOFError:
        return -1

#=============== REPORTE DE USO DE DTOS =============#
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
        while alUsoPromos.tell() < t:
            rlup = pickle.load(alUsoPromos)
            if int(rlup.codPromo) == int(cod):
                cont = cont + 1
    return cont

def buscaSecLoc22(cod_loc, pos_inicial):
    global afPromociones, alPromociones
    rlp = promociones() # antes estaba rlp = locales(), no se por que
    t = os.path.getsize(afPromociones)
    alPromociones.seek(pos_inicial, 0) # comienza desde pos_inicial
    encontrado = False
    try:
        while alPromociones.tell()<t and not encontrado:
            pos = alPromociones.tell()
            rlp = pickle.load(alPromociones)
            a = alPromociones.tell()
            if int(rlp.codLocal) == int(cod_loc):
                encontrado = True
        if encontrado:
            return pos
        else:
            return -1
    except (EOFError, pickle.PickleError):
        return -1

def Reporte():
    global codCurrentUser
    rlu = usuarios() # registro logico usuarios 
    rlup = uso_promociones()  
    rlp = promociones() 
    rll = locales()  
    os.system("cls")
    print( """
    *******************************************************
    *           REPORTE DE USO DE DESCUENTO               *
    *******************************************************
    """)
    
    band = True
    while band: # valida el ingreso de fechas
        fecha_desde = input("\n-Ingrese el rango de fechas para ver las promociones válidas <año-mes-día>: ")
        try:
            fecha_desde = datetime.strptime(fecha_desde, "%Y-%m-%d").date()
            band = False
        except ValueError:
            print(Fore.RED+"La fecha ingresada no tiene el formato correcto <año-mes-día>."+Fore.RESET)
    band = True
    while band: # valida el ingreso de fechas
        fecha_hasta = input("-Ingresa la fecha de finalizacion de la promoción <año-mes-día>: ")
        try:
            fecha_hasta = datetime.strptime(fecha_hasta, "%Y-%m-%d").date()
            band = False
        except ValueError:
            print(Fore.RED+"La fecha ingresada no tiene el formato correcto <año-mes-día>."+Fore.RESET)  
    
    pos = buscaSecDue2(codCurrentUser, 0) #busco si el dueño tiene locales/en q posicion 
    while int(pos) != (-1):  #itera mostrando todos los locales
           
        alLocales.seek(pos,0)          # paro el puntero en la posición del codigo del local (en archivo locales)
        rll = pickle.load(alLocales)  # traigo archivo a memoria

        pospromo = buscaSecLoc22(int(rll.codLocal),0) # busco promociones que pertenecen al local señalado
    

        while pospromo != (-1): #itera mostrando todas las promos
            alPromociones.seek(pospromo,0)
            rlp = pickle.load(alPromociones)
            
            aa = (fecha_desde >= rlp.fechaDesdePromo)
            bb = (fecha_hasta <= rlp.fechaHastaPromo)
            cc= fecha_desde
            dd = fecha_hasta
            ee = rlp.fechaDesdePromo
            ff = rlp.fechaHastaPromo


            if (str(rlp.estado).strip() == "aprobado") and ( rlp.fechaDesdePromo >= fecha_desde ) and ( rlp.fechaHastaPromo<= fecha_hasta):
                    
                print("\n* Nombre del local: "+rll.nombreLocal+" *")
                print("Local N° " + rll.codLocal)
                print("Promociones disponibles en el rango de fechas ingresado: ")
                print("~ Promo N° "+rlp.codPromo+": "+rlp.textoPromo)
                print("  - Fecha de inicio: "+str(rlp.fechaDesdePromo))
                print("  - Fecha de fin: "+str(rlp.fechaHastaPromo))
                print("  - Cantidad de uso: "+ str(cant(rlp.codPromo)))
                print(" ")
            
                
            alPromociones.seek(0,0)
            rlp = pickle.load(alPromociones)
            tamreg = alPromociones.tell()

            saltos = pospromo + tamreg #que busque a partir del proximo registro
            pospromo = buscaSecLoc22(rll.codLocal,saltos) # el segundo parametro es para que comience a buscar desde la posición donde encontro la primer promo
        
        alLocales.seek(0,0)
        rll = pickle.load(alLocales)
        tamregB = alLocales.tell()
        saltosB = pos + tamregB
        pos = buscaSecDue2(codCurrentUser, saltosB) # el segundo parametro es para que comience a buscar desde la posición donde encontro el primer local
    if pos == -1:
        print(Fore.YELLOW+"\nNo hay locales asignados para este usuario."+Fore.RESET)
        os.system("pause")
        os.system("cls")
    elif pospromo == -1:
        print(Fore.YELLOW+"No hay promociones disponibles aún."+Fore.RESET)

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

def pantallachapin():
    os.system("cls")
    print("*********************************")
    print("*       RESUELTO EN CHAPIN      *")
    print("*********************************")
    os.system("pause")


#=============FORMATEO PROMOS=================#
def formatearpromos(rlp):
    rlp.codPromo = str(rlp.codPromo)
    rlp.codPromo = rlp.codPromo.ljust(2, ' ')
    rlp.textoPromo = str(rlp.textoPromo)
    rlp.textoPromo = rlp.textoPromo.ljust(200, ' ')
    rlp.estado = str(rlp.estado)
    rlp.estado = rlp.estado.ljust(10, ' ')
    for i in range (6):
        rlp.diasSemana[i] = str(rlp.diasSemana[i])
        rlp.diasSemana[i] = rlp.diasSemana[i].ljust(1, ' ') # no se si justificarlo porque tiene un solo digito

#==========PUNTO 3 =======================#
def mostrar_promocion(promocion):
    
    print("\n- Codigo: ",str(promocion.codPromo))
    print("- Descripción: ",promocion.textoPromo.strip())
    print("- Fecha inicio: ",str(promocion.fechaDesdePromo))
    print("- Fecha final: ",str(promocion.fechaHastaPromo))
    print("- Dias disponibles: ",', '.join(map(str, promocion.diasSemana)))
    print("- Estado: ",(promocion.estado).strip())
    print("- Codigo del local: ",str(promocion.codLocal))
    if (promocion.estado).strip() == "aprobado":
        print("- Cantidad de uso: ",str(cantuso))
    
    

def mostrarPromosPendientes():
    global afPromociones, alPromociones
    cont = 0
    t = os.path.getsize(afPromociones)
    if t == 0:
        print(Fore.YELLOW+"No hay promociones registradas todavia"+Fore.RESET)
    else:
        print("Promociones pendientes:")
        alPromociones.seek(0)
        while alPromociones.tell()<t:
            promo = pickle.load(alPromociones)
            if (promo.estado).strip() == "pendiente":
                mostrar_promocion(promo)
                print("-----")
                cont = 1
        
        if cont == 0:
            print(Fore.YELLOW + "NO hay ninguna promoción pendiente" + Fore.RESET)
            
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
                print (Fore.YELLOW+"La promocion no existe en pendientes"+Fore.RESET)

            else:

                promo = promociones()
                alPromociones.seek(pos, 0)
                promo = pickle.load(alPromociones)


                rta = input("¿Confirma la modificacion? (Si o no): ")
                rta = rta.strip()

                while validaChar(str(rta),"si","no"):
                    rta = input(Fore.RED+"Incorrecto. ¿Confirma la modificacion? (Si o no): "+Fore.RESET)
                    rta = rta.strip()

                if rta.lower() == "si":

                    promo.estado = str("aprobado").ljust(10, " ")

                    alPromociones.seek(pos, 0)

                    pickle.dump(promo, alPromociones)

                    alPromociones.flush()

                    print(Fore.GREEN + "*****************************************")
                    print("*      Promoción aceptada con éxito     *")
                    print("*****************************************" + Fore.RESET)
                    mostrar_promocion(promo)
                
                        

            codigoPromo = int(input("Ingrese el codigo de la promocion que quiere aprobar. Ingrese 0 para volver: "))
            codigoPromo = int(codigoPromo)
    else:
        print(Fore.YELLOW+"Archivo de promociones aun vacio"+Fore.RESET)
#=====================PUNTO 5 ==================
def reporteUsoDeDtos():
    global afPromociones, alPromociones, cantuso, afUsoPromos, alUsoPromos

    os.system("cls")

    print(Fore.CYAN+"---------------------------------------------")
    print("|   Reporte de Utilización de Descuentos    |")
    print("---------------------------------------------"+Fore.RESET)

    print("Ingrese el rango de fechas para ver las promociones válidas.")
    fecha_desde = input("Ingrese la fecha desde <año-mes-día>: ")
    fecha_hasta =input("Ingrese la fecha hasta <año-mes-día>: ")
    fecha_desde = datetime.strptime(fecha_desde, "%Y-%m-%d").date()
    fecha_hasta = datetime.strptime(fecha_hasta, "%Y-%m-%d").date()

    cont = 0
    t = os.path.getsize(afPromociones)
    if t == 0:
        print(Fore.YELLOW+"\nNo hay promociones registradas todavia"+Fore.RESET)
    else:
        promo = promociones()
        alPromociones.seek(0)

        while alPromociones.tell()<t:
            promo = pickle.load(alPromociones)
            fecha_desde_promo = promo.fechaDesdePromo
            fecha_hasta_promo = promo.fechaHastaPromo

            if (promo.estado).strip() == "aprobado" and (fecha_desde_promo>= fecha_desde) and ( fecha_hasta_promo <= fecha_hasta):
                cont = 1

                t = os.path.getsize(afUsoPromos)
                alUsoPromos.seek(0)  

                while alUsoPromos.tell()<t:
                    vrTemp = pickle.load(alUsoPromos)# traigo a memoria el registro del usuario

                    if int(vrTemp.codPromo) == int(promo.codPromo) and fecha_desde_promo <= vrTemp.fechaUsoPromo and vrTemp.fechaUsoPromo<= fecha_hasta_promo:
        
                        mostrar_promocion(promo)
        if cont == 0:
            print(Fore.RED + "NO hay ninguna promoción aprobada en esa fecha o simplemente no existe" + Fore.RESET)

        os.system("pause")
                

def buscaSecCodPromo(a):
    global afPromociones, alPromociones

    t = os.path.getsize(afPromociones)
    alPromociones.seek(0)  

    while alPromociones.tell()<t:
        pos = alPromociones.tell() # guardo la posicion antes de que avance (el load hace que avance al principio del registro siguiente al que estaba)
        vrTemp = pickle.load(alPromociones)# traigo a memoria el registro del usuario

        if int(vrTemp.codPromo) == int(a) and (vrTemp.estado).strip() == "pendiente":# si el codigo coincide con el ingresado retorna la posicion
            return pos
    return -1

#======================CLIENTE====================#
def cliente():
    os.system("cls")
    menuCliente()
    opc = str(input("Opción? <0-3>: "))
    while opc < "0" or opc > "3":
        opc = str(input(Fore.RED+"Incorrecto!: Opción? <0-3>: "+Fore.RESET))
    while (opc >= "0" and opc <= "3") and opc != "0" :
        match opc:
            case "1": buscarDTOS()
            case "2": solicitarDTOS()
            case "3": pantallachapin()
        os.system("cls")
        menuCliente()
        opc = str(input("Opción? <0-3>: "))
        while opc < "0" or opc > "3":
            opc = str(input(Fore.RED+"Incorrecto!: Opción? <0-3>: "+Fore.RESET))

#=================== BUSCAR DTO ===================
def buscarDTOS():
    global alPromociones, afPromociones, alLocales, afLocales, afUsoPromos, alUsoPromos
    os.system("cls")

    print(Fore.CYAN+"---------------------------------------------")
    print("|       Buscar Promociones Disponibles      |")
    print("---------------------------------------------"+Fore.RESET)


    codigoLocal = (input("\nIngrese el codigo del local que tiene promocion. Con 0 sale del menu: "))

    codigoLocal = int(codigoLocal)

    fecha_cli = input("Ingrese una fecha que cuente desde hoy en adelante <año-mes-día>: ")
    fecha_cli = datetime.strptime(fecha_cli, "%Y-%m-%d").date()

    fecha_hoy = date.today()

    cont = 0
    t = os.path.getsize(afPromociones)
    if t == 0:
        print(Fore.YELLOW+"No hay promociones registradas todavia"+Fore.RESET)
    else:
        promo = promociones()
        alPromociones.seek(0)

        while alPromociones.tell()<t:
             
            promo = pickle.load(alPromociones)

            fecha_desde_promo = promo.fechaDesdePromo
            fecha_hasta_promo = promo.fechaHastaPromo

            if (promo.estado).strip() == "aprobado" and (fecha_hasta_promo>= fecha_cli) and ( fecha_desde_promo <= fecha_cli) and fecha_cli>= fecha_hoy and int(promo.diasSemana[fecha_hoy.weekday()]) == 1 and codigoLocal == int(promo.codLocal):
                
                mostrar_promocion(promo)
                cont = 1 # bandera para saber si entro

        
        if cont == 0:
            print(Fore.RED + "NO hay ninguna promoción aprobada en esa fecha o simplemente no existe" + Fore.RESET)
        
    os.system("pause")
    

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
    global alPromociones, afPromociones, alLocales, afLocales, cantuso
    os.system("cls")

    print(Fore.CYAN+"-----------------------------------")
    print("|       Solicitar  Descuento      |")
    print("-----------------------------------"+Fore.RESET)

    codPromocion = (input("\nIngrese el codigo de promocion que quiere usar. Con 0 sale al menu: "))

    codPromocion = int(codPromocion)

    fecha_hoy = date.today()

    cont = 0
    t = os.path.getsize(afPromociones)
    if t == 0:
        print(Fore.YELLOW+"No hay promociones registradas todavia"+Fore.RESET)
    else:     
        alPromociones.seek(0)

        while alPromociones.tell()<t:
            vrTemp = pickle.load(alPromociones)# traigo a memoria el registro del usuario

            fecha_desde_promo = vrTemp.fechaDesdePromo
            fecha_hasta_promo = vrTemp.fechaHastaPromo

            aa = (vrTemp.estado).strip() == "aprobado"
            bb = (fecha_hasta_promo>= fecha_hoy) 
            c = fecha_desde_promo
            cc = fecha_desde_promo <= fecha_hoy
            dd = int(vrTemp.diasSemana[fecha_hoy.weekday()]) == 1
            ee = codPromocion == int(vrTemp.codPromo)




            if (vrTemp.estado).strip() == "aprobado" and (fecha_hasta_promo>= fecha_hoy) and ( fecha_desde_promo <= fecha_hoy) and int(vrTemp.diasSemana[fecha_hoy.weekday()]) == 1 and codPromocion == int(vrTemp.codPromo):
                cont = 1

                cantuso += 1 

                regUsoPro = uso_promociones()
                alUsoPromos.seek(0)
                regUsoPro.codCliente = codCurrentUser
                regUsoPro.codPromo = codPromocion
                regUsoPro.fechaUsoPromo = fecha_hoy
                formatearUsoPromos(regUsoPro)
                pickle.dump(regUsoPro, alUsoPromos)
                alUsoPromos.flush()

                mostrar_promocion(vrTemp)
                print(Fore.GREEN+"*******************************************")
                print("*     Descuento utilizado con éxito       *")
                print("*******************************************"+Fore.RESET)
                
                os.system("pause")
                
        
        if cont == 0:
            print(Fore.RED + "NO hay ninguna promoción aprobada en esa fecha o simplemente no existe" + Fore.RESET)
            os.system("pause")


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
    while validaRangoEntero(opc, 1, 3):
        opc = input(Fore.RED + "Incorrecto - Ingrese una opción [1-3]: " + Fore.RESET)
    opc = int(opc)
    os.system("cls")
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
            menuDuenioDeLocal()
            duenioDeLocal()
    elif opc == 2:
        crearUsuariosTipoCliente()
    elif opc == 3:
        print("\n\nGracias por visitarnos ...\n\n")

alUsuarios.close()
alLocales.close()
alPromociones.close()
alUsoPromos.close()