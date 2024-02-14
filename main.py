from flask import Flask, render_template, request, redirect, flash, jsonify, make_response
from werkzeug.utils import secure_filename
from flask import session
from flask import g

import os
import controladores.controlador_productos as controlador_productos
import controladores.controlador_usuarios as controlador_usuarios
import controladores.controlador_clientes as controlador_clientes
import clases.clase_producto as clase_producto
import clases.clase_usuario as clase_usuario
import clases.clase_cliente as clase_cliente
import clases.clase_auth as clase_auth
import hashlib
import random


# from flask_jwt import JWT, jwt_required
app = Flask(__name__)
##### SEGURIDAD - INICIO #######################################################

def authenticate(username, password):
    usuario = controlador_usuarios.obtener_usuario(username)
    user = clase_auth.Usuario(usuario[0], usuario[1], usuario[2])

    h = hashlib.new('sha256')
    h.update(bytes(password, encoding="utf-8"))
    encpass = h.hexdigest()
    if user and (user.password == encpass):
        return user

def identity(payload):
    user_id = payload['identity']
    usuario = controlador_usuarios.obtener_usuario_por_id(user_id)
    user = clase_auth.Usuario(usuario[0], usuario[1], usuario[2])
    return user

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

# jwt = JWT(app, authenticate, identity)

##### SEGURIDAD - FIN ##########################################################
# Validacion



def validar_token():

    token = request.cookies.get('token')
    username = request.cookies.get('username')
    usuario = controlador_usuarios.obtener_usuario(username)

    if usuario is not None and len(usuario) > 4 and token == usuario[4]:
        return True
    return False

def validar_TipoUsuario():
    username = request.cookies.get('username')
    tipo_usuario = 'administrador'
    usuario = controlador_usuarios.obtener_Tipo_usuario(username)
    if tipo_usuario == usuario[5]:
        return True
    return False


# ### APIS
# # PRODUCTOS
# @app.route("/api_obtener_productos")
# @jwt_required()
# def api_obtener_productos():
#     response = dict()
#     datos = []
#     productos = controlador_productos.obtener_productos()
#     for producto in productos:
#         miobjproducto = clase_producto.Producto(producto[0], producto[1], producto[2], producto[3], producto[4], producto[5])
#         datos.append(miobjproducto.obtenerObjetoSerializable())

#     # Preparando responde objeto JSON
#     response["data"] = datos
#     response["code"] = 1
#     response["message"] = "Listado de Productos correcto"
#     return jsonify(response)

# # Establece un límite máximo para el stock
# MAX_STOCK = 100

# @app.route("/api_guardar_productos", methods=["POST"])
# @jwt_required()
# def api_guardar_producto():
#     nombre = request.json["nombre"]
#     descripcion = request.json["descripcion"]
#     precio = request.json["precio"]
#     stock = int(request.json["stock"])
#     imagen = request.json["imagen"]

#     # Verifica si el stock supera el límite
#     if stock > MAX_STOCK:
#         return jsonify({"codigo": "2", "mensaje": "El stock supera el límite máximo permitido."})

#     # Asegúrate de haber importado e inicializado controlador_productos
#     controlador_productos.insertar_producto(nombre, descripcion, precio, stock, imagen)

#     return jsonify({"codigo": "1", "mensaje": "Producto guardado correctamente."})



# @app.route("/api_actualizar_producto", methods=["POST"])
# @jwt_required()
# def api_actualizar_producto():
#     nombre = request.json["nombre"]
#     descripcion = request.json["descripcion"]
#     precio = request.json["precio"]
#     stock = request.json["stock"]
#     imagen = request.json["imagen"]
#     id = request.json["id"]
#     controlador_productos.actualizar_producto(nombre, descripcion, precio, stock, imagen, id)
#     return jsonify({"codigo": "1", "mensaje": "Producto actualizado correctamente."})

# @app.route("/api_eliminar_producto", methods=["POST"])
# @jwt_required()
# def api_eliminar_producto():
#     controlador_productos.eliminar_producto(request.json["id"])
#     return jsonify({"codigo": "1", "mensaje": "Producto Eliminado correctamente"})

