from colorama import just_fix_windows_console
from models import productos, movimientos
from tabulate import tabulate

just_fix_windows_console()

def limpiar():
    print("\033[H\033[J", end="")

def agregar_producto(productos_pedido, es_venta=True):
    limpiar()
    products = productos.buscar_producto()
    print("\nResultados:\n")
    for i, producto in enumerate(products, 1):
        print(f"{i}. {producto[1]} --- Stock: {producto[3]}")
    print()
    try:
        seleccion = int(input("Seleccione producto: "))
    except ValueError:
        print("Producto no valido")
        input("Enter para continuar")
        return
    if seleccion < 1 or seleccion > len(products):
        print("Producto no valido")
        return None
    producto = list(products[seleccion - 1])

    if producto:
        esta = False
        for product in productos_pedido:
            if product[0] == producto[0]:
                esta = True
        if esta:
            print("\nProducto ya se encuentra en la lista")
            input("\nEnter para continuar")
            return
             
    try:
        cantidad = int(input("Cantidad: "))
    except ValueError:
        print("Cantidad no valida")
        input("Enter para continuar")  
        return      
    if cantidad > 0:
        if cantidad <= productos.buscar_stock(producto[0])[0] and es_venta:
            producto.append(cantidad)
        elif not es_venta:
            producto.append(cantidad)
            productos_pedido.append(producto)
            return producto           
        else:
            print("\nCantidad no disponible")
            print("Cantidad no debe exceder el stock")
            input("\nEnter para continuar")
            return
    else:
        print("\nCantidad debe ser positivo")
        input("\nEnter para continuar")
        return
    
    if es_venta:
        opcion_precio = input("Desea utilizar otro precio? Presione [S] para Si: ")
        if opcion_precio.upper() == "S":
            try:
                precio_nuevo = int(input("Introduzca el precio nuevo: "))
            except ValueError:
                print("\nPrecio invalido")
                input("\nEnter para salir")
                return
            if precio_nuevo > 0:
                producto[2] = precio_nuevo
            else:
                print("\nPrecio invalido")
                input("\nEnter para salir")  
                return  
            
    productos_pedido.append(producto)
    return producto   

def editar_producto_pedidos(products):
    try:
        num_producto = int(input("Seleccione el producto a editar: "))
    except ValueError:
        print("Producto no valido")
        input("Presione Enter para continuar")
        return
    if num_producto < 1 or num_producto > len(products):  
        print("Producto no valido")
        input("Presione Enter para continuar")
        return
    product = products[num_producto - 1]
    try:
        cantidad = int(input("Cantidad: "))
    except ValueError:
        print("Cantidad no valida")
        input("Presione Enter para continuar")
        return    
    if cantidad < 1:
        print("Cantidad no valida")
        input("Presione Enter para continuar")
        return  
    if cantidad > product[3]:
        print("\nCantidad no disponible")
        print("Cantidad debe ser menor que el stock")
        input("\nPresione Enter para continuar")
        return        
    product[5] = cantidad
    
def eliminar_producto_pedidos(products):
    try:
        num_producto = int(input("Seleccione el producto a eliminar: "))
    except ValueError:
        print("Producto no valido")
        input("Presione Enter para continuar")
        return    
    if num_producto < 1 or num_producto > len(products):  
        print("Producto no valido")
        input("Presione Enter para continuar")
        return          
    products.pop(num_producto - 1)
 
#---------------------------------------------------------------------------

def crear_producto():
    limpiar()
    nombre = input("Nombre del producto: ")
    if not nombre:
        print("\nDebe introducir un nombre")
        input("\nEnter para salir")
        return
    try:
        precio_compra = float(input("Precio de compra: "))
        precio_venta = float(input("Precio de venta: "))
    except ValueError:
        print("ERROR! debe introducir un numero")
        input("Presione Enter para salir")
    if precio_compra < 0 or precio_venta < 0:
        print("\nPrecio no debe ser negativo")
        print("Accion cancelada")
        input("\nEnter para salir")
        return
    productos.crear_producto(nombre, precio_compra, precio_venta)
    print("Producto agregado")
    input("Enter para continuar")   
    
