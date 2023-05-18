# definir as rotas de nosso site
from flask import render_template, url_for, redirect, request, session, flash
from flask_paginate import get_page_args, Pagination
from loja_airforce import app, db, bcrypt, add_carrinho, format_currency
from flask_login import login_required, login_user, logout_user, current_user
from loja_airforce.forms import FormLogin, FormCriarConta, FormLoginAdm, FormAddProduto, FormDeleteProduto, FormEndereco, FormBusca, FormCarrinho
from loja_airforce.models import Usuario, Produto, Endereco, Imagem
from werkzeug.utils import secure_filename
import os
from PIL import Image
import json
from flask import jsonify
from collections import Counter


@app.route("/", methods=["GET", "POST"])
def homepage():
    form = FormBusca()

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    produtos = Produto.query.offset(offset).limit(per_page).all()
    total = Produto.query.count()

    pagination = Pagination(page=page, total=total, per_page=per_page, label={'previous': 'Anterior', 'next': 'Próximo', 'page': 'Página', 'total': 'Total', 'of': 'de'},)


    # aloritimo de busca de produtos
    if form.validate_on_submit():
        pesquisa = f'%{form.busca.data}%'
        produtos = Produto.query.filter(Produto.nome_produto.like(pesquisa)).offset(offset).limit(per_page).all()
        total = Produto.query.filter(Produto.nome_produto.like(pesquisa)).count()

        pagination = Pagination(page=page, total=total, per_page=per_page, label={'previous': 'Anterior', 'next': 'Próximo', 'page': 'Página', 'total': 'Total', 'of': 'de'})
        

        return render_template('homepage.html', produtos=produtos, pagination=pagination, form=form, views="homepage", busca=True)
  

    pagination = Pagination(page=page, total=total, per_page=per_page, label={'previous': 'Anterior', 'next': 'Próximo', 'page': 'Página', 'total': 'Total', 'of': 'de'})

    return render_template('homepage.html', produtos=produtos, pagination=pagination, form = form, views="homepage", add_carrinho=add_carrinho, busca=False)


@app.route("/login/<user>", methods=["GET", "POST"])
def login(user):
    if user == "administrador":
        form = FormLoginAdm()
    else:
        form = FormLogin()

    if form.validate_on_submit():
        try:
            usuario = Usuario.query.filter_by(email=form.email.data).first()
        except:
            usuario = Usuario.query.filter_by(fullname=form.username.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario)

            if user == "usuario-pedido":
                user = "usuario"
                return redirect(url_for("pedido"))

            if current_user.fullname == "admin":
                return redirect(url_for("admin"))

            return redirect(url_for("homepage"))

    return render_template("login.html", form=form, usuario=user, type=1, hide_nav_buttons=True, views="login")

@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form = FormCriarConta()

    if form.validate_on_submit():
        senha = bcrypt.generate_password_hash(form.senha.data)
        usuario = Usuario(fullname=form.nome_completo.data, email=form.email.data, senha=senha)
        
        db.session.add(usuario)
        db.session.commit()
        # fazer o login do usuario
        login_user(usuario, remember=True)
        return redirect(url_for("endereco"))

    return render_template("criarconta.html", form=form, hide_nav_buttons=True, views="criarconta")

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    # area do adminstrador
    form_add = FormAddProduto()
    form_del = FormDeleteProduto()
    produtos = Produto.query.all()
    indice = len(produtos)

    # ADICIONAR UM NOVO PRODUTO  
    if form_add.validate_on_submit():
        arquivo = form_add.foto.data
        secure_name = secure_filename(arquivo.filename)
        nomeProduto = form_add.nome_produto.data.replace(" ", "-")[:10]
        novo_nome = f"img-{indice}-{nomeProduto}" + os.path.splitext(secure_name)[1]

        # salvar o arquivo dentro da pasta img
        project_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(project_path, app.config["UPLOAD_FOLDER"], novo_nome)

        try:
            with Image.open(arquivo) as img:
                img = img.resize((500, 500))
                img.save(path, quality=72)

        except Exception as e:
            print(f"Erro ao processar a imagem: {e}")
            flash("Erro ao processar a imagem. Tente novamente.", "danger")
            return redirect(url_for("admin"))


        # criar a foto no banco com o item "imagem" sendo o nome do arquivo
        produto = Produto(nome_produto=form_add.nome_produto.data,
                        valor=form_add.valor.data,
                        qtd_estoque=form_add.qtd_estoque.data)

        db.session.add(produto)
        db.session.commit()

        imagem = Imagem(imagem=f'static/img/{novo_nome}', id_produto=indice+1)
        db.session.add(imagem)
        db.session.commit()

        return redirect(url_for("admin"))


    # REMOVER UM PRODUTO
    if form_del.validate_on_submit():
        id_produto = form_del.id_produto.data
        
        try:
            produto = Produto.query.get(int(id_produto))
            
            if produto.imagens:
                for imagem in produto.imagens:
                    db.session.delete(imagem)
                    db.session.commit()

            # apaga o produto no banco de dados
            db.session.delete(produto)
            db.session.commit()

            # apaga a imagem do produto da pasta img
            project_path = os.path.abspath(os.path.dirname(__file__))
            if produto.imagens:
                path = os.path.join(project_path, produto.imagens[0].imagem)
                os.remove(path)
        except:
            print("Houve algum erro, verifique!")
       

        return redirect(url_for("admin"))

    return render_template("admin.html", form_add=form_add, form_del=form_del, produtos=produtos, hide_nav_buttons=True, views="adm")


