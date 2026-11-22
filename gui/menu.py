from colorama import just_fix_windows_console, Fore, Style
from datetime import datetime
from models import mensajerias, pedidos
from gui import pedidos_gui, compras_gui, proveedores_gui, clientes_gui, productos_gui, mensajerias_gui, mensajeros_gui, reportes_gui


just_fix_windows_console()

def limpiar():
    print("\033[H\033[J", end="")

def mostrar_menu_principal(pedidos_pendientes, mensajerias_pendientes):
    limpiar()

    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
    print(Fore.CYAN + "╔════════════════════════════════════════════╗")
    print(Fore.CYAN + "║      SISTEMA DE GESTIÓN DULCE TRADICIÓN    ║")
    print(Fore.CYAN + "╚════════════════════════════════════════════╝")

    print()
    print(Fore.WHITE + f"📅 Fecha y hora: {fecha_hora}")
    print()

    print(Fore.BLUE + f"🛒 Pedidos pendientes: {pedidos_pendientes}")
    print(Fore.MAGENTA + f"🚚 Mensajerías pendientes: {mensajerias_pendientes}")

    print(Fore.CYAN + "──────────────────────────────────────")

    print(Fore.BLUE + "[1] 📋 Pedidos")
    print(Fore.MAGENTA + "[2] 🚚 Mensajerías")
    print(Fore.YELLOW + "[3] 🛒 Compras")
    print(Fore.GREEN + "[4] 📦 Productos")
    print(Fore.CYAN + "[5] 👤 Clientes")
    print(Fore.LIGHTBLUE_EX + "[6] 🛵 Mensajeros")
    print(Fore.LIGHTMAGENTA_EX + "[7] 📈 Reportes")
    print(Fore.RED + "[0] ❌ Salir")


    print(Fore.CYAN + "──────────────────────────────────────")

    opcion = input(Fore.WHITE + Style.BRIGHT + "Seleccione una opción: ")

    return opcion

def menu_principal():

    while True:
        pedidos_pendientes = len(pedidos.listar_pedidos_reservados()) 
        mensajerias_pendientes = len(mensajerias.listar_mensajerias_pendientes())
        opcion = mostrar_menu_principal(pedidos_pendientes, mensajerias_pendientes)

        if opcion == "1":
            menu_principal_pedidos()

        elif opcion == "2":
            menu_mensajerias()

        elif opcion == "3":
            menu_compras()

        elif opcion == "4":
            menu_productos()

        elif opcion == "5":
            menu_clientes()

        elif opcion == "6":
            menu_mensajeros()

        elif opcion == "7":
            menu_reportes()

        elif opcion == "0":
            print("\nGracias por utilizar el sistema.")
            break

        else:
            print("\n❌ Opción no válida.")
            input("\nPresione ENTER para continuar...")

def mostrar_menu_pedidos(pedidos_pendientes, mensajerias_pendientes):
    limpiar()

    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
    print(Fore.CYAN + "════════════════════════════════════════════")
    print(Fore.CYAN + "                   PEDIDOS                  ")
    print(Fore.CYAN + "════════════════════════════════════════════")

    print()
    print(Fore.WHITE + f"📅 Fecha y hora: {fecha_hora}")
    print()

    print(Fore.BLUE + f"🛒 Pedidos pendientes: {pedidos_pendientes}")
    print(Fore.MAGENTA + f"🚚 Mensajerías pendientes: {mensajerias_pendientes}")

    print(Fore.CYAN + "──────────────────────────────────────")
        
    print(Fore.BLUE + "[1] Crear pedido")
    print(Fore.MAGENTA + "[2] Gestionar pedidos")
    print(Fore.YELLOW + "[3] Ver pendientes")
    print()
    print(Fore.RED + "[0] Volver al menú principal")
    print()
        
    print(Fore.CYAN + "──────────────────────────────────────")
    opcion = input(Fore.WHITE + Style.BRIGHT + "Seleccione una opción: ")
        
    return opcion

