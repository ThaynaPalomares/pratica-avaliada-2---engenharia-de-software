from src.emprestimo_refatorado import (
    ConexaoSQLite,
    RepositorioLivro,
    RepositorioLeitor,
    RepositorioEmprestimo,
    RepositorioReserva,
    RepositorioMulta,
    ServicoNotificacao,
    ServicoRelatorio,
    CalculadoraMulta,
    GerenciadorEmprestimo
)

conexao = ConexaoSQLite("biblioteca.db")

repo_livro = RepositorioLivro(conexao)
repo_leitor = RepositorioLeitor(conexao)
repo_emprestimo = RepositorioEmprestimo(conexao)
repo_reserva = RepositorioReserva(conexao)
repo_multa = RepositorioMulta(conexao)

servico_notificacao = ServicoNotificacao()
servico_relatorio = ServicoRelatorio()
calculadora_multa = CalculadoraMulta()

gerenciador = GerenciadorEmprestimo(
    repo_livro,
    repo_leitor,
    repo_emprestimo,
    repo_reserva,
    repo_multa,
    servico_notificacao,
    servico_relatorio,
    calculadora_multa
)

print("=== TESTE DE BUSCA ===")
print("Livro:", repo_livro.buscar("978-0134685991"))
print("Leitor:", repo_leitor.buscar("12345678901"))

print("\n=== TESTE DE EMPRÉSTIMO ===")
resultado = gerenciador.realizar_emprestimo("978-0134685991", "12345678901")
print("Resultado:", resultado)

print("\n=== TESTE DE MULTA ===")
print("Multa do empréstimo 1:", gerenciador.calcular_multa(1))