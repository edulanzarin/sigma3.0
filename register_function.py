from connect_database import conectar_banco


def cadastrar_usuario(usuario, senha):
    try:
        conn = conectar_banco()

        cursor = conn.cursor()
        query = "INSERT INTO cadastros (usuario, senha) VALUES (%s, %s)"
        cursor.execute(query, (usuario, senha))

        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print("Erro ao cadastrar usuário:", str(e))
        return False
