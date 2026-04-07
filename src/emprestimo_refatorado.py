from abc import ABC, abstractmethod
import sqlite3
from datetime import datetime, timedelta
from email.mime.text import MIMEText
import smtplib
from reportlab.pdfgen import canvas


class IRepositorio(ABC):
    @abstractmethod
    def buscar(self, identificador):
        pass

    @abstractmethod
    def salvar(self, entidade):
        pass


class ConexaoSQLite:
    def __init__(self, db_path='biblioteca.db'):
        self.db_path = db_path

    def conectar(self):
        return sqlite3.connect(self.db_path)


class RepositorioLivro(IRepositorio):
    def __init__(self, conexao):
        self.conexao = conexao

    def buscar(self, isbn):
        conn = self.conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livros WHERE isbn = ?", (isbn,))
        livro = cursor.fetchone()
        conn.close()
        return livro

    def salvar(self, entidade):
        raise NotImplementedError("Método não aplicável para este repositório.")

    def atualizar_exemplares(self, isbn, delta):
        conn = self.conexao.conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE livros
            SET exemplares_disponiveis = exemplares_disponiveis + ?
            WHERE isbn = ?
            """,
            (delta, isbn)
        )
        conn.commit()
        conn.close()


class RepositorioLeitor(IRepositorio):
    def __init__(self, conexao):
        self.conexao = conexao

    def buscar(self, cpf):
        conn = self.conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM leitores WHERE cpf = ?", (cpf,))
        leitor = cursor.fetchone()
        conn.close()
        return leitor

    def salvar(self, entidade):
        raise NotImplementedError("Método não aplicável para este repositório.")


class RepositorioEmprestimo(IRepositorio):
    def __init__(self, conexao):
        self.conexao = conexao

    def buscar(self, emprestimo_id):
        conn = self.conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emprestimos WHERE id = ?", (emprestimo_id,))
        emprestimo = cursor.fetchone()
        conn.close()
        return emprestimo

    def salvar(self, entidade):
        conn = self.conexao.conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO emprestimos (livro_isbn, leitor_cpf, data_emprestimo, data_devolucao_prevista)
            VALUES (?, ?, ?, ?)
            """,
            (
                entidade["livro_isbn"],
                entidade["leitor_cpf"],
                entidade["data_emprestimo"],
                entidade["data_devolucao_prevista"]
            )
        )
        conn.commit()
        emprestimo_id = cursor.lastrowid
        conn.close()
        return emprestimo_id


class RepositorioReserva(IRepositorio):
    def __init__(self, conexao):
        self.conexao = conexao

    def buscar(self, reserva_id):
        conn = self.conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,))
        reserva = cursor.fetchone()
        conn.close()
        return reserva

    def salvar(self, entidade):
        conn = self.conexao.conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO reservas (livro_isbn, leitor_cpf, data_reserva)
            VALUES (?, ?, ?)
            """,
            (
                entidade["livro_isbn"],
                entidade["leitor_cpf"],
                entidade["data_reserva"]
            )
        )
        conn.commit()
        reserva_id = cursor.lastrowid
        conn.close()
        return reserva_id


class RepositorioMulta(IRepositorio):
    def __init__(self, conexao):
        self.conexao = conexao

    def buscar(self, multa_id):
        conn = self.conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM multas WHERE id = ?", (multa_id,))
        multa = cursor.fetchone()
        conn.close()
        return multa

    def salvar(self, entidade):
        conn = self.conexao.conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO multas (emprestimo_id, valor)
            VALUES (?, ?)
            """,
            (
                entidade["emprestimo_id"],
                entidade["valor"]
            )
        )
        conn.commit()
        multa_id = cursor.lastrowid
        conn.close()
        return multa_id