def menu_principal_pedidos(): 
    
    while True:
        pedidos_pendientes = len(pedidos.listar_pedidos_reservados()) 
        mensajerias_pendientes = len(mensajerias.listar_mensajerias_pendientes())   
        opcion = mostrar_menu_pedidos(pedidos_pendientes, mensajerias_pendientes)
        
        if opcion == "1":
            pedidos_gui.opcion_pedido()
        elif opcion == "2":
            pedidos_gui.opcion_gestionar()
        elif opcion == "3":
            pedidos_gui.lista_pedidos_pendientes()    
        elif opcion == "0":
            return
        else:
            print("\n❌ Opción no válida.")
            input("\nPresione ENTER para continuar...")
 
def mostrar_menu_compras(pedidos_pendientes, mensajerias_pendientes):
    limpiar()

    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
    print(Fore.CYAN + "════════════════════════════════════════════")
    print(Fore.CYAN + "                   COMPRAS                  ")
    print(Fore.CYAN + "════════════════════════════════════════════")

    print()
    print(Fore.WHITE + f"📅 Fecha y hora: {fecha_hora}")
    print()

    print(Fore.BLUE + f"🛒 Pedidos pendientes: {pedidos_pendientes}")
    print(Fore.MAGENTA + f"🚚 Mensajerías pendientes: {mensajerias_pendientes}")

    print(Fore.CYAN + "──────────────────────────────────────")

    print(Fore.BLUE + "[1] Crear compra")
    print(Fore.MAGENTA + "[2] Ver compras")
    print(Fore.YELLOW + "[3] Ver detalle de compra")
    print(Fore.GREEN + "[4] Elimirar compras")
    print(Fore.CYAN + "[5] Editar compra")
    print(Fore.LIGHTBLUE_EX + "[6] Proveddores")
    print(Fore.RED + "[0] ❌ Salir")


    print(Fore.CYAN + "──────────────────────────────────────")

    opcion = input(Fore.WHITE + Style.BRIGHT + "Seleccione una opción: ")

    return opcion
    
def menu_compras():
    while True:
        pedidos_pendientes = len(pedidos.listar_pedidos_reservados()) 
        mensajerias_pendientes = len(mensajerias.listar_mensajerias_pendientes())
        opcion = mostrar_menu_compras(pedidos_pendientes, mensajerias_pendientes)

        if opcion == "1":
            compras_gui.opcion_compra()
            
        elif opcion == "2":
            compras_gui.ver_compras()
            
        elif opcion == "3":
            compras_gui.ver_detalle_compra()

        elif opcion == "4":
            compras_gui.eliminar_compra()

        elif opcion == "5":
            compras_gui.actualizar_compra()            

        elif opcion == "6":
            menu_proveedor()

        elif opcion == "0":
            return

        else:
            print("\n❌ Opción no válida.")
            input("\nPresione ENTER para continuar...")

def mostrar_menu_proveedor(pedidos_pendientes, mensajerias_pendientes):
    limpiar()

    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
    print(Fore.CYAN + "════════════════════════════════════════════")
    print(Fore.CYAN + "                PROVEEDORES                 ")
    print(Fore.CYAN + "════════════════════════════════════════════")

    print()
    print(Fore.WHITE + f"📅 Fecha y hora: {fecha_hora}")
    print()

    print(Fore.BLUE + f"🛒 Pedidos pendientes: {pedidos_pendientes}")
    print(Fore.MAGENTA + f"🚚 Mensajerías pendientes: {mensajerias_pendientes}")

    print(Fore.CYAN + "──────────────────────────────────────")

    print(Fore.BLUE + "[1] Crear proveedor")
    print(Fore.MAGENTA + "[2] Ver proveedores")
    print(Fore.YELLOW + "[3] Elimirar proveedor")
    print(Fore.GREEN + "[4] Editar proveedor")
    print(Fore.RED + "[0] ❌ Salir")


    print(Fore.CYAN + "──────────────────────────────────────")

    opcion = input(Fore.WHITE + Style.BRIGHT + "Seleccione una opción: ")

    return opcion    

