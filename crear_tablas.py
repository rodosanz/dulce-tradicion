from database import conectar

def crear_tablas():
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS productos(
                            producto_id SERIAL PRIMARY KEY,
                            nombre VARCHAR(100) NOT NULL,
                            precio_compra NUMERIC(10,2) NOT NULL CHECK(precio_compra > 0),
                            precio_venta NUMERIC(10,2) NOT NULL CHECK(precio_venta > 0),
                            stock INT NOT NULL DEFAULT 0 CHECK(stock >= 0)
                        );

                        CREATE TABLE IF NOT EXISTS clientes(
                            cliente_id SERIAL PRIMARY KEY,
                            telefono VARCHAR(20) UNIQUE,
                            nombre VARCHAR(100) NOT NULL,
                            direccion TEXT,
                            observaciones TEXT,
                            precio_mensajeria NUMERIC(10,2) DEFAULT 0
                        );

                        CREATE TABLE IF NOT EXISTS mensajeros(
                            mensajero_id SERIAL PRIMARY KEY,
                            nombre VARCHAR(100) NOT NULL,
                            telefono VARCHAR(20) UNIQUE
                        );

                        CREATE TABLE IF NOT EXISTS mensajerias(
                            mensajeria_id SERIAL PRIMARY KEY,
                            cliente_id INT NOT NULL REFERENCES clientes(cliente_id),
                            estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente' CHECK(
                                estado IN (
                                    'Pendiente',
                                    'Enviado',
                                    'Entregado',
                                    'Cancelado'
                                )
                            ),
                            costo_mensajeria NUMERIC(10,2) NOT NULL DEFAULT 0,
                            total NUMERIC(10,2) NOT NULL CHECK(total > 0),
                            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            mensajero_id INT REFERENCES mensajeros(mensajero_id)
                        );

                        CREATE TABLE IF NOT EXISTS detalle_mensajerias(
                            detalle_mensajeria_id SERIAL PRIMARY KEY,
                            mensajeria_id INT REFERENCES mensajerias(mensajeria_id),
                            producto_id INT REFERENCES productos(producto_id),
                            cantidad INT NOT NULL CHECK(cantidad > 0),
                            precio_unitario NUMERIC(10,2) NOT NULL CHECK(precio_unitario > 0),
                            costo NUMERIC(10,2) NOT NULL CHECK(costo > 0)
                        );

                        CREATE TABLE IF NOT EXISTS ventas(
                            venta_id SERIAL PRIMARY KEY,
                            cliente_id INT REFERENCES clientes(cliente_id),
                            estado VARCHAR(30) NOT NULL DEFAULT 'Entregado' CHECK(
                                estado IN (
                                    'Reservado',
                                    'Entregado',
                                    'Cancelado'
                                )
                            ),
                            total NUMERIC(10,2) NOT NULL CHECK(total > 0),
                            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );

                        CREATE TABLE IF NOT EXISTS detalle_ventas(
                            detalle_venta_id SERIAL PRIMARY KEY,
                            venta_id INT REFERENCES ventas(venta_id),
                            producto_id INT REFERENCES productos(producto_id),
                            cantidad INT NOT NULL CHECK(cantidad > 0),
                            precio_unitario NUMERIC(10,2) NOT NULL CHECK(precio_unitario > 0),
                            costo NUMERIC(10,2) NOT NULL CHECK(costo > 0)
                        );

                        CREATE TABLE IF NOT EXISTS proveedores(
                            proveedor_id SERIAL PRIMARY KEY,
                            nombre VARCHAR(100) NOT NULL UNIQUE,
                            telefono VARCHAR(20) UNIQUE
                        );

                        CREATE TABLE IF NOT EXISTS compras(
                            compra_id SERIAL PRIMARY KEY,
                            proveedor_id INT REFERENCES proveedores(proveedor_id),
                            total NUMERIC(10,2) NOT NULL CHECK(total > 0),
                            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            observaciones TEXT
                        );

                        CREATE TABLE IF NOT EXISTS detalle_compras(
                            detalle_compra_id SERIAL PRIMARY KEY,
                            compra_id INT REFERENCES compras(compra_id),
                            producto_id INT REFERENCES productos(producto_id),
                            cantidad INT NOT NULL CHECK(cantidad > 0),
                            precio_compra NUMERIC(10,2) NOT NULL CHECK(precio_compra > 0)
                        );

                        CREATE TABLE IF NOT EXISTS movimientos_inventario(
                            inventario_id SERIAL PRIMARY KEY,
                            producto_id INT REFERENCES productos(producto_id),
                            tipo VARCHAR(20) NOT NULL CHECK(
                                tipo IN(
                                    'Venta',
                                    'Mensajeria',
                                    'Compra',
                                    'Ajuste'
                                )
                            ),
                            referencia_id INT,
                            cantidad INT NOT NULL CHECK( cantidad <> 0),
                            observaciones TEXT,
                            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error creando tablas: {e}")
    finally:
        cursor.close()
        conn.close()