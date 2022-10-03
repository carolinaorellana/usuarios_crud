# importar la función que devolverá una instancia de una conexión
from aplicacion.config.mysqlconnection import connectToMySQL
# modelar la clase después de la tabla friend de nuestra base de datos
class Usuario:
    def __init__( self , data ):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.correo = data['correo']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # ahora usamos métodos de clase para consultar nuestra base de datos
    #LEER TODOS LOS USUARIOS
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('usuarios_schema').query_db(query)
        # crear una lista vacía para agregar nuestras instancias de friends
        usuarios = []
        # Iterar sobre los resultados de la base de datos y crear instancias de friends con cls
        for usuario in results:
            usuarios.append( cls(usuario) )
        return usuarios

    #CREAR UN NUEVO USUARIO
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO usuarios ( nombre , apellido , correo , created_at, updated_at ) VALUES ( %(nombre)s , %(apellido)s , %(correo)s , NOW() , NOW() );"
        #esta sintaxis de %()s es para evitar inyecciones y maltrato de datos. muy importante
        
        # data es un diccionario que se pasará al método de guardar desde server.py
        return connectToMySQL('usuarios_schema').query_db( query, data )
    
    #MOSTRAR UN USUARIO
    @classmethod
    def un_usuario(cls,data):
        query = "SELECT * FROM usuarios WHERE id=%(identificador)s;"
        results = connectToMySQL('usuarios_schema').query_db(query,data)
        return results
    
    #UPDATE UN USUARIO
    @classmethod
    def editar_un_usuario(cls,data):
        query="UPDATE usuarios SET nombre = %(nombre)s, apellido = %(apellido)s, correo =%(correo)s, updated_at = NOW()  WHERE id=%(id)s"
        return connectToMySQL('usuarios_schema').query_db( query, data )

    #DELETE UN USUARIO
    @classmethod 
    def delete(cls,data):
        query = "DELETE FROM usuarios WHERE id=%(identificador)s;"
        results = connectToMySQL('usuarios_schema').query_db(query,data)
        return results

    #esta classmethod es para que seleccione el ultimo id creado, lo usaré para que cuando se agregue un nuevo usuario, se redirija con el ultimo id creado en la cuenta, es decir su propio id, esto es porque los id no estan siendo LEIDOS ni nada por el estilo en la pagina de crear nuevo usuario.
    #este no necesita ninguna informacion como parametro.
    @classmethod
    def select_last(cls):
        query= "SELECT * FROM usuarios ORDER BY id DESC Limit 1;"
        results = connectToMySQL('usuarios_schema').query_db(query)
        return results


