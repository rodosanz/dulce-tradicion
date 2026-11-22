from models import mensajeros
from tabulate import tabulate

def limpiar():
    print("\033[H\033[J", end="")
 
def crear_mensajero():
    limpiar()
    nombre = input("Introduzca el nombre: ")
    telefono = input("Introduzca el telefono: ")
    mensajeros.crear_mensajero(nombre, telefono)
    print("\nMensajero creado correctamente")
    input("\nEnter para continuar")
    
def ver_mensajeros():
    limpiar()
    lista_mensajeros = mensajeros.listar_mensajeros()
    print(tabulate(
        lista_mensajeros,
        headers=['Mensajero_ID', 'Nombre', 'Telefono'],
        tablefmt='rounded_grip'
    ))
    input("\nEnter para salir")
    
def eliminar_mensajero():
    limpiar()
    try:
        mensajero_id = int(input("Introduzca el ID del mensajero: "))
    except ValueError:
        print("\nID invalido")
        input("\nEnter para salir")
        return
    if mensajeros.buscar_mensajero(mensajero_id):
        mensajeros.eliminar_mensajero(mensajero_id)
        print("\nMensajero eliminado correctamente")
        input("\nEnter para continuar")
    else:
        print("\nMensajero no encontrado")
        input("\nEnter para salir")
 
def editar_mensajero():
    limpiar()
    try:
        mensajero_id = int(input("Introduzca el ID del mensajero: "))
    except ValueError:
        print("\nID invalido")
        input("\nEnter para salir")
        return
    if mensajeros.buscar_mensajero(mensajero_id):
        print("\n1. Nombre")
        print("2. Telefono")
        opcion_actualizar = input("\nSeleccione la opcion que desea actualizar: ")
        if opcion_actualizar == "1":
            nombre = input("\nIntroduzca nombre nuevo: ")
            mensajeros.actualizar_mensajero(mensajero_id, 'nombre', nombre)
        elif opcion_actualizar == "2":
            telefono = input("\nIntroduzca telefono nuevo: ")
            mensajeros.actualizar_mensajero(mensajero_id, 'telefono', telefono)
        else:
            print("\nOpcion no valida")
            input("\nEnter para salir")
            return
        print("Mensajero actualizado correctamente")
        input("\nEnter para continuar")
        return
    else:
        print("\nmensajero no encontrado")
        input("\nEnter para salir")
        
def buscar_mensajero(es_estado=False):
    limpiar()
    lista_mensajeros = mensajeros.buscar_mensajero_nombre()
    if not lista_mensajeros:
        print("\nMensajero no encontrado")
        input("\nEnter para salir")
        return
    for i, mensajero in enumerate(lista_mensajeros, 1):
        print(f"{i}. {mensajero[1]}")
    try:
        select = int(input("Seleccione el mensajero: "))
    except ValueError:
        print("\nOpcion no valida")
        input("\nEnter para salir")
        return
    if select < 1 or select > len(lista_mensajeros):
        print("\nOpcion no valida")
        input("\nEnter para salir")
        return       
    mensaj = lista_mensajeros[select - 1]
    if not es_estado:
        print(tabulate(
            [mensaj],
            headers=['Mensajero_ID', 'Nombre', 'Telefono'],
            tablefmt='rounded_grip'
        ))
        input("\nEnter para salir")
    return mensaj