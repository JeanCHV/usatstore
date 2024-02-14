import pymysql

def obtener_conexion():
    return pymysql.connect(host='viaduct.proxy.rlwy.net',
                                user='root',
                                password='aH2gEHhFde5GGHDA-6HdfD42bd-2bb43',
                                db='tienda')