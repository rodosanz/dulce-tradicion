from database import conectar


def crear_producto(nombre, precio_compra, precio_venta):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO productos(nombre, precio_compra, precio_venta)
            VALUES(%s, %s, %s)
        """, (nombre, precio_compra, precio_venta,)
    )
    conn.commit()
    conn.close()

def actualizar_producto(producto_id, columna, valor):
    columnas_permitidas = ['nombre', 'precio_compra', 'precio_venta', 'stock']
    if columna not in columnas_permitidas:
        raise ValueError('Columna no permitida')
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"""
                   UPDATE productos SET {columna} = %s WHERE producto_id = %s
                   """, (valor, producto_id,))
    conn.commit()
    conn.close()

def eliminar_producto(producto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   DELETE FROM productos WHERE producto_id = %s
                   """, (producto_id,))
    conn.commit()
    conn.close()

def listar_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM productos ORDER BY stock DESC'
    )
    filas = cursor.fetchall()  
    conn.close()
    return filas

def buscar_producto():
    buscar = input('Buscar producto: ')
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT producto_id, nombre, precio_venta, stock, precio_compra FROM productos WHERE nombre ILIKE %s
                   """, (f"%{buscar}%",)) 
    filas = cursor.fetchall()
    conn.close()
    return filas

def buscar_stock(producto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT stock FROM productos WHERE producto_id = %s
                   """, (producto_id,))
    filas = cursor.fetchone()
    conn.close()
    return filas