from database import conectar


def reportes_hoy_pedidos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT COALESCE(SUM(total),0) AS total_dia, COUNT(*) cantidad
                   FROM ventas
                   WHERE DATE(fecha) = CURRENT_DATE AND estado <> 'Cancelado'
                   """)
    filas = cursor.fetchone()
    conn.close()
    return filas

def productos_vendidos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT nombre, COALESCE(SUM(vendidos),0) AS vendidos   
                    FROM (SELECT p.nombre, COALESCE(SUM(dv.cantidad),0) AS vendidos
                    FROM detalle_ventas dv
                    JOIN productos p
                    ON dv.producto_id = p.producto_id
                    JOIN ventas v
                    ON dv.venta_id = v.venta_id
                    WHERE DATE(v.fecha) = CURRENT_DATE AND v.estado <> 'Cancelado'
                    GROUP BY p.nombre
                    
                    UNION ALL
                    
                    SELECT p.nombre, COALESCE(SUM(dm.cantidad),0) AS vendidos
                    FROM detalle_mensajerias dm
                    JOIN productos p
                    ON dm.producto_id = p.producto_id
                    JOIN mensajerias m
                    ON dm.mensajeria_id = m.mensajeria_id
                    WHERE DATE(m.fecha) = CURRENT_DATE AND m.estado <> 'Cancelado'
                    GROUP BY p.nombre) t
                    GROUP BY nombre
                    ORDER BY vendidos DESC
                   """)
    filas = cursor.fetchall()
    conn.close()
    return filas   

def ganancias_pedidos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT COALESCE(SUM((dv.precio_unitario - dv.costo) * dv.cantidad),0)
                    FROM detalle_ventas dv
                    JOIN productos p
                    ON dv.producto_id = p.producto_id
                    JOIN ventas v
                    ON dv.venta_id = v.venta_id
                    WHERE DATE(v.fecha) = CURRENT_DATE AND v.estado <> 'Cancelado'
                   """)
    filas = cursor.fetchone()
    conn.close()
    return filas     

def reportes_hoy_mensajerias():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT COALESCE(SUM(total),0) AS total_dia, COUNT(*) cantidad
                   FROM mensajerias
                   WHERE DATE(fecha) = CURRENT_DATE AND estado <> 'Cancelado'
                   """)
    filas = cursor.fetchone()
    conn.close()
    return filas

def ganancias_mensajerias():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT COALESCE(SUM((dm.precio_unitario - dm.costo) * dm.cantidad),0)
                    FROM detalle_mensajerias dm
                    JOIN productos p
                    ON dm.producto_id = p.producto_id
                    JOIN mensajerias m
                    ON dm.mensajeria_id = m.mensajeria_id
                    WHERE DATE(m.fecha) = CURRENT_DATE AND m.estado <> 'Cancelado'
                   """)
    filas = cursor.fetchone()
    conn.close()
    return filas  

def reportes_fecha_pedidos(fecha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT COALESCE(SUM(total),0) AS total_dia, COUNT(*) cantidad
                   FROM ventas
                   WHERE DATE(fecha) = %s AND estado <> 'Cancelado'
                   """, (fecha,))
    filas = cursor.fetchone()
    conn.close()
    return filas

def productos_fecha_vendidos(fecha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT nombre, COALESCE(SUM(vendidos),0) AS vendidos   
                    FROM (SELECT p.nombre, COALESCE(SUM(dv.cantidad),0) AS vendidos
                    FROM detalle_ventas dv
                    JOIN productos p
                    ON dv.producto_id = p.producto_id
                    JOIN ventas v
                    ON dv.venta_id = v.venta_id
                    WHERE DATE(v.fecha) = %s AND v.estado <> 'Cancelado'
                    GROUP BY p.nombre
                    
                    UNION ALL
                    
                    SELECT p.nombre, COALESCE(SUM(dm.cantidad),0) AS vendidos
                    FROM detalle_mensajerias dm
                    JOIN productos p
                    ON dm.producto_id = p.producto_id
                    JOIN mensajerias m
                    ON dm.mensajeria_id = m.mensajeria_id
                    WHERE DATE(m.fecha) = %s AND m.estado <> 'Cancelado'
                    GROUP BY p.nombre) t
                    GROUP BY nombre
                    ORDER BY vendidos DESC
                   """, (fecha, fecha,))
    filas = cursor.fetchall()
    conn.close()
    return filas  

def ganancias_fecha_pedidos(fecha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT COALESCE(SUM((dv.precio_unitario - dv.costo) * dv.cantidad),0)
                    FROM detalle_ventas dv
                    JOIN productos p
                    ON dv.producto_id = p.producto_id
                    JOIN ventas v
                    ON dv.venta_id = v.venta_id
                    WHERE DATE(v.fecha) = %s AND v.estado <> 'Cancelado'
                   """, (fecha,))
    filas = cursor.fetchone()
    conn.close()
    return filas

