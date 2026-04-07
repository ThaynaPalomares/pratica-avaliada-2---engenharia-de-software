# Modelagem UML - BiblioTech

## Diagrama de Classes

```mermaid
classDiagram
    class Livro {
        +String isbn
        +String titulo
        +String autor
        +String categoria
        +int exemplaresDisponiveis
        +buscarDisponibilidade()
        +atualizarQuantidade()
    }

    class Exemplar {
        +int numero
        +String status
        +marcarEmprestado()
        +marcarDisponivel()
    }

    class Leitor {
        +String cpf
        +String nome
        +String email
        +String telefone
        +verificarPendencias()
        +consultarHistorico()
    }

    class Emprestimo {
        +int id
        +String dataEmprestimo
        +String dataDevolucaoPrevista
        +String dataDevolucao
        +registrar()
        +renovar()
    }

    class Reserva {
        +int id
        +String dataReserva
        +String status
        +registrar()
        +notificarLeitor()
    }

    class Bibliotecario {
        +int id
        +String nome
        +registrarEmprestimo()
        +registrarDevolucao()
    }

    class Multa {
        +int id
        +float valor
        +boolean paga
        +calcularValor()
        +registrarPagamento()
    }

    Livro "1" --> "*" Exemplar : possui
    Leitor "1" --> "*" Emprestimo : realiza
    Livro "1" --> "*" Emprestimo : gera
    Leitor "1" --> "*" Reserva : faz
    Livro "1" --> "*" Reserva : recebe
    Emprestimo "1" --> "0..1" Multa : gera
    Bibliotecario "1" --> "*" Emprestimo : registra