@app.route("/produto/<id>", methods=["GET", "POST"])
def produto(id):
    form = FormBusca()
    form_carrinho = FormCarrinho()

    produto = Produto.query.get(int(id))

    if form_carrinho.submit.data:
    # Adiciona produto ao carrinho
        add_carrinho.append(produto.id)

        return render_template("produto.html", produto=produto, views="produto", form=form, form_carrinho=form_carrinho, add_carrinho=add_carrinho)

    # algoritmo de busca de produtos
    if form.validate_on_submit():
        pesquisa = f'%{form.busca.data}%'

        page = request.args.get('page', 1, type=int)
        per_page = 10
        offset = (page - 1) * per_page

        produtos = Produto.query.filter(Produto.nome_produto.like(pesquisa)).offset(offset).limit(per_page).all()
        total = Produto.query.filter(Produto.nome_produto.like(pesquisa)).count()

        pagination = Pagination(page=page, total=total, per_page=per_page, label={'previous': 'Anterior', 'next': 'Próximo', 'page': 'Página', 'total': 'Total', 'of': 'de'})

        return redirect(url_for('homepage', produtos=produtos, pagination=pagination, form=form, views="homepage"))

    return render_template("produto.html", produto=produto, views="produto", form=form, form_carrinho=form_carrinho, add_carrinho=add_carrinho)


    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    add_carrinho.clear()
    return redirect(url_for("homepage"))


@app.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    total = 0

    # verificar se há itens repetidos na lista do carrinho
    count = Counter(add_carrinho)
    car = dict(count)

    produtos = Produto.query.filter(Produto.id.in_(add_carrinho)).all()
    for produto in produtos:
        total += produto.valor * car[produto.id]


    return render_template('carrinho.html', produtos=produtos, total=total, add_carrinho=add_carrinho, car=car)


@app.route('/adicionar-endereco', methods=['GET', 'POST'])
@login_required
def endereco():
    form = FormEndereco()
    if form.validate_on_submit():
        # registrar no banco de dados
        endereco = Endereco(endereco1 = form.endereco1.data,
        endereco2 = form.endereco2.data, 
        estado = form.estado.data,
        pais = form.pais.data,
        cep = form.cep.data,
        id_usuario = current_user.id)
        db.session.add(endereco)
        db.session.commit()
        return redirect(url_for("homepage"))
    return render_template('endereco.html', form=form, views="endereco")

@app.route("/tabela")
def tabela():
    produtos = Produto.query.all()
    return render_template("tabela.html", produtos=produtos)

@app.route("/pedido")
def pedido():
    add_carrinho.clear()
    return render_template("pedido.html")

@app.route("/limpar_carrinho")
def limpar_carrinho():
    add_carrinho.clear()
    return redirect(url_for('carrinho'))

@app.route("/remover_produto/<id>")
def remover_produto(id):
    id_produto = int(id)
    global add_carrinho
    add_carrinho = [elemento for elemento in add_carrinho if elemento != id_produto]

   
    return redirect(url_for('carrinho'))

