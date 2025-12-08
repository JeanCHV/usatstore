import pymysql

def sqlConn():
    try:
        return pymysql.connect(host='localhost',
                               user='root',
                               password='',
                               db='tienda')
    except pymysql.Error as e:
        print("Error al conectar con la base de datos:", e)
        return None