# # USUARIOS
# @app.route("/api_obtener_usuarios")
# @jwt_required()
# def api_obtener_usuarios():
#     response = dict()
#     datos = []
#     usuario = controlador_usuarios.obtener_usuarios()
#     for usuario in usuario:
#         miobjusuario = clase_usuario.Usuario(usuario[0], usuario[1], usuario[2], usuario[3],usuario[4])
#         datos.append(miobjusuario.obtenerObjetoSerializable())

#     # Preparando responde objeto JSON
#     response["data"] = datos
#     response["code"] = 1
#     response["message"] = "Listado de Usuarios correcto"
#     return jsonify(response)

# @app.route("/api_guardar_usuario", methods=["POST"])
# @jwt_required()
# def api_guardar_usuario():
#     username = request.json["username"]
#     password = request.json["password"]
#     email = request.json["email"]
#     tipo_usuario = request.json["tipo_usuario"]

#     h = hashlib.new('sha256')
#     h.update(bytes(password, encoding="utf-8"))
#     encpass = h.hexdigest()

#     controlador_usuarios.registrar_usuario(username, encpass, email, tipo_usuario)
#     return jsonify({"codigo": "1", "mensaje": "Usuario guardado correctamente."})

# @app.route("/api_actualizar_usuario", methods=["POST"])
# @jwt_required()
# def api_actualizar_usuario():
#     username = request.json["username"]
#     new_username = request.json["new_username"]
#     new_password = request.json["new_password"]
#     new_email = request.json["new_email"]
#     tipo_usuario = request.json["tipo_usuario"]

#     controlador_usuarios.actualizar_usuario(new_username, new_password, new_email, tipo_usuario,username)
#     return jsonify({"codigo": "1", "mensaje": "Usuario actualizado correctamente."})

# @app.route("/api_eliminar_usuario", methods=["POST"])
# @jwt_required()
# def api_eliminar_usuario():
#     id=request.json["id"]
#     controlador_usuarios.eliminar_usuario(id)
#     return jsonify({"codigo": "1", "mensaje": "Usuario eliminado correctamente."})


# # CLIENTES

# @app.route("/api_obtener_cliente")
# @jwt_required()
# def api_obtener_cliente():
#     response = dict()
#     datos = []
#     cliente = controlador_clientes.obtener_todos_los_clientes()
#     for cliente in cliente:
#         miobjcliente = clase_cliente.Cliente(cliente[0], cliente[1], cliente[2], cliente[3])
#         datos.append(miobjcliente.obtenerObjetoSerializable())
#     # Preparando responde objeto JSON
#     response["data"] = datos
#     response["code"] = 1
#     response["message"] = "Listado de Clientes correcto"
#     return jsonify(response)

# @app.route("/api_guardar_cliente", methods=["POST"])
# @jwt_required()
# def api_guardar_cliente():
#     nombre = request.json["nombre"]
#     email = request.json["email"]
#     direccion = request.json["direccion"]
#     controlador_clientes.crear_cliente(nombre, email, direccion)
#     return jsonify({"codigo": "1", "mensaje": "Cliente guardado correctamente."})


# @app.route("/api_actualizar_cliente", methods=["POST"])
# @jwt_required()
# def api_actualizar_cliente():
#     cliente_id=request.json["id"]
#     nombre = request.json["nombre"]
#     email = request.json["email"]
#     direccion = request.json["direccion"]
#     controlador_clientes.actualizar_cliente(cliente_id, nombre, email, direccion)
#     return jsonify({"codigo": "1", "mensaje": "Cliente actualizado correctamente."})

# @app.route("/api_eliminar_cliente", methods=["POST"])
# @jwt_required()
# def api_eliminar_cliente():
#     controlador_clientes.eliminar_cliente(request.json["id"])
#     return jsonify({"codigo": "1", "mensaje": "Cliente Eliminado correctamente"})

##Templates y Funciones
#Cliente
@app.route("/gestionar_cliente")
def formulario_crud_cliente():
    if validar_token():
        clientes = controlador_clientes.obtener_todos_los_clientes()
        return render_template("clientes/crud_clientes.html", clientes=clientes, esSesionIniciada=True, esAdministrador=False)
    return redirect("/login")

@app.route("/agregar_cliente")
def formulario_agregar_cliente():
    if validar_token():
        return render_template("clientes/agregar_cliente.html", esSesionIniciada=True, esAdministrador=False)
    return redirect("/login")

