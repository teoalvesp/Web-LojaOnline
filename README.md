## Loja Online de Tênis Nike Air Force

Este é um projeto de uma loja online de tênis Nike Air Force, desenvolvida em Flask, com a utilização de Bootstrap para estilização. O projeto inclui funcionalidades como login de usuário com autenticação e senha criptografada, criação de conta, armazenamento de produtos, imagens de produtos, usuários e endereços dos usuários em um banco de dados, carrinho de compras no backend, área de administração para adicionar ou remover produtos e paginação para produtos.

#### OBSERVAÇÃO: Todo o processo do frontend foi feito em processo de aprendizagem do mesmo, existe funcionalidades feitas no backend que poderia trazer melhor acessibilidade se feita com JavaScript no front, em breve chegará novas versões com melhorias.

## Tecnologias utilizadas

-Flask
-Python
-Bootstrap
-SQLite
-HTML
-CSS
-JavaScript

## Para executar o projeto, você precisará das seguintes ferramentas instaladas em sua máquina:

1 - Clone o repositório em sua máquina local
2 - Instale as dependências necessárias:

pip install -r requirements.txt

3 - Configure o banco de dados no arquivo config.py
4 - Execute o comando a seguir para criar as tabelas no banco de dados:

flask db upgrade

- O projeto possue um arquivo chamado "criar_banco.py",
caso queira recriar o seu banco de dados, execute o mesmo.

5 - Inicie o servidor:

execute o arquivo "main.py"

6 - Acesse http://localhost:5000 em seu navegador para visualizar o site


## Funcionalidades

-Login de usuário com autenticação e senha criptografada
-Criação de conta de usuário
-Armazenamento de produtos, imagens de produtos, usuários e endereços dos usuários em um banco de dados
-Carrinho de compras no backend
-Área de administração para adicionar ou remover produtos
-Paginação para produtos

## Contribuição
Se você quiser contribuir para o projeto, siga os seguintes passos:

-Faça um fork deste repositório
-Crie uma nova branch com sua alteração: git checkout -b feature/nome-da-alteracao
-Faça o commit das alterações: git commit -m "Adicione uma nova funcionalidade"
-Faça o push para a branch criada: git push origin feature/nome-da-alteracao
-Abra um pull request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.
