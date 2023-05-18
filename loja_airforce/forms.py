## definir os formulários do nosso site

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, FloatField, IntegerField, SelectField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, InputRequired
from loja_airforce.models import Usuario, Produto, Endereco, Imagem

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()]) # nos validators passa uma lista de validações
    senha = PasswordField("Senha", validators=[DataRequired()])
    btn_submit = SubmitField("Fazer Login")


class FormLoginAdm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()]) # nos validators passa uma lista de validações
    senha = PasswordField("Senha", validators=[DataRequired()])
    btn_submit = SubmitField("Fazer Login")


class FormCriarConta(FlaskForm):
    nome_completo = StringField("Nome Completo", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    btn_submit = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first() 
        # validação do email
        if usuario:
            return ValidationError("E-mail já cadastrado, faça login para continuar")

class FormAddProduto(FlaskForm):
    nome_produto = StringField("Nome do Produto", validators=[DataRequired()])
    valor = FloatField("Valor", validators=[DataRequired()])
    qtd_estoque = IntegerField("Quantidade em Estoque", validators=[DataRequired()])
    foto = FileField("Foto", validators=[DataRequired()])
    btn_submit = SubmitField("Enviar")

class FormDeleteProduto(FlaskForm):
    id_produto = IntegerField("Id do Produto", validators=[DataRequired()])
    btn_submit = SubmitField("Remover")

class FormEndereco(FlaskForm):
    endereco1 = StringField("Endereço", validators=[DataRequired()])
    endereco2 = StringField("Cidade", validators=[DataRequired()])
    estado = SelectField('Estado', choices=[('AC', 'Acre'),
                                            ('AL', 'Alagoas'),
                                            ('AP', 'Amapá'),
                                            ('AM', 'Amazonas'),
                                            ('BA', 'Bahia'),
                                            ('CE', 'Ceará'),
                                            ('DF', 'Distrito Federal'),
                                            ('ES', 'Espírito Santo'),
                                            ('GO', 'Goiás'),
                                            ('MA', 'Maranhão'),
                                            ('MT', 'Mato Grosso'),
                                            ('MS', 'Mato Grosso do Sul'),
                                            ('MG', 'Minas Gerais'),
                                            ('PA', 'Pará'),
                                            ('PB', 'Paraíba'),
                                            ('PR', 'Paraná'),
                                            ('PE', 'Pernambuco'),
                                            ('PI', 'Piauí'),
                                            ('RJ', 'Rio de Janeiro'),
                                            ('RN', 'Rio Grande do Norte'),
                                            ('RS', 'Rio Grande do Sul'),
                                            ('RO', 'Rondônia'),
                                            ('RR', 'Roraima'),
                                            ('SC', 'Santa Catarina'),
                                            ('SP', 'São Paulo'),
                                            ('SE', 'Sergipe'),
                                            ('TO', 'Tocantins')],
                        validators=[InputRequired()])
    pais = SelectField('País', choices=[('','Escolha...'),('Brasil', 'Brasil')])
    cep = StringField("CEP", validators=[DataRequired()])
    btn_submit = SubmitField("Salvar Endereço")

class FormBusca(FlaskForm):
    busca = StringField("Pesquisar")
    btn_submit = SubmitField("Buscar")

class FormCarrinho(FlaskForm):
    submit = SubmitField("Adicionar ao carrinho")