@app.route("/actualizar_cliente", methods=["POST"])
def actualizar_cliente():
    id = request.form["id"]
    nombre = request.form["nombre"]
    email = request.form["email"]
    direccion = request.form["direccion"]
    controlador_clientes.actualizar_cliente(nombre, email, direccion, id)
    return redirect("/gestionar_cliente")

@app.route("/guardar_cliente", methods=["POST"])
def guardar_cliente():
    nombre = request.form["nombre"]
    email = request.form["email"]
    direccion = request.form["direccion"]

    controlador_clientes.crear_cliente(nombre, email, direccion)
    return redirect("/gestionar_cliente")

@app.route('/formulario_editar_cliente/<int:id>')
def editar_cliente(id):
    clientes = controlador_clientes.obtener_cliente_por_id(id)
    return render_template("clientes/editar_cliente.html", clientes=clientes, esSesionIniciada=True, esAdministrador=False)

@app.route("/eliminar_cliente", methods=["POST"])
def eliminar_cliente():
    controlador_clientes.eliminar_cliente(request.form["id"])
    return redirect("/gestionar_cliente")


# RECUPERAR CONTRASEÑA
@app.route("/recuperar_contraseña")
def recuperar_contraseña():
    return render_template("user/recuperar_contraseña.html")


# ACERCA DE NOSOTROS
@app.route("/acerca_de_nosotros")
def acerca_de_nosotros():
    if validar_token():
        productos = controlador_productos.obtener_productos()

        if validar_TipoUsuario():
            return render_template("productos/acerca_de_nosotros.html", productos=productos, esSesionIniciada=True,
                                   esAdministrador=False)
        else:
            return render_template("productos/acerca_de_nosotros.html", productos=productos, esSesionIniciada=True,
                                   esAdministrador=True)
    return redirect("/login")


# CONTACTANOS
@app.route("/contactanos")
def contactanos():
    if validar_token():
        productos = controlador_productos.obtener_productos()

        if validar_TipoUsuario():
            return render_template("productos/contactanos.html", productos=productos, esSesionIniciada=True,
                                   esAdministrador=False)
        else:
            return render_template("productos/contactanos.html", productos=productos, esSesionIniciada=True,
                                   esAdministrador=True)
    return redirect("/login")


@app.route("/productos")
def productos():
    if validar_token():
        productos = controlador_productos.obtener_productos()

        if validar_TipoUsuario():
            return render_template("productos/productos.index.html", productos=productos, esSesionIniciada=True,
                                   esAdministrador=False)
        else:
            return render_template("productos/productos.index.html", productos=productos, esSesionIniciada=True,
                                   esAdministrador=True)
    return redirect("/login")

# CRUD DE PRODUCTOS
@app.route("/gestionar_producto")
def formulario_crud_producto():
    if validar_token():
        productos = controlador_productos.obtener_productos()
        return render_template("productos/crud_producto.html", productos=productos, esSesionIniciada=True,
                               esAdministrador=False)
    return redirect("/login")

# FORMULARIO AGREGAR PRODUCTO HTML
@app.route("/agregar_producto")
def formulario_agregar_producto():
    if validar_token():
        return render_template("productos/agregar_producto.html", esSesionIniciada=True, esAdministrador=False)
    return redirect("/login")

#FUNCION GUARDAR PRODUCTO
@app.route("/guardar_producto", methods=["POST"])
def guardar_producto():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    stock = request.form["stock"]

    try:
        if 'imagen' in request.files:
            imagen = request.files['imagen']
            # Verificar que el archivo no esté vacío
            if imagen and len(imagen.read()) > 0:
                imagen.seek(0)  # Reiniciar la posición del cursor después de leer el archivo
                filename = secure_filename(imagen.filename)
                imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                controlador_productos.insertar_producto(nombre, descripcion, precio, stock, filename)
            else:
                flash("Error: El archivo de imagen está vacío.")
        else:
            controlador_productos.insertar_producto(nombre, descripcion, precio, stock, None)

        flash("Producto guardado correctamente.")
    except Exception as e:
        print(f"Error al guardar el producto: {e}")
        flash("Error al guardar el producto. Inténtalo de nuevo.")

    return redirect("/productos")


# FORMULARIO EDITAR PRODUCTO
@app.route("/editar_producto/<int:id>")
def editar_producto(id):
    productos = controlador_productos.obtener_producto_por_id(id)
    return render_template("productos/editar_producto.html", productos=productos, esSesionIniciada=True,
                           esAdministrador=False)

