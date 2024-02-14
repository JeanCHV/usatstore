class Usuario:
    id=0
    username=""
    password=""
    email=""
    tipo_usuario   =""

    def __init__(self, u_id, u_username,u_password, u_email, u_tipo_usuario):
        self.id=u_id
        self.username=u_username
        self.password =u_password
        self.email=u_email
        self.tipo_usuario=u_tipo_usuario

    def obtenerObjetoSerializable(self):
        dicctemp=dict()
        dicctemp["id"]=self.id
        dicctemp["username"]=self.username
        dicctemp["password"]=self.password
        dicctemp["email"]=self.email
        dicctemp["tipo_usuario"]=self.tipo_usuario
        return dicctemp

    def __str__(self):
        return "User(id='%s')" % self.id