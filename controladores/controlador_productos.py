from bd import obtener_conexion
import os
from flask import current_app
from flask import request
from werkzeug.utils import secure_filename


def obtener_productos():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion, precio, stock, imagen FROM productos")
        productos = cursor.fetchall()
    conexion.close()
    return productos

def obtener_producto_por_id(id):
    conexion = obtener_conexion()
    producto = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, descripcion, precio, stock, imagen FROM productos WHERE id = %s", (id,))
        producto = cursor.fetchone()
    conexion.close()
    return producto

def obtener_nombre_imagen(id):
    conexion = obtener_conexion()
    producto = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT imagen FROM productos WHERE id = %s", (id,))
        producto = cursor.fetchone()
    conexion.close()
    return producto

def obtener_producto_por_nombre(nom):
    conexion = obtener_conexion()

    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, descripcion, precio, stock, imagen FROM productos WHERE nombre LIKE %s",
                ('%' + nom + '%',))
            producto = cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener el producto por nombre: {e}")
        producto = None
    finally:
        conexion.close()

    return producto


def insertar_producto(nombre, descripcion, precio, stock, imagen):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO productos(nombre, descripcion, precio, stock, imagen) VALUES (%s, %s, %s, %s, %s)",
                       (nombre, descripcion, precio, stock, imagen))
    conexion.commit()
    conexion.close()

def actualizar_producto(nombre, descripcion, precio, stock, imagen, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s, imagen = %s WHERE id = %s",
                       (nombre, descripcion, precio, stock, imagen, id))

        # Verificar si se subió un archivo
        if 'imagen' in request.files and request.files['imagen'].filename != '':
            imagen = request.files['imagen']
            # Obtener la ruta completa de destino
            destino = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(imagen.filename))
            # Guardar el archivo
            imagen.save(destino)

    conexion.commit()
    conexion.close()

def eliminar_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()