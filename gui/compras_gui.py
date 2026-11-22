from colorama import just_fix_windows_console, Fore, Style
from models import compras, proveedores,productos, movimientos
from gui import productos_gui
from tabulate import tabulate


just_fix_windows_console()

def limpiar():
    print("\033[H\033[J", end="")

def compra(productos_compra):
    limpiar()
    
    print(Fore.CYAN + "════════════════════════════════════════════")
    print(Fore.CYAN + "           PRODUCTOS DE LA COMPRA           ")
    print(Fore.CYAN + "════════════════════════════════════════════")
    print()
    total = 0
    if productos_compra:
        for i, producto in enumerate(productos_compra,1):
            print(f"{i}. {producto[1]} x {producto[5]} = ${producto[4] * producto[5]}")
            total += producto[4] * producto[5]
        
        print(Fore.CYAN + "──────────────────────────────────────")
        
        print("Total: $", total)
        
        print(Fore.CYAN + "──────────────────────────────────────")
    
    print("[A] Agregar producto")
    print("[G] Guardar compra")
    print("[E] Editar producto")
    print("[X] Eliminar producto")
    print("[C] Cancelar")

    opcion = input(Fore.WHITE + Style.BRIGHT + "Seleccione una opcion: ")
    return opcion.upper()

def opcion_compra(productos_compra=None, es_actualizar=False, compra_id=None): 
    productos_compra = [] if productos_compra is None else productos_compra
    while True:
        es_venta = False
        opcion = compra(productos_compra)
        if opcion == "A":
            productos_gui.agregar_producto(productos_compra, es_venta)
        elif opcion == "G":
            if len(productos_compra) == 0:
                print("Debe agregar al menos un producto")
                input("Enter para continuar")
                break
            if es_actualizar:
                guardar_actualizacion(productos_compra, compra_id)
            else:
                guardar_compra(productos_compra)
            productos_compra.clear()
            return
        elif opcion == "E":
            productos_gui.editar_producto_pedidos(productos_compra)
        elif opcion == "X":
            productos_gui.eliminar_producto_pedidos(productos_compra)
        elif opcion == "C":
            productos_compra.clear()
            return
        else:
            print("\nOpcion no valida")
            input('\nEnter para continuar')
            
def guardar_compra(productos_compra):
    total = sum(producto[4] * producto[5] for producto in productos_compra)
        
    fila_proveedores = proveedores.buscar_proveedor_nombre()
    proveedor_id = None
    if fila_proveedores:
        for i, fila in enumerate(fila_proveedores, 1):
            print(f"{i}. {fila[1]}")
        try:
            opcion_proveedor = int(input("\nSeleccione proveedor: "))
        except ValueError:
            print("\nOpcion no valida")
            input("\nEnter para salir")
        if opcion_proveedor < 1 or opcion_proveedor > len(fila_proveedores):
            print("Opcion no valida")
            input("\nEnter para salir")
            return
        proveedor = fila_proveedores[opcion_proveedor - 1]
        proveedor_id = proveedor[0]
    else:
        print("Proveedor no encontado")
        
    observacion = None
    opcion_observacion = input("Desea añadir alguna observacion? [S] para Si: ")
    if opcion_observacion.upper() == "S":
        observacion = input("Introduzca observacion: ")
    compra_id = compras.crear_compra(total, observacion, proveedor_id)
    for product in productos_compra:
        compras.crear_detalle_compra(compra_id, product[0], product[5], product[4])
        stock = productos.buscar_stock(product[0])
        stock_actual = stock[0] + product[5]
        productos.actualizar_producto(product[0], 'stock', stock_actual)
        movimientos.crear_movimiento_inventario(product[0], 'Compra', compra_id, product[5], None)

    print("\nCompra realizada con exito")
    input("\nEnter para continuar")

def ver_compras():
    limpiar()
    lista_compras = compras.listar_compra()
    print(tabulate(
        lista_compras,
        headers=['Compra_id', 'Proveedor', 'Total', 'Fecha', 'Observaciones'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")
    
def ver_detalle_compra():
    limpiar()
    try:
        compra_id = int(input("Introduzca el ID de la compra: "))
    except ValueError:
        print("\nID invalido")
        input("\nEnter para salir")
        return
    if compras.buscar_compra(compra_id):
        lista_detalles = compras.listar_detalle_compra(compra_id)
        lista_compra = []
        for detalle in lista_detalles:
            producto_id, producto, precio_venta, stock, precio_compra, cantidad = detalle
            lista_compra.append([producto, cantidad, precio_compra, cantidad * precio_compra])
        print(tabulate(
            lista_compra,
            headers=['Producto', 'Cantidad', 'Precio_Compra', 'Subtotal'],
            tablefmt='rounded_grid'
        ))
        input("\nEnter para salir")
        return
    else:
        print("\nID no encontrado")
        input("\nEnter para salir")
        return
  
def eliminar_compra():
    limpiar()
    try:
        compra_id = int(input("Introduzca el ID de la compra: "))
    except ValueError:
        print("\nID invalido")
        input("\nEnter para salir")
        return
    if compras.buscar_compra(compra_id):
        compras.eliminar_detalle_compra(compra_id)
        compras.eliminar_compra(compra_id)
        print("\nCompra eliminada correctamente")
        input("\nEnter para continuar")
        return
    else:
        print("\nID no encontrado")
        input("\nEnter para salir")   
        return
    
def actualizar_compra():
    try:
        compra_id = int(input("Introduzca el ID de la compra: "))
    except ValueError:
        print("\nID no valido")
        input("\nEnter para continuar")
        return
    if not compras.buscar_compra(compra_id):
        print("\nPedido no encontrado")
        input("\nEnter para salir")
        return
    productos_compra = compras.listar_detalle_compra(compra_id)
    lista_compra = []
    
    for product in productos_compra:
        lista_compra.append(list(product))

    es_actualizar = True
    opcion_compra(lista_compra, es_actualizar, compra_id)
    
def guardar_actualizacion(productos_compra, compra_id):
   
    productos_originales = compras.listar_detalle_compra(compra_id)
 
    for producto in productos_originales:
        stock = productos.buscar_stock(producto[0])[0]
        productos.actualizar_producto(
            producto[0],
            'stock',
            stock - producto[5]
        )  
        movimientos.crear_movimiento_inventario(producto[0], 'Compra', compra_id, -producto[5], 'Actualizacion de la compra')
 
  
    compras.eliminar_detalle_compra(compra_id)

    total = 0

    # aumentar stock de los productos nuevos
    for producto in productos_compra:

        stock = productos.buscar_stock(producto[0])[0]

        productos.actualizar_producto(
            producto[0],
            'stock',
            stock + producto[5]
        )
        
        movimientos.crear_movimiento_inventario(producto[0], 'Compra', compra_id, producto[5], 'Actualizacion de la compra')

        compras.crear_detalle_compra(
            compra_id,
            producto[0],
            producto[5],
            producto[4]
        )

        total += producto[4] * producto[5]

    compras.actualizar_compra(compra_id, 'total', total)

    print("\nPedido actualizado correctamente")
    input("\nEnter para continuar")
     