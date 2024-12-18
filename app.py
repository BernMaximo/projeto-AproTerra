from flask import Flask
from flask import render_template

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASEURI'] = 'sqlite:///meudb.db' #SQLite é o banco de dados predefinido do python
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)

@app.route('/')
def home():
    return render_template('index.html', nome="Usuário")

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/inicio')
def inicio():
    return "Essa é a pagina inicial."