def menu_proveedor():
    while True:
        pedidos_pendientes = len(pedidos.listar_pedidos_reservados()) 
        mensajerias_pendientes = len(mensajerias.listar_mensajerias_pendientes())
        opcion = mostrar_menu_proveedor(pedidos_pendientes, mensajerias_pendientes)

        if opcion == "1":
            proveedores_gui.crear_proveedor()
            
        elif opcion == "2":
            proveedores_gui.ver_proveedores()

        elif opcion == "3":
            proveedores_gui.eliminar_proveedor()

        elif opcion == "4":
            proveedores_gui.editar_proveedor()           

        elif opcion == "0":
            return

        else:
            print("\n❌ Opción no válida.")
            input("\nPresione ENTER para continuar...")        

def mostrar_menu_clientes(pedidos_pendientes, mensajerias_pendientes):
    limpiar()

    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
    print(Fore.CYAN + "════════════════════════════════════════════")
    print(Fore.CYAN + "                  CLIENTES                  ")
    print(Fore.CYAN + "════════════════════════════════════════════")

    print()
    print(Fore.WHITE + f"📅 Fecha y hora: {fecha_hora}")
    print()

    print(Fore.BLUE + f"🛒 Pedidos pendientes: {pedidos_pendientes}")
    print(Fore.MAGENTA + f"🚚 Mensajerías pendientes: {mensajerias_pendientes}")

    print(Fore.CYAN + "──────────────────────────────────────")

    print(Fore.BLUE + "[1] Crear cliente")
    print(Fore.MAGENTA + "[2] Ver clientes")
    print(Fore.YELLOW + "[3] Buscar cliente por telefono")
    print(Fore.GREEN + "[4] Buscar clientes por nombre")
    print(Fore.CYAN + "[5] Elimirar clientes")
    print(Fore.LIGHTBLUE_EX + "[6] Editar clientes")
    print(Fore.RED + "[0] ❌ Salir")


    print(Fore.CYAN + "──────────────────────────────────────")

    opcion = input(Fore.WHITE + Style.BRIGHT + "Seleccione una opción: ")

    return opcion
 
def menu_clientes():
    while True:
        pedidos_pendientes = len(pedidos.listar_pedidos_reservados()) 
        mensajerias_pendientes = len(mensajerias.listar_mensajerias_pendientes())
        opcion = mostrar_menu_clientes(pedidos_pendientes, mensajerias_pendientes)

        if opcion == "1":
            clientes_gui.agregar_cliente()
            
        elif opcion == "2":
            clientes_gui.ver_clientes()

        elif opcion == "3":
            clientes_gui.buscar_info_cliente()
            
        elif opcion == "4":
            clientes_gui.buscar_cliente_nombre()

        elif opcion == "5":
            clientes_gui.eliminar_cliente()

        elif opcion == "6":
            clientes_gui.editar_cliente()           

        elif opcion == "0":
            return

        else:
            print("\n❌ Opción no válida.")
            input("\nPresione ENTER para continuar...") 

def mostrar_menu_productos(pedidos_pendientes, mensajerias_pendientes):
    limpiar()

    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
    print(Fore.CYAN + "════════════════════════════════════════════")
    print(Fore.CYAN + "                  PRODUCTOS                 ")
    print(Fore.CYAN + "════════════════════════════════════════════")

    print()
    print(Fore.WHITE + f"📅 Fecha y hora: {fecha_hora}")
    print()

    print(Fore.BLUE + f"🛒 Pedidos pendientes: {pedidos_pendientes}")
    print(Fore.MAGENTA + f"🚚 Mensajerías pendientes: {mensajerias_pendientes}")

    print(Fore.CYAN + "──────────────────────────────────────")

    print(Fore.BLUE + "[1] Crear producto")
    print(Fore.MAGENTA + "[2] Ver productos")
    print(Fore.YELLOW + "[3] Eliminar producto")
    print(Fore.GREEN + "[4] Editar producto")
    print(Fore.RED + "[0] ❌ Salir")


    print(Fore.CYAN + "──────────────────────────────────────")

    opcion = input(Fore.WHITE + Style.BRIGHT + "Seleccione una opción: ")

    return opcion
        
