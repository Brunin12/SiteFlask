import json
import urllib.request
from random import randint

from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cursos.sqlite3'
app.config['SECRET_KEY'] = 'd758cb22b069fcab6dd6a877b7939c59169a63f2'
app.static_folder = 'static'

db = SQLAlchemy(app)

frutas = ['maçã']
registros = []


class Cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    ch = db.Column(db.Integer)

    def __init__(self, nome, descricao, ch):
        self.nome = nome
        self.descricao = descricao
        self.ch = ch


@app.route('/', methods=["GET", "POST"])
def home():
    nome = "Tuim"
    idade = 12
    aleatorio = randint(0, 3)
    if request.method == "POST":
        if request.form.get("frutas_input"):
            frutas.append(request.form.get("frutas_input"))
    return render_template("index.html", idade=idade, nome=nome, frutas=frutas, aleatorio=aleatorio)


@app.route('/sobre')
def sobre():
    return render_template("sobre.html")


@app.route('/jogar/<jogo>')
def jogar(jogo):
    if jogo == "space_invaders":
        return render_template("jogo.html")
    else:
        return home()


@app.route('/alunos', methods=["GET", "POST"])
def alunos():
    if request.method == "POST":
        if request.form.get("aluno_input") and request.form.get("nota_input"):
            nome_aluno = request.form.get("aluno_input")
            nota_aluno = float(request.form.get("nota_input"))

            # Verifica se o aluno já existe no dicionário "registros" e atualiza o valor da nota
            for registro in registros:
                if registro['nome'] == nome_aluno:
                    registro['nota'] = nota_aluno
                    break
            else:
                registros.append({"nome": nome_aluno, "nota": nota_aluno})

    return render_template("classit/alunos.html", registros=registros)


@app.route('/filmes/<categoria>')
def filmes(categoria):
    url = ""
    if categoria == 'categorias':
        return render_template("supermovies/filmes.html")
    elif categoria == 'populares':
        url = \
            "https://api.themoviedb.org/3/movie/popular?api_key=af3279e78076bc5268a9739421acebff&language=pt-BR&page=1"
    elif categoria == 'drama':
        url = \
            ("https://api.themoviedb.org/3/discover/movie?api_key=af3279e78076bc5268a9739421acebff&with_genres=18"
             "&language=pt-BR&page=1")
    elif categoria == 'kids':
        url = \
            ("https://api.themoviedb.org/3/discover/movie?region=BR&certification=G&include_adult=false&api_key"
             "=af3279e78076bc5268a9739421acebff&language=pt-BR&page=1")

    elif categoria == 'tom_cruise':
        url = \
            ("https://api.themoviedb.org/3/discover/movie?api_key=af3279e78076bc5268a9739421acebff&with_people=500"
             "&language=pt-BR&page=1&language=pt-BR&page=1")

    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    json_data = json.loads(dados)
    return render_template("supermovies/dados_filme.html", filmes=json_data['results'])


@app.route('/cursos')
def cursos_lista():
    page = request.args.get('page', 1, type=int)
    per_page = 4
    todos_cursos = Cursos.query.paginate(page=page, per_page=per_page)
    return render_template('cursos/cursos_lista.html', cursos=todos_cursos)


@app.route('/criar_curso', methods=["GET", "POST"])
def criar_curso():
    adicionado = False
    if request.method == "POST":
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        ch = request.form.get('ch')
        if not nome or not descricao or not ch or not ch.isdigit():
            flash("Preencha todos os campos do Formulário", "error")
        else:

            curso = Cursos(nome, descricao, ch)
            db.session.add(curso)
            db.session.commit()
            adicionado = True
    return render_template('cursos/criar_curso.html', adicionado=adicionado)


@app.route('/buscar_cursos', methods=["GET"])
def buscar_cursos():
    if request.method == "GET":
        q = request.args.get("q")
        if q:
            cursos_encontrados = Cursos.query.filter(
                Cursos.nome.like(f'%{q}%')).all()
            return render_template('cursos/cursos_lista.html', cursos=cursos_encontrados)

    return render_template('cursos/cursos_lista.html', cursos=Cursos.query.all())


@app.route('/<int:id>/editar_curso', methods=["GET", "POST"])
def editar_curso(id_curso):
    curso = Cursos.query.filter_by(id=id_curso).first()
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        ch = request.form["ch"]
        if not nome or not descricao or not ch or not ch.isdigit():
            flash("Preencha todos os campos do Formulário", "error")
        else:
            Cursos.query.filter_by(id=id_curso).update({"nome": nome, "descricao": descricao, "ch": ch})
            db.session.commit()
            return redirect(url_for("cursos_lista"))
    return render_template('cursos/editar_curso.html', curso=curso)


@app.route('/<int:id>/excluir_curso')
def excluir_curso(id_curso):
    curso = Cursos.query.filter_by(id=id_curso).first()
    db.session.delete(curso)
    db.session.commit()
    return redirect(url_for("cursos_lista"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