# FUNCION ACTUALIZAR PRODUCTO
@app.route("/actualizar_producto", methods=["POST"])
def actualizar_producto():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    stock = request.form["stock"]

    try:
        if 'imagen' in request.files and request.files['imagen'].filename != '':
            imagen = request.files['imagen']
            # Verificar que el archivo no esté vacío
            if len(imagen.read()) == 0:
                flash("Error: El archivo de imagen está vacío.")
                return redirect("/gestionar_producto")
            imagen.seek(0)  # Reiniciar la posición del cursor después de leer el archivo
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            # Si no se subió una nueva imagen, obtén el nombre actual de la imagen
            nombre_imagen_actual = controlador_productos.obtener_nombre_imagen(id)
            filename = nombre_imagen_actual

        controlador_productos.actualizar_producto(nombre, descripcion, precio, stock, filename, id)
        flash("Producto actualizado correctamente.")
    except Exception as e:
        print(f"Error al actualizar el producto: {e}")
        flash("Error al actualizar el producto. Inténtalo de nuevo.")

    return redirect("/gestionar_producto")



#FUNCION ELIMINAR PRODUCTO
@app.route("/eliminar_producto", methods=["POST"])
def eliminar_producto():
    controlador_productos.eliminar_producto(request.form["id"])
    return redirect("/productos")

#FUNCION CARGAR PRODUCTO
@app.route("/cargar_producto", methods=["POST"])
def cargar_producto():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    stock = request.form["stock"]

    # Verificar si se subió un archivo
    if 'imagen' in request.files and request.files['imagen'].filename != '':
        imagen = request.files['imagen']
        # Guardar el archivo y obtener el nombre del archivo
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = None

    controlador_productos.actualizar_producto(nombre, descripcion, precio, stock, filename, id)
    return redirect("/gestionar_producto")

#FORMULARIO DETALLE PRODUCTO
@app.route("/productos/<int:id>")
def detalle_producto(id):
    productos = controlador_productos.obtener_producto_por_id(id)
    return render_template("productos/producto_detalle.html", productos=productos, esSesionIniciada=True,
                           esAdministrador=False)

#USUARIOS

# CRUD DE USUARIOS
@app.route("/gestionar_usuario")
def formulario_crud_usuario():
    if validar_token():
        usuarios = controlador_usuarios.obtener_usuarios()
        return render_template("user/crud_usuarios.html", usuarios=usuarios, esSesionIniciada=True,
                               esAdministrador=False)
    return redirect("/login")

# FORMULARIO AGREGAR USUARIO
@app.route("/agregar_usuario")
def formulario_agregar_usuario():
    if validar_token():
        return render_template("user/agregar_usuario.html", esSesionIniciada=True, esAdministrador=False)
    return redirect("/login")

# FUNCION GUARDAR USUARIO
@app.route("/guardar_usuario", methods=["POST"])
def guardar_usuario():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    tipo_usuario = request.form["tipo_usuario"]

    existing_user = controlador_usuarios.obtener_usuario(username)
    if existing_user:
        flash("El nombre de usuario ya está en uso. Por favor, elige otro.")
        return redirect("/registrar_usuario")

    h = hashlib.new('sha256')
    h.update(bytes(password, encoding="utf-8"))
    encpass = h.hexdigest()

    controlador_usuarios.registrar_usuario(username, encpass, email, tipo_usuario)
    return redirect("/gestionar_usuario")

#FORMULARIO EDITAR USUARIO
@app.route("/editar_usuario/<int:id>")
def editar_usuario(id):
    usuarios = controlador_usuarios.obtener_usuario_por_id(id)
    return render_template("user/edit_user.html", usuarios=usuarios, esSesionIniciada=True, esAdministrador=False)

# FUNCION ACTUALIZAR USUARIO
@app.route("/actualizar_usuario", methods=["POST"])
def actualizar_usuario():
    new_username = request.form["new_username"]
    new_password = request.form["new_password"]
    new_email = request.form["new_email"]
    tipo_usuario = request.form["tipo_usuario"]
    username = request.form["username"]

    controlador_usuarios.actualizar_usuario(new_username, new_password, new_email, tipo_usuario, username)
    return redirect("/gestionar_usuario")