def ver_productos():
    limpiar()
    lista_productos = productos.listar_productos()
    print(tabulate(
        lista_productos,
        headers=['ID', 'Nombre', 'Precio_Compra', 'Precio_Venta', 'Stock'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")
    
def eliminar_producto():
    limpiar()
    products = productos.buscar_producto()
    for i, product in enumerate(products, 1):
        print(f"{i}. {product[1]}")
    try:
        opcion = int(input("\nSeleccione el producto que desea eliminar: "))
    except ValueError:
        print("\nOpcion no valida")
        input("\nEnter para salir")
        return
    if opcion < 1 or opcion > len(products):
        print("\nOpcion no valida")
        input("\nEnter para salir")
        return
    
    producto_eliminar = products[opcion - 1]
    
    productos.eliminar_producto(producto_eliminar[0])
    
    print("\nProducto eliminado correctamente")
    input("\nEnter para continuar")
    
def editar_producto():
    limpiar()
    products = productos.buscar_producto()
    for i, product in enumerate(products, 1):
        print(f"{i}. {product[1]}")
    try:
        opcion = int(input("\nSeleccione el producto que desea actualizar: "))
    except ValueError:
        print("\nOpcion no valida")
        input("\nEnter para salir")
        return
    if opcion < 1 or opcion > len(products):
        print("\nOpcion no valida")
        input("\nEnter para salir")
        return
    
    producto_actualizar = products[opcion - 1]
    
    print("""\n1. Nombre
2. Precio de compra
3. Precio de venta
4. Stock""")
    select = input("\nSeleccione la opcion que desea actualizar: ")
    
    if select == "1":
        nombre = input("\nIntroduzca el nombre nuevo: ")
        if nombre:
            productos.actualizar_producto(producto_actualizar[0], 'nombre', nombre)
        else:
            print("\nOpcion no valida")
            input("\nEnter para salir")
            return
    elif select == "2":
        try:
            precio_compra = float(input("\nIntroduzca precio de compra nuevo: "))
        except ValueError:
            print("\nError debe introducir un numero")
            input("\nEnter para salir") 
            return
        if precio_compra:
            productos.actualizar_producto(producto_actualizar[0], 'precio_compra', precio_compra)
        else:
            print("\nOpcion no valida")
            input("\nEnter para salir")
            return
    elif select == "3":
        try:
            precio_venta = float(input("\nIntroduzca precio de venta nuevo: "))
        except ValueError:
            print("\nError debe introducir un numero")
            input("\nEnter para salir") 
            return
        if precio_venta:
            productos.actualizar_producto(producto_actualizar[0], 'precio_venta', precio_venta) 
        else:
            print("\nOpcion no valida")
            input("\nEnter para salir")
            return
    elif select == "4":
        print("\n1. Aumentar\n2. Disminuir")
        opcion_stock = input("\nSeleccione la opcion que desea realizar: ")
        if opcion_stock == "1":
            try:
                stock = int(input("\nIntroduzca la cantidad que desea aumentar: "))
            except ValueError:
                print("\nError debe introducir un numero")
                input("\nEnter para salir") 
                return
            if stock > 0:
                obs = input("\nIntroduzca el motivo de la actualizacion: ")
                stock_actual = productos.buscar_stock(producto_actualizar[0])[0]
                productos.actualizar_producto(producto_actualizar[0], 'stock', stock_actual + stock) 
                movimientos.crear_movimiento_inventario(producto_actualizar[0], 'Ajuste', None, stock, obs)
            else: 
                print("\nLa cantidad debe ser positiva")
                input("\nEnter para salir") 
                return                
        elif opcion_stock == "2":
            try:
                stock = int(input("\nIntroduzca la cantidad que desea disminuir: "))
            except ValueError:
                print("\nError debe introducir un numero")
                input("\nEnter para salir") 
                return
            if stock > 0:
                obs = input("\nIntroduzca el motivo de la actualizacion: ")
                stock_actual = productos.buscar_stock(producto_actualizar[0])[0]
                productos.actualizar_producto(producto_actualizar[0], 'stock', stock_actual - stock) 
                movimientos.crear_movimiento_inventario(producto_actualizar[0], 'Ajuste', None, -stock, obs)
    
            else:
                print("\nLa cantidad debe ser positiva")
                input("\nEnter para salir")  
                return 
        else:
            print("\nOpcion no valida")
            input("\nEnter para salir")   
            return 
    else:
        print("\nOpcion no valida")
        input("\nEnter para salir")
        return
    
    print("\nProducto actualizado correctamente")
    input("\nEnter para continuar")         
        
    
    
    