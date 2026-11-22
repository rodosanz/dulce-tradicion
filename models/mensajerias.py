from database import conectar


def crear_mensajeria(cliente_id, estado, costo_mensajeria, total):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO mensajerias(cliente_id, estado, costo_mensajeria, total)
                   VALUES(%s, %s, %s, %s) RETURNING mensajeria_id
                   """, (cliente_id, estado, costo_mensajeria, total,))
    mensajeria_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return mensajeria_id
   
def detalle_mensajerias(mensajeria_id, producto_id, cantidad, precio_unitario, costo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO detalle_mensajerias(mensajeria_id, producto_id, cantidad, precio_unitario, costo)
                   VALUES(%s, %s, %s, %s, %s)
                   """, (mensajeria_id, producto_id, cantidad, precio_unitario, costo,))
    conn.commit()
    conn. close()
       
def eliminar_mensajeria(mensajeria_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   DELETE FROM mensajerias WHERE mensajeria_id = %s
                   """, (mensajeria_id,))
    conn.commit()
    conn.close()
    
def eliminar_detalle_mensajerias(mensajeria_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   DELETE FROM detalle_mensajerias WHERE mensajeria_id = %s
                   """, (mensajeria_id,))
    conn.commit()
    conn.close()
    
def actualizar_mensajeria(mensajeria_id, columna, valor):
    columnas_permitidas = [
        'telefono_cliente',
        'estado',
        'costo_mensajeria',
        'total',
        'fecha',
        'mensajero_id'
    ]
    if columna not in columnas_permitidas:
        raise ValueError('Columna no permitida')
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"""
                   UPDATE mensajerias SET {columna} = %s WHERE mensajeria_id = %s
                   """, (valor, mensajeria_id,))
    conn.commit()
    conn.close()    
    
def actualizar_detalle_mensajerias(detalle_mensajeria_id, columna, valor):
    columnas_permitidas = [
        'mensajeria_id',
        'producto_id',
        'cantidad',
        'precio_unitario'
    ]
    if columna not in columnas_permitidas:
        raise ValueError('Columna no permitida')

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"""
                   UPDATE detalle_mensajerias SET {columna} = %s WHERE detalle_mensajeria_id = %s
                   """, (valor, detalle_mensajeria_id,))
    conn.commit()
    conn.close()    
       
def listar_mensajerias():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT m.mensajeria_id, c.nombre, c.telefono, m.estado, m.costo_mensajeria, m.total, mj.nombre, m.fecha 
                   FROM mensajerias m LEFT JOIN clientes c
                   ON m.cliente_id = c.cliente_id
                   LEFT JOIN mensajeros mj
                   ON m.mensajero_id = mj.mensajero_id 
                   """)   
    filas = cursor.fetchall()
    conn.close()
    return filas

def listar_ultimas_mensajerias(limite):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT m.mensajeria_id, c.nombre, c.telefono, m.estado, m.costo_mensajeria, m.total, mj.nombre, m.fecha 
                   FROM mensajerias m LEFT JOIN clientes c
                   ON m.cliente_id = c.cliente_id
                   LEFT JOIN mensajeros mj
                   ON m.mensajero_id = mj.mensajero_id 
                   ORDER BY m.fecha DESC LIMIT %s
                   """, (limite,))   
    filas = cursor.fetchall()
    conn.close()
    return filas

def listar_detalle_mensajerias(mensajeria_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT p.producto_id, p.nombre, dm.precio_unitario, p.stock, p.precio_compra, dm.cantidad 
                   FROM detalle_mensajerias dm LEFT JOIN productos p ON dm.producto_id = p.producto_id
                   WHERE mensajeria_id = %s
                   """, (mensajeria_id,))   
    filas = cursor.fetchall()
    conn.close()
    return filas
   
def listar_mensajerias_pendientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT m.mensajeria_id, c.nombre, c.telefono, m.estado, m.costo_mensajeria, m.total, mj.nombre, m.fecha 
                   FROM mensajerias m LEFT JOIN clientes c
                   ON m.cliente_id = c.cliente_id 
                   LEFT JOIN mensajeros mj
                   ON m.mensajero_id = mj.mensajero_id 
                   WHERE estado = 'Pendiente'
                   """)   
    filas = cursor.fetchall()
    conn.close()
    return filas

def listar_mensajerias_enviadas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT m.mensajeria_id, c.nombre, c.telefono, m.estado, m.costo_mensajeria, m.total, mj.nombre, m.fecha 
                   FROM mensajerias m LEFT JOIN clientes c
                   ON m.cliente_id = c.cliente_id 
                   LEFT JOIN mensajeros mj
                   ON m.mensajero_id = mj.mensajero_id 
                   WHERE estado = 'Enviado'
                   """)   
    filas = cursor.fetchall()
    conn.close()
    return filas
    
def listar_mensajerias_entregadas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT m.mensajeria_id, c.nombre, c.telefono, m.estado, m.costo_mensajeria, m.total, mj.nombre, m.fecha 
                   FROM mensajerias m LEFT JOIN clientes c
                   ON m.cliente_id = c.cliente_id
                   LEFT JOIN mensajeros mj
                   ON m.mensajero_id = mj.mensajero_id  
                   WHERE estado = 'Entregado'
                   """)   
    filas = cursor.fetchall()
    conn.close()
    return filas

def listar_mensajeria_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT m.mensajeria_id, c.nombre, c.telefono, m.estado, m.costo_mensajeria, m.total, m.fecha 
                   FROM mensajerias m LEFT JOIN clientes c
                   ON m.cliente_id = c.cliente_id
                   WHERE m.cliente_id = %s
                   ORDER BY fecha
                   """, (cliente_id,))   
    filas = cursor.fetchall()
    conn.close()
    return filas   

def buscar_mensajeria(mensajeria_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM mensajerias WHERE mensajeria_id = %s
                   """, (mensajeria_id,))
    filas = cursor.fetchone()
    conn.close()
    return filas