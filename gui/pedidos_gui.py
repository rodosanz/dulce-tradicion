from models import pedidos, clientes, mensajerias, productos, movimientos
from gui import productos_gui, clientes_gui
from datetime import datetime
from colorama import just_fix_windows_console, Fore, Style
from tabulate import tabulate

just_fix_windows_console()

def limpiar():
    print("\033[H\033[J", end="")

def guardar_pedido(productos_pedido):
    total = sum(producto[2] * producto[5] for producto in productos_pedido)
    estado = input("¿Desea reservar este pedido? Presione (S) para Si: ")
    if estado.upper() == 'S':
        telefono = input("Introduzca el numero de telefono: ")   
        cliente = clientes.buscar_cliente(telefono)    
        if cliente:
            venta_id = pedidos.crear_pedido(cliente[0], 'Reservado', total)
            for producto in productos_pedido:               
                stock = productos.buscar_stock(producto[0])[0]
                stock -= producto[5]   
                productos.actualizar_producto(producto[0], 'stock', stock)               
                pedidos.crear_detalle_pedido(venta_id, producto[0], producto[5], producto[2], producto[4])
                movimientos.crear_movimiento_inventario(producto[0], 'Venta', venta_id, -producto[5], None)
        else:
            print("Cliente no encontrado")
            opcion = input("Desea agregar un nuevo cliente? Presione (S) para Si: ")
            if opcion.upper() == 'S':
                cliente_id = clientes_gui.agregar_cliente() 
                if not cliente_id:
                    return
                venta_id = pedidos.crear_pedido(cliente_id, 'Reservado', total)
                for producto in productos_pedido:                
                    stock = productos.buscar_stock(producto[0])[0]
                    stock -= producto[5]   
                    productos.actualizar_producto(producto[0], 'stock', stock)                   
                    pedidos.crear_detalle_pedido(venta_id, producto[0], producto[5], producto[2], producto[4]) 
                    movimientos.crear_movimiento_inventario(producto[0], 'Venta', venta_id, -producto[5], None)

            else:
                print("Pedido cancelado")
                input("Presione Enter para continuar")
                return                    
    else:
        venta_id = pedidos.crear_pedido(None, 'Entregado', total)
        for producto in productos_pedido:           
            stock = productos.buscar_stock(producto[0])[0]
            stock -= producto[5]   
            productos.actualizar_producto(producto[0], 'stock', stock)
            pedidos.crear_detalle_pedido(venta_id, producto[0], producto[5], producto[2], producto[4])
            movimientos.crear_movimiento_inventario(producto[0], 'Venta', venta_id, -producto[5], None)

    print("Pedido creado correctamente")
    input("Presione Enter para continuar")
        
def pedido(productos_pedido):
    limpiar()
    
    print(Fore.CYAN + "════════════════════════════════════════════")
    print(Fore.CYAN + "            PRODUCTOS DEL PEDIDO            ")
    print(Fore.CYAN + "════════════════════════════════════════════")
    print()
    total = 0
    if productos_pedido:
        for i, producto in enumerate(productos_pedido,1):
            print(f"{i}. {producto[1]} x {producto[5]} = ${producto[2] * producto[5]}")
            total += producto[2] * producto[5]
        
        print(Fore.CYAN + "──────────────────────────────────────")
        
        print("Total: $", total)
        
        print(Fore.CYAN + "──────────────────────────────────────")
    
    print("[A] Agregar producto")
    print("[G] Guardar pedido")
    print("[E] Editar producto")
    print("[X] Eliminar producto")
    print("[C] Cancelar")

    opcion = input(Fore.WHITE + Style.BRIGHT + "Seleccione una opcion: ")
    return opcion.upper()

