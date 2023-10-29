from PyQt5.QtCore import QThread, pyqtSignal
from connect_database import conectar_banco
from error_window import MyErrorMessage


class ConciliarThread(QThread):
    conciliacao_done = pyqtSignal()

    def __init__(self, codigo_empresa):
        super().__init__()
        self.codigo_empresa = codigo_empresa

    def run(self):
        try:
            codigo_empresa = self.codigo_empresa
            tabela_conciliacao = f"conciliacao_{codigo_empresa}"
            conn = conectar_banco()
            cursor = conn.cursor()

            update_query = f"""
            UPDATE transacoes AS t
            SET t.debito = (
                CASE
                    WHEN EXISTS (
                        SELECT 1
                        FROM {tabela_conciliacao} AS c
                        WHERE t.descricao LIKE CONCAT('%', LOWER(c.descricao), '%')
                    ) THEN
                        (SELECT COALESCE(debito, conta_debito)
                        FROM {tabela_conciliacao} AS c
                        WHERE t.descricao LIKE CONCAT('%', LOWER(c.descricao), '%')
                        LIMIT 1)
                    ELSE
                        t.debito  -- Mantém o valor original de debito
                END
            ),
            t.credito = (
                CASE
                    WHEN EXISTS (
                        SELECT 1
                        FROM {tabela_conciliacao} AS c
                        WHERE t.descricao LIKE CONCAT('%', LOWER(c.descricao), '%')
                    ) THEN
                        (SELECT COALESCE(credito, conta_credito)
                        FROM {tabela_conciliacao} AS c
                        WHERE t.descricao LIKE CONCAT('%', LOWER(c.descricao), '%')
                        LIMIT 1)
                    ELSE
                        t.credito  -- Mantém o valor original de credito
                END
            );
            """

            cursor.execute(update_query)
            conn.commit()
            conn.close()
            self.conciliacao_done.emit()

        except Exception as e:
            error_message = MyErrorMessage()
            error_message.showMessage("Erro ao conciliar " + str(e))
            error_message.exec_()

    def obter_dados_atualizados(self):
        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            select_query = f"""
            "SELECT id_transacao, data_transacao, debito, credito, valor, descricao FROM transacoes"
            """
            cursor.execute(select_query)
            dados_atualizados = cursor.fetchall()
            conn.close()

            return dados_atualizados
        except Exception as e:
            error_message = MyErrorMessage()
            error_message.showMessage("Erro ao conciliar " + str(e))
            error_message.exec_()
