from models import movimientos, reportes
from tabulate import tabulate
from datetime import datetime


def limpiar():
    print("\033[H\033[J", end="")

def historial():
    limpiar() 
    lista_movimientos = movimientos.listar_movimientos_inventario()
    print(tabulate(
        lista_movimientos,
        headers=['Inventario_ID', 'Producto', 'Tipo', 'Referencia', 'Cantidad', 'Observaciones', 'Fecha'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")
    
def reportes_hoy():
    limpiar()
    report_pedidos = reportes.reportes_hoy_pedidos()
    productos_venta = reportes.productos_vendidos()
    ganancia_pedidos = reportes.ganancias_pedidos()
    report_mensajeria = reportes.reportes_hoy_mensajerias()
    ganancia_mensajeria = reportes.ganancias_mensajerias()
    print("=====================================")
    print("           REPORTES DE HOY           ")
    print("=====================================")
    print()
    print("Ventas:")
    print("--------")
    print("Ingresos: $", report_pedidos[0])
    print("Cantidad de ventas: ", report_pedidos[1])
    print("Ganacias: $", ganancia_pedidos[0])
    print()
    print("Mensajerias:")
    print("-------------")
    print("Ingresos: $", report_mensajeria[0])
    print("Cantidad de mensajerias: ", report_mensajeria[1])
    print("Ganancias: $", ganancia_mensajeria[0])
    print()
    print("Total del dia:")
    print("--------------")
    print("Ingresos: $", report_mensajeria[0] + report_pedidos[0])
    print("Cantidad de ventas total: ", report_mensajeria[1] + report_pedidos[1])
    print("Ganancias: $", ganancia_mensajeria[0] + ganancia_pedidos[0])   

    print(tabulate(
        productos_venta,
        headers=['Producto', 'Cantidad vendida'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")
    
def reportes_fecha():
    limpiar()
    fecha = input("Ingresa fecha (DD/MM/AAAA): ")
    try:
        fecha = datetime.strptime(fecha, "%d/%m/%Y").date()
    except ValueError:
        print("Fecha invalida")
        input("\nEnter para salir")
        return
            
    report_pedidos = reportes.reportes_fecha_pedidos(fecha)
    productos_venta = reportes.productos_fecha_vendidos(fecha)
    ganancia_pedidos = reportes.ganancias_fecha_pedidos(fecha)
    report_mensajeria = reportes.reportes_fecha_mensajerias(fecha)
    ganancia_mensajeria = reportes.ganancias_fecha_mensajerias(fecha)
    print("========================================")
    print(f"           REPORTES DE {fecha}           ")
    print("========================================")
    print()
    print("Ventas:")
    print("--------")
    print("Ingresos: $", report_pedidos[0])
    print("Cantidad de ventas: ", report_pedidos[1])
    print("Ganacias: $", ganancia_pedidos[0])
    print()
    print("Mensajerias:")
    print("-------------")
    print("Ingresos: $", report_mensajeria[0])
    print("Cantidad de mensajerias: ", report_mensajeria[1])
    print("Ganancias: $", ganancia_mensajeria[0])
    print()
    print("Total del dia:")
    print("--------------")
    print("Ingresos: $", report_mensajeria[0] + report_pedidos[0])
    print("Cantidad de ventas total: ", report_mensajeria[1] + report_pedidos[1])
    print("Ganancias: $", ganancia_mensajeria[0] + ganancia_pedidos[0])   

    print(tabulate(
        productos_venta,
        headers=['Producto', 'Cantidad vendida'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")  
    
def reporte_entre():
    limpiar()
    fecha_in = input("Ingresa fecha inicial (DD/MM/AAAA): ")
    try:
        fecha_in = datetime.strptime(fecha_in, "%d/%m/%Y").date()
    except ValueError:
        print("Fecha invalida")
        input("\nEnter para salir")
        return
    fecha_fin = input("Ingresa fecha final (DD/MM/AAAA): ")
    try:
        fecha_fin = datetime.strptime(fecha_fin, "%d/%m/%Y").date()
    except ValueError:
        print("Fecha invalida")
        input("\nEnter para salir")
        return
            
    report_pedidos = reportes.reportes_entre_pedidos(fecha_in, fecha_fin)
    productos_venta = reportes.productos_entre_vendidos(fecha_in, fecha_fin)
    ganancia_pedidos = reportes.ganancias_entre_pedidos(fecha_in, fecha_fin)
    report_mensajeria = reportes.reportes_entre_mensajerias(fecha_in, fecha_fin)
    ganancia_mensajeria = reportes.ganancias_entre_mensajerias(fecha_in, fecha_fin)
    print("========================================")
    print("                 REPORTES               ")
    print("========================================")
    print()
    print("Ventas:")
    print("--------")
    print("Ingresos: $", report_pedidos[0])
    print("Cantidad de ventas: ", report_pedidos[1])
    print("Ganacias: $", ganancia_pedidos[0])
    print()
    print("Mensajerias:")
    print("-------------")
    print("Ingresos: $", report_mensajeria[0])
    print("Cantidad de mensajerias: ", report_mensajeria[1])
    print("Ganancias: $", ganancia_mensajeria[0])
    print()
    print("Total del dia:")
    print("--------------")
    print("Ingresos: $", report_mensajeria[0] + report_pedidos[0])
    print("Cantidad de ventas total: ", report_mensajeria[1] + report_pedidos[1])
    print("Ganancias: $", ganancia_mensajeria[0] + ganancia_pedidos[0])   

    print(tabulate(
        productos_venta,
        headers=['Producto', 'Cantidad vendida'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")    
    
def productos_ganacias():
    limpiar()
    fecha_in = input("Ingresa fecha inicial (DD/MM/AAAA): ")
    try:
        fecha_in = datetime.strptime(fecha_in, "%d/%m/%Y").date()
    except ValueError:
        print("Fecha invalida")
        input("\nEnter para salir")
        return
    fecha_fin = input("Ingresa fecha final (DD/MM/AAAA): ")
    try:
        fecha_fin = datetime.strptime(fecha_fin, "%d/%m/%Y").date()
    except ValueError:
        print("Fecha invalida")
        input("\nEnter para salir")
        return
    
    generan_mas = reportes.productos_ganan_mas(fecha_in, fecha_fin)
    
    print("========================================")
    print("                 REPORTES               ")
    print("========================================")
    print()
    print(tabulate(
        generan_mas,
        headers=['Producto', 'Ganancias', 'Cantidad'],
        tablefmt='rounded_grid'
    ))
    input("\nEnter para salir")