def opcion_pedido(productos_pedido=None, es_actualizar=False, pedido_id=None): 
    productos_pedido = [] if productos_pedido is None else productos_pedido
    while True:
        opcion = pedido(productos_pedido)
        if opcion == "A":
            productos_gui.agregar_producto(productos_pedido)
        elif opcion == "G":
            if len(productos_pedido) == 0:
                print("Debe agregar al menos un producto")
                input("Enter para continuar")
                break
            if es_actualizar:
                guardar_actualizacion_pedido(productos_pedido, pedido_id)
            else:
                guardar_pedido(productos_pedido)
            productos_pedido.clear()
            break
        elif opcion == "E":
            productos_gui.editar_producto_pedidos(productos_pedido)
        elif opcion == "X":
            productos_gui.eliminar_producto_pedidos(productos_pedido)
        elif opcion == "C":
            break
        else:
            print("\nOpcion no valida")
            input('\nEnter para continuar')
 
def gestionar_pedido(pedidos_pendientes, mensajerias_pendientes):
    limpiar()

    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
    print(Fore.CYAN + "════════════════════════════════════════════")
    print(Fore.CYAN + "             GESTIONAR PEDIDOS              ")
    print(Fore.CYAN + "════════════════════════════════════════════")

    print()
    print(Fore.WHITE + f"📅 Fecha y hora: {fecha_hora}")
    print()

    print(Fore.BLUE + f"🛒 Pedidos pendientes: {pedidos_pendientes}")
    print(Fore.MAGENTA + f"🚚 Mensajerías pendientes: {mensajerias_pendientes}")

    print(Fore.CYAN + "──────────────────────────────────────")
        
    print(Fore.BLUE + "[1] Ver todos pedido")
    print(Fore.MAGENTA + "[2] Ver ultimos pedidos")
    print(Fore.YELLOW + "[3] Ver detalle de pedido")
    print(Fore.GREEN + "[4] Editar pedido")
    print(Fore.CYAN + "[5] Cambiar estado")
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
        opcion = gestionar_pedido(pedidos_pendientes, mensajerias_pendientes)
        if opcion == "1":
            lista_pedidos()
        elif opcion == "2":
            ultimos_pedidos()
        elif opcion == "3":
            lista_detalle_pedido()
        elif opcion == "4":
            editar_pedido()
        elif opcion == "5":
            estado_pedido()
        elif opcion == "0":
            return
        else:
            print("\nOpcion no valida")
            input("\nEnter para continuar")
            
