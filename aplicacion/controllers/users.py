from dataclasses import dataclass
from flask import render_template, request, redirect
from aplicacion import app
from aplicacion.models.user import Usuario

#Redirigir la ruta inicial a users para que no haya falla al probar desde ese link
@app.route("/")
def inicio():
    return redirect('/users')

@app.route("/users/new")
def index():
    # llamar al método de clase get all para obtener todos los amigos
    usuarios = Usuario.get_all()
    print(usuarios)
    return render_template("crear.html", usuarios=usuarios)

@app.route('/crear_usuario', methods=["POST"])
def crear_usuario():
    # Primero hacemos un diccionario de datos a partir de nuestro request.form proveniente de nuestra plantilla
    # Las claves en los datos tienen que alinearse exactamente con las variables en nuestra cadena de consulta
    data = {
        "nombre": request.form["nombre"],
        "apellido" : request.form["apellido"],
        "correo" : request.form["correo"]
    }
    Usuario.save(data)
    #esto es para encontrar el ultimo id y usarlo en el redirect
    nuevo_usuario= Usuario.select_last()
    id=nuevo_usuario[0]['id']
    print(nuevo_usuario)
    #POST va con REDIRECT
    return redirect(f"/users/{id}")

@app.route('/users')
def mostrar_usuarios():
    usuarios = Usuario.get_all()
    return render_template("todos.html", usuarios=usuarios)

@app.route('/users/<int:id>')
def show_user_by_id(id):
    # print("hola, esta funcionando la funcion")
    data={
        "identificador":id
    }
    todo_de_un_usuario=Usuario.un_usuario(data)
    #print(todo_de_un_usuario) 
    #todo de un usuario es una lista con un diccionario dentro, por esto se define un usuario que sólo sea un diccionario, asi es mas facil llamarlo en el HTML
    usuario=todo_de_un_usuario[0]
    print (usuario)
    return render_template("un-usuario.html", usuario=usuario)

@app.route("/users/<int:id>/edit")
def pagina_editar(id):
    data={
        "identificador":id
    }
    todo_de_un_usuario=Usuario.un_usuario(data)
    usuario=todo_de_un_usuario[0]
    return render_template("editar-un-usuario.html", usuario=usuario)

@app.route("/users/<int:id>/actualizando", methods=["POST"])
def editar_usuario(id):
    data = {
        "id":id,
        "nombre": request.form["enombre"],
        "apellido" : request.form["eapellido"],
        "correo" : request.form["ecorreo"]
    }
    Usuario.editar_un_usuario(data)
    #POST va con REDIRECT
    return redirect(f'/users/{id}')

@app.route("/users/<int:id>/delete")
def delete_user(id):
    data={
        "identificador":id
    }
    Usuario.delete(data)
    return redirect('/users')