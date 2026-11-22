from database import conectar


def crear_movimiento_inventario(producto_id, tipo, referencia_id, cantidad, observaciones):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO movimientos_inventario(producto_id, tipo, referencia_id, cantidad, observaciones)
                   VALUES(%s, %s, %s, %s, %s)
                   """, (producto_id, tipo, referencia_id, cantidad, observaciones,))
    conn.commit()
    conn.close()
    
    
def eliminar_movimiento_inventario(inventario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   DELETE FROM movimientos_inventario WHERE inventario_id = %s
                   """, (inventario_id,))
    conn.commit()
    conn.close()
       
    
def actualizar_movimiento_inventario(inventario_id, columna, valor):
    columnas_permitidas = [
        'producto_id',
        'tipo',
        'referencia_id',
        'cantidad',
        'fecha'
    ]
    if columna not in columnas_permitidas:
        raise ValueError('Columna no permitida')
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"""
                   UPDATE movimientos_inventario SET {columna} = %s WHERE inventario_id = %s
                   """, (valor, inventario_id,))  
    conn.commit()
    conn.close() 
    
    
def listar_movimientos_inventario():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""SELECT m.inventario_id, p.nombre, m.tipo, m.referencia_id, m.cantidad, m.observaciones, m.fecha 
                   FROM movimientos_inventario m LEFT JOIN productos p
                   ON m.producto_id = p.producto_id
                   ORDER BY m.fecha""")
    filas = cursor.fetchall()
    conn.close()
    return filas