class ServicoNotificacao:
    def enviar_email(self, destinatario, assunto, mensagem):
        try:
            msg = MIMEText(mensagem)
            msg["Subject"] = assunto
            msg["To"] = destinatario

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("biblioteca@exemplo.com", "senha")
            server.send_message(msg)
            server.quit()
        except Exception:
            pass


class ServicoRelatorio:
    def gerar_comprovante(self, emprestimo_id, titulo_livro, nome_leitor, data_devolucao):
        try:
            c = canvas.Canvas(f"comprovante_{emprestimo_id}.pdf")
            c.drawString(100, 750, f"Empréstimo #{emprestimo_id}")
            c.drawString(100, 730, f"Livro: {titulo_livro}")
            c.drawString(100, 710, f"Leitor: {nome_leitor}")
            c.drawString(100, 690, f"Devolução: {data_devolucao}")
            c.save()
        except Exception:
            pass


class CalculadoraMulta:
    def calcular(self, data_devolucao_prevista):
        prevista = datetime.strptime(data_devolucao_prevista, "%Y-%m-%d")
        hoje = datetime.now()

        if hoje > prevista:
            dias_atraso = (hoje - prevista).days
            return dias_atraso * 2.0
        return 0.0


class GerenciadorEmprestimo:
    def __init__(
        self,
        repo_livro,
        repo_leitor,
        repo_emprestimo,
        repo_reserva,
        repo_multa,
        servico_notificacao,
        servico_relatorio,
        calculadora_multa
    ):
        self.repo_livro = repo_livro
        self.repo_leitor = repo_leitor
        self.repo_emprestimo = repo_emprestimo
        self.repo_reserva = repo_reserva
        self.repo_multa = repo_multa
        self.servico_notificacao = servico_notificacao
        self.servico_relatorio = servico_relatorio
        self.calculadora_multa = calculadora_multa

    def realizar_emprestimo(self, livro_isbn, leitor_cpf):
        livro = self.repo_livro.buscar(livro_isbn)
        if not livro:
            return False, "Livro não encontrado"

        leitor = self.repo_leitor.buscar(leitor_cpf)
        if not leitor:
            return False, "Leitor não encontrado"

        exemplares_disponiveis = livro[4]

        if exemplares_disponiveis > 0:
            data_emprestimo = datetime.now().strftime("%Y-%m-%d")
            data_devolucao_prevista = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

            emprestimo_id = self.repo_emprestimo.salvar({
                "livro_isbn": livro_isbn,
                "leitor_cpf": leitor_cpf,
                "data_emprestimo": data_emprestimo,
                "data_devolucao_prevista": data_devolucao_prevista
            })

            self.repo_livro.atualizar_exemplares(livro_isbn, -1)

            self.servico_notificacao.enviar_email(
                leitor[2],
                "Empréstimo Realizado",
                f"Empréstimo realizado: {livro[1]}"
            )

            self.servico_relatorio.gerar_comprovante(
                emprestimo_id,
                livro[1],
                leitor[1],
                data_devolucao_prevista
            )

            return True, "Empréstimo realizado com sucesso"

        self.repo_reserva.salvar({
            "livro_isbn": livro_isbn,
            "leitor_cpf": leitor_cpf,
            "data_reserva": datetime.now().strftime("%Y-%m-%d")
        })

        return False, "Livro indisponível. Reserva criada."

    def calcular_multa(self, emprestimo_id):
        emprestimo = self.repo_emprestimo.buscar(emprestimo_id)
        if not emprestimo:
            return 0.0

        valor_multa = self.calculadora_multa.calcular(emprestimo[4])

        if valor_multa > 0:
            self.repo_multa.salvar({
                "emprestimo_id": emprestimo_id,
                "valor": valor_multa
            })

            leitor = self.repo_leitor.buscar(emprestimo[2])
            if leitor:
                self.servico_notificacao.enviar_email(
                    leitor[2],
                    "Multa por Atraso",
                    f"Multa de R$ {valor_multa:.2f} aplicada"
                )

        return valor_multa