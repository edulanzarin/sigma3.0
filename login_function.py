from datetime import datetime
import socket

from connect_database import conectar_banco


def get_ip_address():
    hostname = socket.gethostname()
    ip_computador = socket.gethostbyname(hostname)
    return ip_computador


def get_hora_atual():
    hora_atual = datetime.now()
    return hora_atual


def get_hostname():
    nome_computador = socket.gethostname()
    return nome_computador


def verificar_credenciais(usuario, senha):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        query = "SELECT id_cadastro FROM cadastros WHERE usuario = %s AND senha = %s"
        cursor.execute(query, (usuario, senha))
        id_usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return id_usuario
    except Exception as e:
        print("Erro ao verificar credenciais:", str(e))
        return None


def registrar_login(id_usuario):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        hora_atual = get_hora_atual()
        ip_computador = get_ip_address()
        nome_computador = get_hostname()

        query = "INSERT INTO log_login (id_usuario, data_atual, hora_atual, ip_computador, nome_computador) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(
            query,
            (
                id_usuario,
                hora_atual.date(),
                hora_atual.time(),
                ip_computador,
                nome_computador,
            ),
        )

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Erro ao registrar o login:", str(e))
