import pymysql

def obtener_conexion():
<<<<<<< HEAD
    # return pymysql.connect(host='Grupo04DAW.mysql.pythonanywhere-services.com',
    #                             user='Grupo04DAW',
    #                             password='DAW_2023_2_TIENDA',
    #                             db='Grupo04DAW$tienda')
        return pymysql.connect(host='localhost',
                                user='root',
                                password='',
=======
    return pymysql.connect(host='viaduct.proxy.rlwy.net',
                                port=34430,
                                user='root',
                                password='aH2gEHhFde5GGHDA-6HdfD42bd-2bb43',
>>>>>>> b43304944e0d89fe169f82d3359b23864213db0d
                                db='tienda')