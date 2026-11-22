from models import mensajerias, productos, pedidos, clientes, movimientos
from gui import productos_gui, clientes_gui, mensajeros_gui
from colorama import just_fix_windows_console, Fore, Style
from datetime import datetime
from tabulate import tabulate

just_fix_windows_console()

def limpiar():
    print("\033[H\033[J", end="")

def mensajeria(productos_mensajeria, cliente):
    
    limpiar()
    
    print(Fore.CYAN + "════════════════════════════════════════════")
    print(Fore.CYAN + "         PRODUCTOS DE LA MENSAJERIA         ")
    print(Fore.CYAN + "════════════════════════════════════════════")
    print()
    subtotal = 0
    if productos_mensajeria:
        for i, producto in enumerate(productos_mensajeria,1):
            print(f"{i}. {producto[1]} x {producto[5]} = ${producto[2] * producto[5]}")
            subtotal += producto[2] * producto[5]
        
        print(Fore.CYAN + "──────────────────────────────────────")
        
        print("Subtotal:     $", subtotal)
        print("Mensajeria: + $", cliente[5])
        
        print(Fore.CYAN + "──────────────────────────────────────")
        
        print("Total: $", subtotal + cliente[5])
        
        print(Fore.CYAN + "──────────────────────────────────────")

    
    print("[A] Agregar producto")
    print("[G] Guardar mensajeria")
    print("[E] Editar producto")
    print("[X] Eliminar producto")
    print("[C] Cancelar")
    
    opcion = input(Fore.WHITE + Style.BRIGHT + "Seleccione una opcion: ")
    return opcion.upper()
    
def opcion_mensajeria(productos_mensajeria=None, es_actualizar=False, mensajeria_id=None): 
    
    if not es_actualizar:
        cliente = clientes_gui.buscar_info_cliente()
        if not cliente:
            return
    else:
        cliente_id = mensajerias.buscar_mensajeria(mensajeria_id)[1]
        cliente = clientes.buscar_cliente_id(cliente_id)
    
    productos_mensajeria = [] if productos_mensajeria is None else productos_mensajeria
    
    while True:
        opcion = mensajeria(productos_mensajeria, cliente)
        if opcion == "A":
            productos_gui.agregar_producto(productos_mensajeria)
        elif opcion == "G":
            if len(productos_mensajeria) == 0:
                print("Debe agregar al menos un producto")
                input("Enter para continuar")
                break
            if es_actualizar:
                guardar_actualizacion_mensajeria(productos_mensajeria, mensajeria_id)
            else:
                guardar_mensajeria(productos_mensajeria, cliente)
            productos_mensajeria.clear()
            break
        elif opcion == "E":
            productos_gui.editar_producto_pedidos(productos_mensajeria)
        elif opcion == "X":
            productos_gui.eliminar_producto_pedidos(productos_mensajeria)
        elif opcion == "C":
            break
        else:
            print("\nOpcion no valida")
            input('\nEnter para continuar')
 
def guardar_actualizacion_mensajeria(productos_mensajeria, mensajeria_id):
    
    productos_originales = mensajerias.listar_detalle_mensajerias(mensajeria_id)
 
    for producto in productos_originales:
        stock = productos.buscar_stock(producto[0])[0]
        productos.actualizar_producto(
            producto[0],
            'stock',
            stock + producto[5]
        )   
        movimientos.crear_movimiento_inventario(producto[0], 'Mensajeria', mensajeria_id, producto[5], 'Actualizacion de la mensajeria')
  
    mensajerias.eliminar_detalle_mensajerias(mensajeria_id)

    total = 0

    # descontar stock de los productos nuevos
    for producto in productos_mensajeria:

        stock = productos.buscar_stock(producto[0])[0]

        productos.actualizar_producto(
            producto[0],
            'stock',
            stock - producto[5]
        )

        movimientos.crear_movimiento_inventario(producto[0], 'Mensajeria', mensajeria_id, -producto[5], 'Actualizacion de la mensajeria')

        mensajerias.detalle_mensajerias(
            mensajeria_id,
            producto[0],
            producto[5],
            producto[2],
            producto[4]
        )

        total += producto[2] * producto[5]

    mensajerias.actualizar_mensajeria(mensajeria_id, 'total', total)

    print("\nMensajeria actualizada correctamente")
    input("\nEnter para continuar")   
    