def lista_pedidos():
    limpiar()
    lista_todos_pedidos = pedidos.listar_pedidos()
    print(tabulate(
        lista_todos_pedidos,
        headers = ['ID', 'Estado', 'Total', 'Fecha'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")
 
def lista_detalle_pedido():
    limpiar()
    try:
        pedido_id = int(input("Introduzca el ID del pedido: "))
    except ValueError:
        print("\nID no valido")
        input("\nEnter para continuar")
        return
    pedido_detalle = pedidos.buscar_pedido(pedido_id)
    if not pedido_detalle:
        print("\nPedido no encontrado")
        input("\nEnter para salir")
        return 
    
    if pedido_detalle[2]:
        cliente = clientes.buscar_cliente_id(pedido_detalle[2])
        print("\n==============================")
        print(f"""ID: {cliente[0]}
Nombre: {cliente[2]}
Telefono: {cliente[1]}
Direccion: {cliente[3]}
Observaciones: {cliente[4]}
Precio de mensajeria: {cliente[5]}""")    
        print("===============================\n")
    
    lista_detalle = pedidos.listar_detalle_pedidos(pedido_id)
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
    
def ultimos_pedidos():
    limpiar()
    try:
        limite = int(input("Cuantos pedidos desea ver: "))
    except ValueError:
        print("\nERROR debe introducir un numero entero")
        input("\nEnter para salir")
        return
    if limite < 1:
        print("\nERROR debe introducir un numero positivo")
        input("\nEnter para salir")
        return       
    lista_ultimos_pedidos = pedidos.listar_ultimos_pedidos(limite)
    print(tabulate(
        lista_ultimos_pedidos,
        headers = ['ID', 'Estado', 'Total', 'Fecha'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")    
  
def editar_pedido():
    try:
        pedido_id = int(input("Introduzca el ID del pedido: "))
    except ValueError:
        print("\nID no valido")
        input("\nEnter para continuar")
        return
    pedido_actualizar = pedidos.buscar_pedido(pedido_id)
    if not pedido_actualizar:
        print("\nPedido no encontrado")
        input("\nEnter para salir")
        return
    if pedido_actualizar[1] == 'Cancelado':
        print("\nEl pedido esta cancelado")
        input("\nEnter para salir")
        return
    productos_pedido = pedidos.listar_detalle_pedidos(pedido_id)
    lista_pedido = []
    for producto in productos_pedido:
        lista_pedido.append(list(producto))

    for producto in lista_pedido:
        stock = productos.buscar_stock(producto[0])[0]
        producto[3] = stock + producto[5]

    es_actualizar = True
    opcion_pedido(lista_pedido, es_actualizar, pedido_id)
 
def guardar_actualizacion_pedido(productos_compra, pedido_id):
    
    productos_originales = pedidos.listar_detalle_pedidos(pedido_id)
 
    for producto in productos_originales:
        stock = productos.buscar_stock(producto[0])[0]
        productos.actualizar_producto(
            producto[0],
            'stock',
            stock + producto[5]
        )   
        movimientos.crear_movimiento_inventario(producto[0], 'Venta', pedido_id, producto[5], 'Actualizacion del pedido')

  
    pedidos.eliminar_detalle_pedido(pedido_id)

    total = 0

    # descontar stock de los productos nuevos
    for producto in productos_compra:

        stock = productos.buscar_stock(producto[0])[0]

        productos.actualizar_producto(
            producto[0],
            'stock',
            stock - producto[5]
        )
        
        movimientos.crear_movimiento_inventario(producto[0], 'Venta', pedido_id, -producto[5], 'Actualizacion del pedido')

        pedidos.crear_detalle_pedido(
            pedido_id,
            producto[0],
            producto[5],
            producto[2],
            producto[4]
        )

        total += producto[2] * producto[5]

    pedidos.actualizar_pedido(pedido_id, 'total', total)

    print("\nPedido actualizado correctamente")
    input("\nEnter para continuar")
         
def estado_pedido():
    limpiar()
    try:
        pedido_id = int(input("Introduzca el ID del pedido: "))
    except ValueError:
        print("\nID no valido")
        input("\nEnter para continuar")
        return
    pedido_estado = pedidos.buscar_pedido(pedido_id)
    if not pedido_estado:
        print("\nPedido no encontrado")
        input("\nEnter para salir")
        return
    if pedido_estado[1] == 'Cancelado':
        print("\nEl pedido esta cancelado")
        input("\nEnter para salir")
        return
    print("\n1. Pendiente")
    print("2. Entregado")
    print("3. Cancelado")
    print()
    estado = input("Seleccione un estado: ")
    if estado == "1":
        pedidos.actualizar_pedido(pedido_id, 'estado', 'Reservado')
    elif estado == "2":
        pedidos.actualizar_pedido(pedido_id, 'estado', 'Entregado')
    elif estado == "3":   
        pedidos.actualizar_pedido(pedido_id, 'estado', 'Cancelado') 
        productos_originales = pedidos.listar_detalle_pedidos(pedido_id)
        for producto in productos_originales:
            stock = productos.buscar_stock(producto[0])[0]
            productos.actualizar_producto(
                producto[0],
                'stock',
                stock + producto[5]
            ) 
            movimientos.crear_movimiento_inventario(producto[0], 'Venta', pedido_id, producto[5], 'Cancelacion')
    else:
        print("Opcion no valida")
        input("Enter para salir")
        return  
    print("\nEstado cambiado correctamente")
    input("\nEnter para continuar")
    
def lista_pedidos_pendientes():
    limpiar()
    lista_todos_pedidos = pedidos.listar_pedidos_reservados()
    print(tabulate(
        lista_todos_pedidos,
        headers = ['Pedido_ID', 'Nombre', 'Telefono','Estado', 'Total', 'Fecha'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")   