def reportes_fecha_mensajerias(fecha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT COALESCE(SUM(total),0) AS total_dia, COUNT(*) cantidad
                   FROM mensajerias
                   WHERE DATE(fecha) = %s AND estado <> 'Cancelado'
                   """, (fecha,))
    filas = cursor.fetchone()
    conn.close()
    return filas

def ganancias_fecha_mensajerias(fecha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT COALESCE(SUM((dm.precio_unitario - dm.costo) * dm.cantidad),0)
                    FROM detalle_mensajerias dm
                    JOIN productos p
                    ON dm.producto_id = p.producto_id
                    JOIN mensajerias m
                    ON dm.mensajeria_id = m.mensajeria_id
                    WHERE DATE(m.fecha) = %s AND m.estado <> 'Cancelado'
                   """, (fecha,))
    filas = cursor.fetchone()
    conn.close()
    return filas

def reportes_entre_pedidos(fecha_in, fecha_fin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT COALESCE(SUM(total),0) AS total_dia, COUNT(*) cantidad
                   FROM ventas
                   WHERE (fecha BETWEEN %s AND %s) AND estado <> 'Cancelado'
                   """, (fecha_in, fecha_fin,))
    filas = cursor.fetchone()
    conn.close()
    return filas

def productos_entre_vendidos(fecha_in, fecha_fin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT nombre, COALESCE(SUM(vendidos),0) AS vendidos   
                    FROM (SELECT p.nombre, COALESCE(SUM(dv.cantidad),0) AS vendidos
                    FROM detalle_ventas dv
                    JOIN productos p
                    ON dv.producto_id = p.producto_id
                    JOIN ventas v
                    ON dv.venta_id = v.venta_id
                    WHERE (v.fecha BETWEEN %s AND %s) AND v.estado <> 'Cancelado'
                    GROUP BY p.nombre
                    
                    UNION ALL
                    
                    SELECT p.nombre, COALESCE(SUM(dm.cantidad),0) AS vendidos
                    FROM detalle_mensajerias dm
                    JOIN productos p
                    ON dm.producto_id = p.producto_id
                    JOIN mensajerias m
                    ON dm.mensajeria_id = m.mensajeria_id
                    WHERE (m.fecha BETWEEN %s AND %s) AND m.estado <> 'Cancelado'
                    GROUP BY p.nombre) t
                    GROUP BY nombre
                    ORDER BY vendidos DESC
                   """, (fecha_in, fecha_fin, fecha_in, fecha_fin,))
    filas = cursor.fetchall()
    conn.close()
    return filas  

def ganancias_entre_pedidos(fecha_in, fecha_fin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT COALESCE(SUM((dv.precio_unitario - dv.costo) * dv.cantidad),0)
                    FROM detalle_ventas dv
                    JOIN productos p
                    ON dv.producto_id = p.producto_id
                    JOIN ventas v
                    ON dv.venta_id = v.venta_id
                    WHERE (v.fecha BETWEEN %s AND %s) AND v.estado <> 'Cancelado'
                   """, (fecha_in, fecha_fin,))
    filas = cursor.fetchone()
    conn.close()
    return filas

def reportes_entre_mensajerias(fecha_in, fecha_fin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT COALESCE(SUM(total),0) AS total_dia, COUNT(*) cantidad
                   FROM mensajerias
                   WHERE (fecha BETWEEN %s AND %s) AND estado <> 'Cancelado'
                   """, (fecha_in, fecha_fin,))
    filas = cursor.fetchone()
    conn.close()
    return filas

def ganancias_entre_mensajerias(fecha_in, fecha_fin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT COALESCE(SUM((dm.precio_unitario - dm.costo) * dm.cantidad),0)
                    FROM detalle_mensajerias dm
                    JOIN productos p
                    ON dm.producto_id = p.producto_id
                    JOIN mensajerias m
                    ON dm.mensajeria_id = m.mensajeria_id
                    WHERE (m.fecha BETWEEN %s AND %s)  AND m.estado <> 'Cancelado'
                   """, (fecha_in, fecha_fin,))
    filas = cursor.fetchone()
    conn.close()
    return filas

def productos_ganan_mas(fecha_in, fecha_fin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT nombre, SUM(ganancias) AS ganancias, SUM(vendidos) AS vendidos   
                    FROM (SELECT p.nombre, SUM((dv.precio_unitario - dv.costo) * dv.cantidad) AS ganancias, SUM(dv.cantidad) AS vendidos
                    FROM detalle_ventas dv
                    JOIN productos p
                    ON dv.producto_id = p.producto_id
                    JOIN ventas v
                    ON dv.venta_id = v.venta_id
                    WHERE (v.fecha BETWEEN %s AND %s) AND v.estado <> 'Cancelado'
                    GROUP BY p.nombre
                    
                    UNION ALL
                    
                    SELECT p.nombre, SUM((dm.precio_unitario - dm.costo) * dm.cantidad) AS ganancias, SUM(dm.cantidad) AS vendidos
                    FROM detalle_mensajerias dm
                    JOIN productos p
                    ON dm.producto_id = p.producto_id
                    JOIN mensajerias m
                    ON dm.mensajeria_id = m.mensajeria_id
                    WHERE (m.fecha BETWEEN %s AND %s) AND m.estado <> 'Cancelado'
                    GROUP BY p.nombre) t
                    GROUP BY nombre
                    ORDER BY ganancias DESC
                   """, (fecha_in, fecha_fin, fecha_in, fecha_fin,))
    filas = cursor.fetchall()
    conn.close()
    return filas