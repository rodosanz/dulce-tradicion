from database import conectar


def crear_proveedor(nombre, telefono):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO proveedores(nombre, telefono)
                   VALUES(%s, %s)
                   """, (nombre, telefono,))
    conn.commit()
    conn.close()
      
def eliminar_proveedor(proveedor_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   DELETE FROM proveedores WHERE proveedor_id = %s
                   """, (proveedor_id,))
    conn.commit()
    conn.close()
    
def actualizar_proveedor(proveedor_id, columna, valor):
    columnas_permitidas = [
        'nombre',
        'telefono'
    ]
    if columna not in columnas_permitidas:
        raise ValueError('Columna no permitida')
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"""
                   UPDATE proveedores SET {columna} = %s WHERE proveedor_id = %s
                   """, (valor, proveedor_id,))
    conn.commit()
    conn.close()
       
def listar_proveedores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM proveedores ORDER BY proveedor_id
                   """)
    filas = cursor.fetchall()
    conn.close()
    return filas

def buscar_proveedor(proveedor_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM proveedores WHERE proveedor_id = %s
                   """, (proveedor_id,))
    filas = cursor.fetchone()
    conn.close()
    return filas

def buscar_proveedor_nombre():
    buscar = input("Buscar nombre de proveedor: ")
    conn = conectar()
    cursor =  conn.cursor()
    cursor.execute("""
                   SELECT * FROM proveedores WHERE nombre ILIKE %s
                   """, (f"%{buscar}%",))
    filas = cursor.fetchall()
    conn.close()
    return filas