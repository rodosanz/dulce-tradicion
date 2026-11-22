from models import clientes
from tabulate import tabulate

def limpiar():
    print("\033[H\033[J", end="")
    
def agregar_cliente():
    limpiar()
    telefono = input("Telefono del cliente: ")
    if not telefono:
        print("\nDebe introducir un telefono")
        print("Accion cancelada")
        input("\nEnter para salir")
        return
    if clientes.buscar_cliente(telefono):
        print("\nEl cliente ya existe")
        input("\nEnter para salir")
        return
    nombre = input("Nombre del cliente: ")
    if not nombre:
        print("\nDebe introducir un nombre")
        print("Accion cancelada")
        input("\nEnter para salir")
        return    
    direccion = input("Direccion: ")
    observacion = input("Observaciones: ")
    try:
        precio_mensajeria = float(input("Precio de mensajeria: "))
    except ValueError:
        print("\nDebe introducir un numero")
        print("Accion cancelada")
        input("\nEnter para salir")
        return
    if precio_mensajeria < 0:
        print("\nEl precio no debe ser negativo")
        print("Accion cancelada")
        input("\nEnter para contiuar")
    cliente_id = clientes.crear_cliente(telefono, nombre, direccion, observacion, precio_mensajeria)
    print("Cliente agregado")
    input("Enter para continuar") 
    return cliente_id
    
def ver_clientes():
    limpiar()
    lista_cliente = clientes.listar_clientes()
    print(tabulate(
        lista_cliente,
        headers=['ID', 'Nombre', 'Telefono'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")
  
def buscar_info_cliente():
    limpiar()
    telefono = input("\nIntroduzca el telefono del cliente: ")
    cliente = clientes.buscar_cliente(telefono)
    if not cliente:
        print("\nCliente no encontrado")
        input("\nEnter para salir")
        return
    print("\n==============================")
    print(f"""ID: {cliente[0]}
Nombre: {cliente[2]}
Telefono: {cliente[1]}
Direccion: {cliente[3]}
Observaciones: {cliente[4]}
Precio de mensajeria: {cliente[5]}""")    
    print("===============================")
    input("\nEnter para continuar")
    return cliente

def buscar_cliente_nombre():
    limpiar()
    lista_clientes = clientes.buscar_cliente_nombre()
    if not lista_clientes:
        print("\nCliente no encontrado")
        input("\nEnter para salir")
        return
    for i, cliente in enumerate(lista_clientes, 1):
        print(f"{i}. {cliente[2]}")
    try:
        select = int(input("Seleccione el cliente: "))
    except ValueError:
        print("\nOpcion no valida")
        input("\nEnter para salir")
        return
    if select < 1 or select > len(lista_clientes):
        print("\nOpcion no valida")
        input("\nEnter para salir")
        return       
    client = lista_clientes[select - 1]
  
    print("\n==============================")
    print(f"""ID: {client[0]}
Nombre: {client[2]}
Telefono: {client[1]}
Direccion: {client[3]}
Observaciones: {client[4]}
Precio de mensajeria: {client[5]}""")    
    print("===============================")
    input("\nEnter para salir")   
          
def eliminar_cliente():
    limpiar()
    telefono = input("\nIntroduzca el telefono del cliente: ")
    cliente = clientes.buscar_cliente(telefono)
    if cliente:
        clientes.eliminar_cliente(cliente[1])
        print("\nCliente eliminado correctamente")
        input("\nEnter para continuar")
        return
    else:
        print("\nCliente no encontrado")
        input("\nEnter para salir")
        return
    
def editar_cliente():
    limpiar()
    telefono = input("\nIntroduzca el telefono del cliente: ")
    cliente = clientes.buscar_cliente(telefono)
    if not cliente:
        print("\nCliente no encontrado")
        input("\nEnter para salir")
        return
    
    print("\n1. Telefono")
    print("2. Nombre")
    print("3. Direccion")
    print("4. Observaciones")
    print("5. Precio de mensajeria")
    opcion = input("\nSeleccione la opcion que desea editar: ")
    
    if opcion == "1":
        telefono_nuevo = input("\nIntroduzca el telefono nuevo: ")
        if telefono_nuevo:
            clientes.actualizar_cliente(telefono, 'telefono', telefono_nuevo)
        else:
            print("\nDebe introducir un numero de telefono")
            input("\nEnter para salir")
            return
    elif opcion == "2":
        nombre_nuevo = input("\nIntroduzca el nombre nuevo: ")
        if nombre_nuevo:
            clientes.actualizar_cliente(telefono, 'nombre', nombre_nuevo)
        else:
            print("\nDebe introducir un nombre")
            input("\nEnter para salir")
            return            
    elif opcion == "3":
        direccion_nuevo = input("\nIntroduzca la direccion nueva: ")
        if direccion_nuevo:
            clientes.actualizar_cliente(telefono, 'direccion', direccion_nuevo)
        else:
            print("\nDebe introducir una direccion")
            input("\nEnter para salir")
            return
    elif opcion == "4":
        observacion_nuevo = input("\nIntroduzca observaccion nueva: ")
        if observacion_nuevo:
            clientes.actualizar_cliente(telefono, 'observaciones', observacion_nuevo)
        else:
            print("\nDebe introducir una observacion")
            input("\nEnter para salir")
            return    
    elif opcion == "5":
        try:
            precio_nuevo = float(input("\nIntroduzca precio de mensajeria nuevo: "))
        except ValueError:
            print("\nDebe introducir un numero")
            input("\nEnter para salir")
            return
        if precio_nuevo and precio_nuevo >= 0:
            clientes.actualizar_cliente(telefono, 'precio_mensajeria', precio_nuevo)
        else:
            print("\nDebe introducir un precio de mensajeria valido")
            input("\nEnter para salir")
            return   
    else:
        print("\nOpcion no valida")
        input("\nEnter para salir")
        return
    print("\nCliente actualizado correctamente")
    input("\nEnter para continuar")