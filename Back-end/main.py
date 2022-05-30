from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/Rabbit'

db = SQLAlchemy(app)
migrate = Migrate(app,db)

#Model--------------------------------------------------------------------
class Utente(db.Model):
    __tablename__ = 'utente'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    cakeday = db.Column(db.Date, nullable=False)
    karma = db.Column(db.Integer, default=0)

    """def __init__(self,n,e,p,c,k):
        self.nome=n
        self.email=e
        self.password=p
        self.cakeday=c
        self.karma=k"""

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(db.Date, nullable=False)
    upvote = db.Column(db.Integer, default=0)
    idUtente = db.Column(db.Integer, db.ForeignKey('Utente.id'), nullable=False)
    idSub = db.Column(db.Integer, db.ForeignKey('Subrabbit.id'), nullable=False)
    utente = db.relationship('Utente')
    sub = db.relationship('Subrabbit')

class Immagine(db.Model):
    __tablename__ = 'immagine'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    percorso = db.Column(db.String(80), nullable=False)
    tipo = db.Column(db.Enum('Post', 'Subrabbit', 'Avatar'), nullable=False)
    idPost = db.Column(db.Integer, db.ForeignKey('Post.id'), nullable=False)
    idSub = db.Column(db.Integer, db.ForeignKey('Subrabbit.id'), nullable=False)
    idAvatar = db.Column(db.Integer, db.ForeignKey('Utente.id'), nullable=False)
    post = db.relationship('Post')
    sub = db.relationship('Subrabbit')
    avatar = db.relationship('Utente')

class Follow(db.Model):
    __tablename__ = 'follow'
    idUtente = db.Column(db.Integer, db.ForeignKey('Utente.id'), primary_key=True,  nullable=False)
    idSeguito = db.Column(db.Integer, db.ForeignKey('Utente.id'), primary_key=True,  nullable=False)
    data = db.Column(db.Date, nullable=False)
    utente1 = db.relationship('Utente')
    utente2 = db.relationship('Utente')

class Join(db.Model):
    __tablename__ = 'join'
    idUtente = db.Column(db.Integer, db.ForeignKey('Utente.id'), primary_key=True, nullable=False)
    idSub = db.Column(db.Integer, db.ForeignKey('Subrabbit.id'), primary_key=True, nullable=False)
    data = db.Column(db.Date, nullable=False)
    utente = db.relationship('Utente')
    sub = db.relationship('Subrabbit')

class Subrabbit(db.Model):
    __tablename__ = 'subrabbit'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    descrizione = db.Column(db.String(200), nullable=False)

#Control-----------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registra')
def register():
    return render_template('registra.html')

@app.route('/registra/utente', methods = ['POST'])
def insUser():
    n = request.args.get('name')
    e = request.args.get('email')
    p = request.args.get('password')
    c = request.args.get('cakeday')
    k = request.args.get('karma')
    u = Utente()
    u.name = n
    u.email = e
    u.password = p
    u.cakeday = c
    u.karma = k

    db.session.add(u)
    db.session.commit()

    return render_template('index.html')

"""@app.route('/teamD/<name>')
def teamDetail():
    t = db.session.query(Team).filter_by(Team.name == name).first()
    return render_template('teamDetail.html', team=t)"""