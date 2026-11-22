from models import proveedores
from colorama import just_fix_windows_console, Fore
from tabulate import tabulate

just_fix_windows_console()

def limpiar():
    print("\033[H\033[J", end="")

def crear_proveedor():
    limpiar()
    nombre = input("Introduzca el nombre: ")
    telefono = input("Introduzca el telefono: ")
    proveedores.crear_proveedor(nombre, telefono)
    print("\nProveedor creado correctamente")
    input("\nEnter para continuar")
    
def ver_proveedores():
    limpiar()
    lista_proveedores = proveedores.listar_proveedores()
    print(tabulate(
        lista_proveedores,
        headers=['Proveedor_ID', 'Nombre', 'Telefono'],
        tablefmt='rounded_grip'
    ))
    input("\nEnter para salir")
    
def eliminar_proveedor():
    limpiar()
    try:
        proveedor_id = int(input("Introduzca el ID del proveedor: "))
    except ValueError:
        print("\nID invalido")
        input("\nEnter para salir")
        return
    if proveedores.buscar_proveedor(proveedor_id):
        proveedores.eliminar_proveedor(proveedor_id)
        print("\nProveedor eliminado correctamente")
        input("\nEnter para continuar")
    else:
        print("\nProveedor no encontrado")
        input("\nEnter para salir")
    
def editar_proveedor():
    limpiar()
    try:
        proveedor_id = int(input("Introduzca el ID del proveedor: "))
    except ValueError:
        print("\nID invalido")
        input("\nEnter para salir")
        return
    if proveedores.buscar_proveedor(proveedor_id):
        print("\n1. Nombre")
        print("2. Telefono")
        opcion_actualizar = input("\nSeleccione la opcion que desea actualizar: ")
        if opcion_actualizar == "1":
            nombre = input("\nIntroduzca nombre nuevo: ")
            proveedores.actualizar_proveedor(proveedor_id, 'nombre', nombre)
        elif opcion_actualizar == "2":
            telefono = input("\nIntroduzca telefono nuevo: ")
            proveedores.actualizar_proveedor(proveedor_id, 'telefono', telefono)
        else:
            print("\nOpcion no valida")
            input("\nEnter para salir")
            return
        print("Proveedor actualizado correctamente")
        input("\nEnter para continuar")
        return
    else:
        print("\nProveedor no encontrado")
        input("\nEnter para salir")
        