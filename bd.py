import pymysql

def obtener_conexion():
    # return pymysql.connect(host='Grupo04DAW.mysql.pythonanywhere-services.com',
    #                             user='Grupo04DAW',
    #                             password='DAW_2023_2_TIENDA',
    #                             db='Grupo04DAW$tienda')
        return pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='tienda')