@app.route("/modificar_datos", methods=["GET", "POST"])
def modificar_datos():
    if validar_token():
        nombre_usuario = controlador_usuarios.obtener_nombre_usuario(token=request.cookies.get('token'))
        if request.method == "POST":
            new_password = request.form.get("new_password")
            new_email = request.form.get("new_email")
            tipo_usuario = request.form.get("tipo_usuario")
            username = controlador_usuarios.obtener_nombre_usuario(token=request.cookies.get('token'))

            controlador_usuarios.actualizar_usuario(new_username=username, new_password=new_password, new_email=new_email, tipo_usuario=tipo_usuario, username=username)
            return redirect("/index")

        return render_template("/user/edit_current_user.html", nombre_usuario=nombre_usuario, esSesionIniciada=True)

    return redirect("/login")

# ELIMINAR USUARIO
@app.route("/eliminar_usuario", methods=["POST"])
def eliminar_usuario():
    controlador_usuarios.eliminar_usuario(request.form["id"])
    return redirect("/gestionar_usuario")


@app.route("/")
@app.route("/index")
def index():
    if validar_token():
        # Obtén el nombre del usuario, puedes obtenerlo de la sesión o donde sea que lo almacenes
        nombre_usuario = controlador_usuarios.obtener_nombre_usuario(token = request.cookies.get('token'))
        productos = controlador_productos.obtener_productos()

        if validar_TipoUsuario():
            return render_template("home.html", productos=productos, esSesionIniciada=True, esAdministrador=False, nombre_usuario=nombre_usuario)
        else:
            return render_template("home.html", productos=productos, esSesionIniciada=True, esAdministrador=True, nombre_usuario=nombre_usuario)
    return redirect("/login")



##CARRITO
@app.route("/carrito")
def carrito():
    if validar_token():
        return render_template("carrito.html", esSesionIniciada=True, esAdministrador=False)
    return redirect("/login")

@app.route("/agregar_al_carrito/<int:producto_id>", methods=["GET"])
def agregar_al_carrito(producto_id):
    # Lógica para agregar el producto al carrito (puedes almacenar esta información en una sesión)
    # Por ejemplo, puedes tener una lista en la sesión que almacene los IDs de los productos en el carrito
    if 'carrito' not in session:
        session['carrito'] = []
    session['carrito'].append(producto_id)
    flash('Producto agregado al carrito', 'success')
    return redirect("/productos")


# LOGIN Y REGISTRO
@app.route("/login")
def login():
    token = request.cookies.get('token')
    if token != 'xyz':
        return render_template("/user/login.html")
    return redirect("/index")

# REGISTRAR USUARIO CLIENTE

@app.route("/registrar_usuario", methods=["GET", "POST"])
def registrar_usuario():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        tipo_usuario=request.form["tipo_usuario"]

        existing_user = controlador_usuarios.obtener_usuario(username)
        if existing_user:
            flash("El nombre de usuario ya está en uso. Por favor, elige otro.")
            return redirect("/registrar_usuario")

        h = hashlib.new('sha256')
        h.update(bytes(password, encoding="utf-8"))
        encpass = h.hexdigest()

        controlador_usuarios.registrar_usuario(username, encpass, email,tipo_usuario)

        return redirect("/login")

    return render_template("/user/register.html")




@app.route("/procesar_login", methods=["POST"])
def procesar_login():
    username = request.form["username"]
    password = request.form["password"]

    usuario = controlador_usuarios.obtener_usuario(username)

    h = hashlib.new('sha256')
    h.update(bytes(password, encoding="utf-8"))
    encpass = h.hexdigest()

    if encpass == usuario[2]:
        numale = random.randint(1, 1024)
        a = hashlib.new('sha256')
        a.update(bytes(str(numale), encoding="utf-8"))
        encnumale = a.hexdigest()

        resp = make_response(redirect("/index"))
        resp.set_cookie('token', encnumale)
        resp.set_cookie('username', username)
        controlador_usuarios.actualizartoken_usuario(username, encnumale)
        return resp

    return redirect("/login")

def procesar_logout():
    resp = make_response(redirect("/index"))
    resp.set_cookie('token', '', 0)
    return resp

app.add_url_rule('/logout', 'procesar_logout', procesar_logout)
app.config['UPLOAD_FOLDER'] = 'mysite/static/img/productos'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
