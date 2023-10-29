from PyQt5.QtCore import QThread, pyqtSignal
from connect_database import conectar_banco


class CadastrarConciliacoesThread(QThread):
    cadastro_ready = pyqtSignal()

    def __init__(self, codigo_empresa, descricao, debito, credito):
        super().__init__()
        self.codigo_empresa = codigo_empresa
        self.descricao = descricao
        self.debito = debito
        self.credito = credito

    def run(self):
        table_name = f"conciliacao_{self.codigo_empresa}"

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        table_exists = cursor.fetchone()

        if not table_exists:
            cursor.execute(
                f"CREATE TABLE {table_name} ("
                "id_conciliacao INT PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE, "
                "descricao varchar(100), "
                "conta_debito int, "
                "conta_credito int"
                ")"
            )

        if table_exists:
            cursor.execute(
                f"INSERT INTO {table_name} (descricao, conta_debito, conta_credito) VALUES (%s, %s, %s)",
                (self.descricao, self.debito, self.credito),
            )
            conn.commit()
            conn.close()

            self.cadastro_ready.emit()
