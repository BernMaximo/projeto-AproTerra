from flask import Flask
from flask import render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', nome="Usuário")

if __name__ == '__main__':
    app.run(debug=True)

app.config['MONGO_URI'] = 'mongodb+srv://gustavomaximo072:400515@aprodatabase.cnvcr.mongodb.net/' #exemplo básico de banco de dados
mongo = PyMongo(app)

@app.route('/adicionar')
def adicionar():
    usuarios = mongo.db.usuarios
    return "Usuário adicionado."

@app.route('/usuarios')
def listar():
    usuarios = mongo.db.usuarios.find()
    return {'usuarios': list(usuarios)}