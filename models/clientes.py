from database import conectar


def crear_cliente(telefono, nombre, direccion, observaciones, precio_mensajeria):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO clientes(telefono, nombre, direccion, observaciones, precio_mensajeria) 
                   VALUES(%s, %s, %s, %s, %s) RETURNING cliente_id
                   """, (telefono, nombre, direccion, observaciones, precio_mensajeria,))
    cliente_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return cliente_id
       
def buscar_cliente(telefono):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM clientes WHERE telefono = %s                 
                   """, (telefono,))
    
    cliente = cursor.fetchone()
    conn.close()
    return cliente
 
def buscar_cliente_nombre():
    buscar = input('Buscar nombre del cliente: ')
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM clientes WHERE nombre ILIKE %s
                   """, (f"%{buscar}%",)) 
    filas = cursor.fetchall()
    conn.close()
    return filas
    
def buscar_cliente_id(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM clientes WHERE cliente_id = %s                 
                   """, (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente 
           
def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT cliente_id, nombre, telefono FROM clientes
                   """)
    filas = cursor.fetchall()
    conn.close()
    return filas
      
def eliminar_cliente(telefono):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   DELETE FROM clientes WHERE telefono = %s
                   """, (telefono,))
    conn.commit()
    conn.close()
    
def actualizar_cliente(telefono, columna, valor):
    columnas_permitidas = [
        'telefono',
        'nombre',
        'direccion',
        'observaciones',
        'precio_mensajeria'
    ]
    if columna not in columnas_permitidas:
        raise ValueError('Columna no permitida')
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"""
                   UPDATE clientes SET {columna} = %s WHERE telefono = %s
                   """, (valor, telefono,))
    conn.commit()
    conn.close()