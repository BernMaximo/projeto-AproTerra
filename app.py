from flask import Flask
from flask import render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient #conecta com o banco de dados

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', nome="Usuário")

app.config['MONGO_URI'] = 'mongodb+srv://gustavomaximo072:400515@aprodatabase.cnvcr.mongodb.net/?retryWrites=true&w=majority'
connection_string = "mongodb+srv://gustavomaximo072:400515@aprodatabase.cnvcr.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
db_connection = client["AproDatabase"] #conexão com o banco de dados
print(db_connection), print()

collection = db_connection.get_collection("AproCollection") #conexão com a colecão
print(collection), print()

search_filter = { "Cliente": "João" } #adiciona um filtro de pesquisa
response = collection.find(search_filter)
print(response), print()
for registry in response: print(registry), print()

@app.route('/adicionar')
def adicionar():
    usuarios = mongo.db.usuarios
    return "Usuário adicionado."

@app.route('/usuarios')
def listar():
    usuarios = mongo.db.usuarios.find()
    return {'usuarios': list(usuarios)}

mongo = PyMongo(app)    
if __name__ == '__main__':
    app.run(debug=True)