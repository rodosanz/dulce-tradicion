from database import conectar


def crear_pedido(cliente_id, estado, total):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO ventas(cliente_id, estado, total)
                   VALUES(%s, %s, %s) RETURNING venta_id
                   """, (cliente_id, estado, total,))
    venta_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return venta_id
        
def crear_detalle_pedido(venta_id, producto_id, cantidad, precio_unitario, costo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO detalle_ventas(venta_id, producto_id, cantidad, precio_unitario, costo)
                   VALUES(%s, %s, %s, %s, %s)
                   """, (venta_id, producto_id, cantidad, precio_unitario, costo,))
    conn.commit()
    conn.close()
        
def eliminar_pedido(venta_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   DELETE FROM ventas WHERE venta_id = %s
                   """, (venta_id,))
    conn.commit()
    conn.close()
      
def eliminar_detalle_pedido(venta_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   DELETE FROM detalle_ventas WHERE venta_id = %s
                   """, (venta_id,))
    conn.commit()
    conn.close()
  
def listar_pedidos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""SELECT venta_id, estado, total, fecha FROM ventas ORDER BY fecha""")
    filas = cursor.fetchall()
    conn.close()
    return filas
 
def listar_ultimos_pedidos(limite):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""SELECT venta_id, estado, total, fecha FROM ventas ORDER BY fecha DESC LIMIT %s""", (limite,))
    filas = cursor.fetchall()
    conn.close()
    return filas
   
def listar_detalle_pedidos(venta_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT p.producto_id, p.nombre, dv.precio_unitario, p.stock, p.precio_compra, dv.cantidad 
                   FROM detalle_ventas dv LEFT JOIN productos p ON dv.producto_id = p.producto_id
                   WHERE venta_id = %s
                   """, (venta_id,))
    filas = cursor.fetchall()
    conn.close()
    return filas

def actualizar_pedido(venta_id, columna, valor):
    columnas_permitidas = [
        'cliente_id',
        'estado',
        'total',
        'fecha'
    ]
    if columna not in columnas_permitidas:
        raise ValueError('Columna no permitida')
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"""
                   UPDATE ventas SET {columna} = %s WHERE venta_id = %s
                   """, (valor, venta_id,))
    conn.commit()
    conn.close()
    
def actualizar_detalle_pedido(detalle_venta_id, columna, valor):
    columnas_permitidas = [
        'venta_id',
        'producto_id',
        'cantidad',
        'precio_unitario'
    ]
    if columna not in columnas_permitidas:
        raise ValueError('Columna no permitida')
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"""
                   UPDATE detalle_ventas SET {columna} = %s WHERE detalle_venta_id = %s
                   """, (valor, detalle_venta_id,))
    conn.commit()
    conn.close()
     
def listar_pedidos_reservados():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""SELECT v.venta_id, c.nombre, c.telefono, v.estado, v.total, v.fecha
                   FROM ventas V LEFT JOIN clientes C ON v.cliente_id = c.cliente_id
                   WHERE v.estado = 'Reservado' ORDER BY fecha""")
    filas = cursor.fetchall()
    conn.close()
    return filas

def buscar_pedido(pedido_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT venta_id, estado, cliente_id FROM ventas WHERE venta_id = %s
                   """, (pedido_id,))
    pedido = cursor.fetchone()
    conn.close()
    return pedido