# Requisitos do Sistema BiblioTech

## Requisitos Funcionais

| ID | Descrição | Prioridade |
|----|-----------|------------|
| RF01 | O sistema deve permitir cadastrar livros com título, autor, ISBN, categoria e quantidade de exemplares. | Alta |
| RF02 | O sistema deve permitir consultar livros por ISBN, título ou autor. | Alta |
| RF03 | O sistema deve permitir atualizar os dados de um livro cadastrado. | Média |
| RF04 | O sistema deve permitir cadastrar leitores com nome, CPF, email e telefone. | Alta |
| RF05 | O sistema deve permitir consultar os dados de um leitor cadastrado. | Média |
| RF06 | O sistema deve permitir registrar empréstimos de livros para leitores. | Alta |
| RF07 | O sistema deve calcular automaticamente a data prevista de devolução em 14 dias a partir da data do empréstimo. | Alta |
| RF08 | O sistema deve permitir registrar reservas quando não houver exemplares disponíveis. | Alta |
| RF09 | O sistema deve permitir registrar a devolução de livros emprestados. | Alta |
| RF10 | O sistema deve notificar por email o primeiro leitor da fila de reserva quando um livro for devolvido. | Alta |
| RF11 | O sistema deve permitir renovar empréstimos quando não houver reserva para o livro. | Média |
| RF12 | O sistema deve calcular multa por atraso no valor de R$ 2,00 por dia. | Alta |

## Requisitos Não-Funcionais

| ID | Categoria | Descrição | Métrica |
|----|-----------|-----------|---------|
| RNF01 | Desempenho | O sistema deve retornar consultas de livros e leitores rapidamente. | até 2 segundos por consulta |
| RNF02 | Segurança | O sistema deve proteger os dados pessoais dos leitores. | acesso restrito a usuários autorizados |
| RNF03 | Usabilidade | O sistema deve ser simples de operar para bibliotecários. | operações principais em até 3 cliques |
| RNF04 | Confiabilidade | O sistema deve manter integridade dos dados de empréstimos, reservas e multas. | 0 inconsistências entre empréstimos e estoque |
| RNF05 | Manutenibilidade | O código deve seguir princípios SOLID e separação de responsabilidades. | classes com responsabilidade única |

## Regras de Negócio

| ID | Descrição |
|----|-----------|
| RN01 | O prazo padrão de empréstimo é de 14 dias. |
| RN02 | Um livro só pode ser emprestado se houver exemplar disponível. |
| RN03 | Quando não houver exemplar disponível, o sistema deve permitir reserva. |
| RN04 | A renovação do empréstimo só pode ocorrer se não houver reserva para o livro. |
| RN05 | A multa por atraso deve ser de R$ 2,00 por dia. |
| RN06 | Quando um livro for devolvido, o primeiro leitor da fila de reservas deve ser notificado por email. |

## User Stories

### US01
Como bibliotecário  
Quero cadastrar livros no acervo  
Para manter a coleção da biblioteca atualizada

Critérios de Aceitação:
- [ ] Deve ser possível informar título, autor, ISBN, categoria e quantidade de exemplares
- [ ] O sistema deve impedir cadastro de ISBN duplicado

Story Points: 3

### US02
Como leitor  
Quero me cadastrar no sistema  
Para poder pegar livros emprestados

Critérios de Aceitação:
- [ ] Deve ser possível informar nome, CPF, email e telefone
- [ ] O sistema deve impedir cadastro com CPF já existente

Story Points: 2

### US03
Como bibliotecário  
Quero registrar empréstimos  
Para controlar a saída de livros do acervo

Critérios de Aceitação:
- [ ] O empréstimo deve registrar data de empréstimo e data prevista de devolução
- [ ] O sistema deve reduzir a quantidade de exemplares disponíveis

Story Points: 5

### US04
Como leitor  
Quero reservar um livro indisponível  
Para ser avisado quando ele estiver disponível

Critérios de Aceitação:
- [ ] A reserva só deve ser criada quando não houver exemplares disponíveis
- [ ] O sistema deve registrar a posição do leitor na fila

Story Points: 3

### US05
Como bibliotecário  
Quero registrar devoluções  
Para liberar exemplares para novos empréstimos ou reservas

Critérios de Aceitação:
- [ ] O sistema deve registrar a data de devolução
- [ ] O sistema deve verificar se existe multa por atraso

Story Points: 5

### US06
Como bibliotecário  
Quero renovar empréstimos  
Para atender leitores que precisem de mais tempo com o livro

Critérios de Aceitação:
- [ ] A renovação só deve ocorrer se não houver reservas para o livro
- [ ] O sistema deve recalcular a nova data prevista de devolução

Story Points: 3