from loja_airforce import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)
    endereco = db.Relationship("Endereco", backref="usuario", lazy=True)

class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    endereco1 = db.Column(db.String, nullable=False)
    endereco2 = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, nullable=False)
    pais = db.Column(db.String, nullable=False)
    cep = db.Column(db.String, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    qtd_estoque = db.Column(db.Integer, nullable=False)
    imagens = db.Relationship("Imagem", backref="produto", lazy=True, uselist=True)

class Imagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String, nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)