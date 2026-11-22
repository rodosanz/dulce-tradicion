from database import conectar


def crear_compra(total, observaciones, proveedor_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO compras(total, observaciones, proveedor_id)
                   VALUES(%s, %s, %s) RETURNING compra_id
                   """, (total, observaciones, proveedor_id,))
    compra_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return compra_id
        
def crear_detalle_compra(compra_id, producto_id, cantidad, precio_compra):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO detalle_compras(compra_id, producto_id, cantidad, precio_compra)
                   VALUES(%s, %s, %s, %s)
                   """, (compra_id, producto_id, cantidad, precio_compra,))
    conn.commit()
    conn.close()
    
def eliminar_compra(compra_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   DELETE FROM compras WHERE compra_id = %s
                   """, (compra_id,))   
    conn.commit()
    conn.close()   
    
def eliminar_detalle_compra(compra_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   DELETE FROM detalle_compras WHERE compra_id = %s
                   """, (compra_id,))   
    conn.commit()
    conn.close() 
    
def actualizar_compra(compra_id, columna, valor):
    columnas_permitidas = [
        'total',
        'fecha',
        'observaciones'
    ]
    if columna not in columnas_permitidas:
        raise ValueError('Columna no permitida')
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"""
                   UPDATE compras SET {columna} = %s WHERE compra_id = %s
                   """, (valor, compra_id,))
    conn.commit()
    conn.close() 
      
def actualizar_detalle_compra(detalle_compra_id, columna, valor):
    columnas_permitidas = [
        'compra_id',
        'producto_id',
        'cantidad',
        'precio_compra',
        'proveedor_id'
    ]
    if columna not in columnas_permitidas:
        raise ValueError('Columna no permitida')
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"""
                   UPDATE detalle_compras SET {columna} = %s WHERE detalle_compra_id = %s
                   """, (valor, detalle_compra_id,))
    conn.commit()
    conn.close() 
       
def listar_compra():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT c.compra_id, p.nombre, c.total, c.fecha, c.observaciones FROM compras c LEFT JOIN proveedores p
                   ON c.proveedor_id = p.proveedor_id 
                   """)
    filas = cursor.fetchall()
    conn.close()
    return filas        
    
def listar_detalle_compra(compra_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT p.producto_id, p.nombre, p.precio_venta, p.stock, dc.precio_compra, dc.cantidad
                   FROM detalle_compras dc LEFT JOIN productos p 
                   ON dc.producto_id = p.producto_id
                   WHERE compra_id = %s
                   """, (compra_id,))
    filas = cursor.fetchall()
    conn.close()
    return filas 

def buscar_compra(compra_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM compras WHERE compra_id = %s
                   """, (compra_id,))
    filas = cursor.fetchone()
    conn.close()
    return filas