def guardar_mensajeria(productos_mensajeria, cliente):
    total = sum(producto[2] * producto[5] for producto in productos_mensajeria)

    mensajeria_id = mensajerias.crear_mensajeria(cliente[0], 'Pendiente', cliente[5], total)
    for producto in productos_mensajeria:           
        stock = productos.buscar_stock(producto[0])[0]
        stock -= producto[5]   
        productos.actualizar_producto(producto[0], 'stock', stock)
        mensajerias.detalle_mensajerias(mensajeria_id, producto[0], producto[5], producto[2], producto[4])
        movimientos.crear_movimiento_inventario(producto[0], 'Mensajeria', mensajeria_id, -producto[5], None)

    print("Mensajeria creada correctamente")
    input("Presione Enter para continuar")

def lista_mensajerias_pendientes():
    limpiar()
    lista_pendiente = mensajerias.listar_mensajerias_pendientes()
    print(tabulate(
        lista_pendiente,
        headers=['ID', 'Nombre', 'Telefono', 'Estado', 'Costo_Mensajeria', 'Total', 'Mensajero', 'Fecha'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")
    
def lista_mensajerias_enviadas():
    limpiar()
    lista_enviadas = mensajerias.listar_mensajerias_enviadas()
    print(tabulate(
        lista_enviadas,
        headers=['ID', 'Nombre', 'Telefono', 'Estado', 'Costo_Mensajeria', 'Total', 'Mensajero', 'Fecha'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")
    
def cambiar_estado():
    limpiar()
    try:
        mensajeria_id = int(input("Introduzca el ID de la mensajeria: "))
    except ValueError:
        print("\nID no valido")
        input("\nEnter para continuar")
        return
    mensajeria_estado = mensajerias.buscar_mensajeria(mensajeria_id)
    if not mensajeria_estado:
        print("\nMensajeria no encontrada")
        input("\nEnter para salir")
        return
    if mensajeria_estado[2] == 'Cancelado':
        print("\nLa mensajeria esta cancelada")
        input("\nEnter para salir")
        return
    print("""1. Pendiente
2. Enviada
3. Entregada
4. Cancelada""")
    select = input("\nSeleccione el estado: ")
    if select == "1":
        mensajerias.actualizar_mensajeria(mensajeria_id, 'estado', 'Pendiente')
    elif select == "2":
        mensajerias.actualizar_mensajeria(mensajeria_id, 'estado', 'Enviado')
        mensajero = mensajeros_gui.buscar_mensajero(True)
        mensajerias.actualizar_mensajeria(mensajeria_id, 'mensajero_id', mensajero[0])
    elif select == "3":
        mensajerias.actualizar_mensajeria(mensajeria_id, 'estado', 'Entregado')
    elif select == "4":
        mensajerias.actualizar_mensajeria(mensajeria_id, 'estado', 'Cancelado')
        productos_mensajeria = mensajerias.listar_detalle_mensajerias(mensajeria_id)
        for producto in productos_mensajeria:
            stock = productos.buscar_stock(producto[0])[0]
            productos.actualizar_producto(
                producto[0],
                'stock',
                stock + producto[5]
            ) 
            movimientos.crear_movimiento_inventario(producto[0], 'Mensajeria', mensajeria_id, producto[5], "Cancelacion")
    else:
        print("\nOpcion no valida")
        input("\nEnter para salir")

    print("\nEstado cambiado correctamente")
    input("\nEnter para continuar")

def lista_detalle_mensajeria():
    limpiar()
    try:
        mensajeria_id = int(input("Introduzca el ID de la mensajeria: "))
    except ValueError:
        print("\nID no valido")
        input("\nEnter para continuar")
        return
    mensajeria_detalle = mensajerias.buscar_mensajeria(mensajeria_id)
    if not mensajeria_detalle:
        print("\nMensajeria no encontrada")
        input("\nEnter para salir")
        return 
  
    cliente = clientes.buscar_cliente_id(mensajeria_detalle[1])

    print("\n==============================")
    print(f"""ID: {cliente[0]}
Nombre: {cliente[2]}
Telefono: {cliente[1]}
Direccion: {cliente[3]}
Observaciones: {cliente[4]}
Precio de mensajeria: {cliente[5]}""")    
    print("===============================\n")
    
    lista_detalle = mensajerias.listar_detalle_mensajerias(mensajeria_id)
    lista = []
    for detalle in lista_detalle:
        producto_id, nombre, precio, stock, precio_compra, cantidad = detalle
        subtotal = cantidad * precio
        lista.append([producto_id, nombre, cantidad, precio, subtotal])
    print(tabulate( 
        lista,
        headers=['Producto_ID', 'Nombre', 'Cantidad', 'Precio_Unitario', 'Subtotal'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")

#==================================================================================
def gestionar_mensajeria(pedidos_pendientes, mensajerias_pendientes):
    limpiar()

    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
    print(Fore.CYAN + "════════════════════════════════════════════")
    print(Fore.CYAN + "           GESTIONAR MENSAJERIAS            ")
    print(Fore.CYAN + "════════════════════════════════════════════")

    print()
    print(Fore.WHITE + f"📅 Fecha y hora: {fecha_hora}")
    print()

    print(Fore.BLUE + f"🛒 Pedidos pendientes: {pedidos_pendientes}")
    print(Fore.MAGENTA + f"🚚 Mensajerías pendientes: {mensajerias_pendientes}")

    print(Fore.CYAN + "──────────────────────────────────────")
        
    print(Fore.BLUE + "[1] Ver todas mensajerias")
    print(Fore.MAGENTA + "[2] Ver ultimas mensajerias")
    print(Fore.YELLOW + "[3] Ver mensajeria por cliente")
    print(Fore.GREEN + "[4] Editar mensajeria")
    print()
    print(Fore.RED + "[0] Volver")
    print()
        
    print(Fore.CYAN + "──────────────────────────────────────")
    opcion = input(Fore.WHITE + Style.BRIGHT + "Seleccione una opción: ") 
    return opcion 

def opcion_gestionar():
    limpiar()
    while True:
        pedidos_pendientes = len(pedidos.listar_pedidos_reservados())
        mensajerias_pendientes = len(mensajerias.listar_mensajerias_pendientes())
        opcion = gestionar_mensajeria(pedidos_pendientes, mensajerias_pendientes)
        if opcion == "1":
            lista_mensajerias()
        elif opcion == "2":
            ultimos_mensajerias()
        elif opcion == "3":
            lista_mensajerias_cliente()
        elif opcion == "4":
            editar_mensajeria()
        elif opcion == "0":
            return
        else:
            print("\nOpcion no valida")
            input("\nEnter para continuar")
 
def lista_mensajerias():
    limpiar()
    lista_mensaje = mensajerias.listar_mensajerias()
    print(tabulate(
        lista_mensaje,
        headers=['ID', 'Nombre', 'Telefono', 'Estado', 'Costo_Mensajeria', 'Total', 'Mensajero', 'Fecha'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")
    
def ultimos_mensajerias():
    limpiar()
    try:
        limite = int(input("Cuantas mensajerias desea ver: "))
    except ValueError:
        print("\nERROR debe introducir un numero entero")
        input("\nEnter para salir")
        return
    if limite < 1:
        print("\nERROR debe introducir un numero positivo")
        input("\nEnter para salir")
        return 
    lista_ultimas = mensajerias.listar_ultimas_mensajerias(limite)
    print(tabulate(
        lista_ultimas,
        headers=['ID', 'Nombre', 'Telefono', 'Estado', 'Costo_Mensajeria', 'Total', 'Mensajero', 'Fecha'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")    
    
def lista_mensajerias_cliente():
    limpiar()
    telefono = input("\nIntroduzca el telefono del cliente: ")
    cliente = clientes.buscar_cliente(telefono)
    if not cliente:
        print("\nCliente no encontrado")
        input("\nEnter para salir")
        return
    lista_por_cliente = mensajerias.listar_mensajeria_cliente(cliente[0])
    print(tabulate(
        lista_por_cliente,
        headers=['ID', 'Nombre', 'Telefono', 'Estado', 'Costo_Mensajeria', 'Total', 'Mensajero', 'Fecha'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")   
    
def editar_mensajeria():
    try:
        mensajeria_id = int(input("Introduzca el ID de la mensajeria: "))
    except ValueError:
        print("\nID no valido")
        input("\nEnter para continuar")
        return
    mensajeria_actualizar = mensajerias.buscar_mensajeria(mensajeria_id)
    if not mensajeria_actualizar:
        print("\nMensajeria no encontrada")
        input("\nEnter para salir")
        return
    if mensajeria_actualizar[2] == 'Cancelado':
        print("\nLa mensajeria esta cancelada")
        input("\nEnter para salir")
        return
    productos_mensajeria = mensajerias.listar_detalle_mensajerias(mensajeria_id)
    lista_mensajeria = []
    for producto in productos_mensajeria:
        lista_mensajeria.append(list(producto))

    es_actualizar = True
    opcion_mensajeria(lista_mensajeria, es_actualizar, mensajeria_id)