def menu_productos():
    while True:
        pedidos_pendientes = len(pedidos.listar_pedidos_reservados()) 
        mensajerias_pendientes = len(mensajerias.listar_mensajerias_pendientes())
        opcion = mostrar_menu_productos(pedidos_pendientes, mensajerias_pendientes)

        if opcion == "1":
            productos_gui.crear_producto()
            
        elif opcion == "2":
            productos_gui.ver_productos()

        elif opcion == "3":
            productos_gui.eliminar_producto()

        elif opcion == "4":
            productos_gui.editar_producto()           

        elif opcion == "0":
            return

        else:
            print("\n❌ Opción no válida.")
            input("\nPresione ENTER para continuar...") 
 
def mostrar_menu_mensajeria(pedidos_pendientes, mensajerias_pendientes):
    limpiar()

    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
    print(Fore.CYAN + "════════════════════════════════════════════")
    print(Fore.CYAN + "                MENSAJERIAS                 ")
    print(Fore.CYAN + "════════════════════════════════════════════")

    print()
    print(Fore.WHITE + f"📅 Fecha y hora: {fecha_hora}")
    print()

    print(Fore.BLUE + f"🛒 Pedidos pendientes: {pedidos_pendientes}")
    print(Fore.MAGENTA + f"🚚 Mensajerías pendientes: {mensajerias_pendientes}")

    print(Fore.CYAN + "──────────────────────────────────────")
        
    print(Fore.BLUE + "[1] Crear mensajeria")
    print(Fore.MAGENTA + "[2] Gestionar mensajerias")
    print(Fore.YELLOW + "[3] Ver pendientes")
    print(Fore.GREEN + "[4] Ver enviadas")
    print(Fore.CYAN + "[5] Ver detalle de mensajeria")
    print(Fore.LIGHTBLUE_EX + "[6] Cambiar estado")

    print()
    print(Fore.RED + "[0] Volver al menú principal")
    print()
        
    print(Fore.CYAN + "──────────────────────────────────────")
    opcion = input(Fore.WHITE + Style.BRIGHT + "Seleccione una opción: ")
        
    return opcion
     
def menu_mensajerias():
    
    while True:
        pedidos_pendientes = len(pedidos.listar_pedidos_reservados()) 
        mensajerias_pendientes = len(mensajerias.listar_mensajerias_pendientes())   
        opcion = mostrar_menu_mensajeria(pedidos_pendientes, mensajerias_pendientes)
        
        if opcion == "1":
            mensajerias_gui.opcion_mensajeria()
        elif opcion == "2":
            mensajerias_gui.opcion_gestionar()
        elif opcion == "3":
            mensajerias_gui.lista_mensajerias_pendientes()  
        elif opcion == "4":
            mensajerias_gui.lista_mensajerias_enviadas()
        elif opcion == "5":
            mensajerias_gui.lista_detalle_mensajeria()  
        elif opcion == "6":
            mensajerias_gui.cambiar_estado()              
        elif opcion == "0":
            return
        else:
            print("\n❌ Opción no válida.")
            input("\nPresione ENTER para continuar...")
            
