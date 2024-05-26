from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///missions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Importar rotas para registrar as rotas
from app.controllers import routes

# Criar tabelas do banco de dados, se não existirem
with app.app_context():
    db.create_all()
