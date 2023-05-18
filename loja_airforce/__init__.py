# inicializa o APP
from flask import Flask
from flask_paginate import Pagination
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import locale

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///airforceshop.db'# cria uma pasta com nosso banco de dados
app.config["SECRET_KEY"] = "sua secret_key"
app.config["UPLOAD_FOLDER"] = "static/img"
app.config['PER_PAGE'] = 12  # Defina o número de produtos por página

# carrinho de compras
add_carrinho = list()
car = dict()


db = SQLAlchemy(app) # armazena informações do nosso banco de dados
bcrypt = Bcrypt(app) # cryptografia 
login_manager = LoginManager(app) # gestão do login
login_manager.login_view = "homepage" # onde será rediricionado para fazer login

# definição do locale padrão como Brasil
def format_currency(value):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return locale.currency(value, grouping=True, symbol='R$')

# adicionando format_currency como variável global
app.jinja_env.globals.update(format_currency=format_currency)


# importações dos outros arquivos
from loja_airforce import views