def mostrar_menu_mensajeros(pedidos_pendientes, mensajerias_pendientes):
    limpiar()

    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
    print(Fore.CYAN + "════════════════════════════════════════════")
    print(Fore.CYAN + "                 MENSAJEROS                 ")
    print(Fore.CYAN + "════════════════════════════════════════════")

    print()
    print(Fore.WHITE + f"📅 Fecha y hora: {fecha_hora}")
    print()

    print(Fore.BLUE + f"🛒 Pedidos pendientes: {pedidos_pendientes}")
    print(Fore.MAGENTA + f"🚚 Mensajerías pendientes: {mensajerias_pendientes}")

    print(Fore.CYAN + "──────────────────────────────────────")

    print(Fore.BLUE + "[1] Crear mensajero")
    print(Fore.MAGENTA + "[2] Ver mensajeros")
    print(Fore.YELLOW + "[3] Buscar mensajero por nombre")
    print(Fore.GREEN + "[4] Elimirar mensajero")
    print(Fore.CYAN + "[5] Editar mensajero")
    print(Fore.RED + "[0] ❌ Salir")


    print(Fore.CYAN + "──────────────────────────────────────")

    opcion = input(Fore.WHITE + Style.BRIGHT + "Seleccione una opción: ")

    return opcion

def menu_mensajeros():
    while True:
        pedidos_pendientes = len(pedidos.listar_pedidos_reservados()) 
        mensajerias_pendientes = len(mensajerias.listar_mensajerias_pendientes())
        opcion = mostrar_menu_mensajeros(pedidos_pendientes, mensajerias_pendientes)

        if opcion == "1":
            mensajeros_gui.crear_mensajero()
            
        elif opcion == "2":
            mensajeros_gui.ver_mensajeros()
            
        elif opcion == "3":
            mensajeros_gui.buscar_mensajero()

        elif opcion == "4":
            mensajeros_gui.eliminar_mensajero()

        elif opcion == "5":
            mensajeros_gui.editar_mensajero()           

        elif opcion == "0":
            return

        else:
            print("\n❌ Opción no válida.")
            input("\nPresione ENTER para continuar...") 
            
def mostrar_menu_reportes(pedidos_pendientes, mensajerias_pendientes):
    limpiar()

    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
    print(Fore.CYAN + "════════════════════════════════════════════")
    print(Fore.CYAN + "                  REPORTES                  ")
    print(Fore.CYAN + "════════════════════════════════════════════")

    print()
    print(Fore.WHITE + f"📅 Fecha y hora: {fecha_hora}")
    print()

    print(Fore.BLUE + f"🛒 Pedidos pendientes: {pedidos_pendientes}")
    print(Fore.MAGENTA + f"🚚 Mensajerías pendientes: {mensajerias_pendientes}")

    print(Fore.CYAN + "──────────────────────────────────────")

    print(Fore.BLUE + "[1] Reportes de hoy")
    print(Fore.MAGENTA + "[2] Reporte de una fecha")
    print(Fore.YELLOW + "[3] Reporte entre fechas")
    print(Fore.GREEN + "[4] Productos que mas ganancias generan")
    print(Fore.CYAN + "[5] Historial de movimientos de inventario")
    print(Fore.RED + "[0] ❌ Salir")


    print(Fore.CYAN + "──────────────────────────────────────")

    opcion = input(Fore.WHITE + Style.BRIGHT + "Seleccione una opción: ")

    return opcion
    
def menu_reportes():
    while True:
        pedidos_pendientes = len(pedidos.listar_pedidos_reservados()) 
        mensajerias_pendientes = len(mensajerias.listar_mensajerias_pendientes())
        opcion = mostrar_menu_reportes(pedidos_pendientes, mensajerias_pendientes)

        if opcion == "1":
            reportes_gui.reportes_hoy()
            
        elif opcion == "2":
            reportes_gui.reportes_fecha()
            
        elif opcion == "3":
            reportes_gui.reporte_entre()

        elif opcion == "4":
            reportes_gui.productos_ganacias()
            
        elif opcion == "5":
            reportes_gui.historial()           

        elif opcion == "0":
            return

        else:
            print("\n❌ Opción no válida.")
            input("\nPresione ENTER para continuar...") 