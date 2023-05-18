from loja_airforce import app, db
from loja_airforce.models import Usuario, Endereco, Produto, Imagem

with app.app_context():
    db.create_all()