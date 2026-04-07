# Análise de Design - GerenciadorEmprestimo

## Princípios SOLID violados no código original

### SRP - Single Responsibility Principle
A classe `GerenciadorEmprestimo` viola o princípio da responsabilidade única, pois concentra várias funções diferentes:
- conexão com banco de dados
- busca de livros e leitores
- registro de empréstimos
- atualização de estoque
- criação de reservas
- cálculo de multa
- envio de emails
- geração de comprovante em PDF

Isso faz com que a classe tenha várias razões para mudar.

### OCP - Open/Closed Principle
A classe não está aberta para extensão e fechada para modificação. Se for necessário mudar a forma de envio de notificações, alterar o formato do relatório ou trocar o banco de dados, o código da classe principal precisa ser alterado diretamente.

### DIP - Dependency Inversion Principle
A classe depende diretamente de implementações concretas, como `sqlite3`, `smtplib` e `reportlab`, em vez de depender de abstrações. Isso dificulta manutenção, testes e evolução do sistema.

## Problemas de coesão
A coesão é baixa porque a mesma classe mistura persistência, regra de negócio, comunicação externa e geração de arquivos.

## Problemas de acoplamento
O acoplamento é alto porque a classe está diretamente ligada:
- ao banco SQLite
- ao servidor SMTP
- à biblioteca de geração de PDF
- à estrutura das tabelas do banco por meio de índices como `livro[4]` e `leitor[2]`

## Outros problemas identificados
- uso de `except: pass`, ocultando erros
- credenciais fixas no código
- lógica de negócio misturada com infraestrutura
- dificuldade para reutilização e testes

## Sugestões de refatoração
Para melhorar o design, a refatoração deve:
- separar os repositórios por entidade
- criar um serviço específico para notificações
- criar um serviço específico para relatórios
- criar uma classe separada para cálculo de multas
- usar injeção de dependências na classe principal
- manter o gerenciador principal apenas como orquestrador do processo

## Validação da refatoração

Após a refatoração, foi possível executar o sistema e realizar um empréstimo com sucesso, demonstrando que:
- as responsabilidades foram corretamente separadas
- o sistema continua funcional após a reorganização
- a estrutura está mais modular e preparada para evolução