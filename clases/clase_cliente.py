class Cliente:
    id=0
    nombre=""
    email=""
    direccion   =""

    def __init__(self, c_id, c_nombre, c_email, c_direccion):
        self.id=c_id
        self.nombre=c_nombre
        self.email=c_email
        self.direccion=c_direccion

    def obtenerObjetoSerializable(self):
        dicctemp=dict()
        dicctemp["id"]=self.id
        dicctemp["nombre"]=self.nombre
        dicctemp["email"]=self.email
        dicctemp["direccion"]=self.direccion
        return dicctemp