from database import conectar

def crear_mensajero(nombre, telefono):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO mensajeros(nombre, telefono)
                   VALUES(%s, %s)
                   """, (nombre, telefono,))
    conn.commit()
    conn.close
    
def eliminar_mensajero(mensajero_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   DELETE FROM mensajeros WHERE mensajero_id = %s
                   """, (mensajero_id,))
    conn.commit()
    conn.close   
    
def actualizar_mensajero(mensajero_id, columna, valor):
    columnas_permitidas = [
        'nombre',
        'telefono'
    ]
    if columna not in columnas_permitidas:
        raise ValueError('Columna no permitida')
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"""
                   UPDATE mensajeros SET {columna} = %s WHERE mensajero_id = %s
                   """, (valor, mensajero_id,))
    conn.commit()
    conn.close()
    
def listar_mensajeros():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM mensajeros
                   """)
    filas = cursor.fetchall()
    conn.close()  
    return filas

def buscar_mensajero_nombre():
    buscar = input('Buscar nombre del mensajero: ')
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM mensajeros WHERE nombre ILIKE %s
                   """, (f"%{buscar}%",)) 
    filas = cursor.fetchall()
    conn.close()
    return filas

def buscar_mensajero(mensajero_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM mensajeros WHERE mensajero_id = %s                 
                   """, (mensajero_id,))  
    cliente = cursor.fetchone()
    conn.close()
    return cliente