#rotas

from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from fakepinterest.models import Usuario, Foto
import  os
from werkzeug.utils import secure_filename


@app.route('/', methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            # Atualize a chamada para url_for para usar o parâmetro 'username'
            return redirect(url_for("perfil", username=usuario.username))
    return render_template('homepage.html', form=form_login)




@app.route('/registro',  methods=["GET", "POST"])
def registro():
    form_criar_conta = FormCriarConta()
    if form_criar_conta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        usuario = Usuario(username=form_criar_conta.username.data, senha=senha,
                          email=form_criar_conta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)

        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("register.html", form=form_criar_conta)

@app.route("/perfil/<username>", methods=["GET", "POST"])
@login_required
def perfil(username):
    usuario = Usuario.query.filter_by(username=username).first()
    if usuario:
        if usuario == current_user:
            # O usuário está vendo seu próprio perfil
            form_foto = FormFoto()
            if form_foto.validate_on_submit():
                arquivo = form_foto.foto.data
                nome_seguro = secure_filename(arquivo.filename)
                caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                    app.config["UPLOAD_FOLDER"], nome_seguro)
                arquivo.save(caminho)
                foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
                database.session.add(foto)
                database.session.commit()

            return render_template("perfil.html", usuario=current_user, form=form_foto)
        else:
            # O usuário está vendo o perfil de outro usuário
            return render_template("perfil.html", usuario=usuario, form=None)
    else:
        # Se o usuário não existir, redirecione ou exiba uma mensagem de erro
        return render_template("perfil_nao_encontrado.html", username=username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/feed')
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()


    return render_template("feed.html", fotos=fotos)