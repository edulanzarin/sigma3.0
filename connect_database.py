import mysql.connector


def conectar_banco():
    conn = mysql.connector.connect(
        host="containers-us-west-68.railway.app",
        user="root",
        password="fklU6HxSmfCS7HDUYh9p",
        database="railway",
        port=6060,
    )

    return conn
