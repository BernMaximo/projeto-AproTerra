from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html') #, nome="Usuário"

@app.route('/add-user', methods=['GET']) #rota para exibir o formulário 
def register_form():
    return render_template('create-login.html')

@app.route('/login-user', methods=['GET']) #rota para exibir o formulário 
def login_form():
    return render_template('login.html')

app.config['MONGO_URI'] = 'mongodb+srv://gustavomaximo072:400515@aprodatabase.cnvcr.mongodb.net/?retryWrites=true&w=majority'
connection_string = "mongodb+srv://gustavomaximo072:400515@aprodatabase.cnvcr.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
db_connection = client["AproDatabase"] #conexão com o banco de dados

collection = db_connection.get_collection("AproCollection") #conexão com a colecão

def generate_user_key(): #gera uma chave de 6 dígitos única
    return str(random.randint(100000, 999999))

@app.route('/add', methods=['POST'])
def add_records():
    try:
        # Obtém os dados enviados no corpo da requisição
        data = request.json
        
        if not data:
            return jsonify({"error": "Nenhum dado enviado!"}), 400
        
        # Insere o registro no MongoDB
        result = collection.insert_one(data)
        
        # Retorna uma resposta de sucesso
        return jsonify({
            "message": "Registro adicionado com sucesso!",
            "id": str(result.inserted_id)  # Converte ObjectId para string
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/read', methods=['GET'])
def read_records():
    try:
        records = list(collection.find())
        for record in records:
            record['_id'] = str(record['_id'])  # Converte ObjectId para string
        return jsonify(records), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update/<id>', methods=['PUT'])
def update_record(id):
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Nenhum dado enviado!"}), 400
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.matched_count == 0:
            return jsonify({"error": "Registro não encontrado!"}), 404
        return jsonify({"message": "Registro atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete/<id>', methods=['DELETE'])
def delete_record(id):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Registro não encontrado!"}), 404
        return jsonify({"message": "Registro deletado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add-user', methods=['POST']) #rota para processar o registro
def add_user():
    if request.content_type == 'application/x-www-form-urlencoded':
            username = request.form.get('username')
            celular = request.form.get('celular')
            email = request.form.get('email')
            cpf = request.form.get('cpf')
    else:
        return jsonify({"error": "Tipo de mídia não suportado."}), 415
    
    if not username or not celular or not email or not cpf:
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400

    #if db_connection.users.find_one():
        #return jsonify({"error": "CPF já cadastrado"}), 409

    user_key = generate_user_key()
    hashed_cpf = generate_password_hash(request.form.get('cpf'))

    user = {
        "user_name": username,
        "celular": celular,
        "email": email,
        "cpf": hashed_cpf,
        "user_key": user_key
    }

    try:
        collection.insert_one(user)
        return jsonify({"message": f"Usuario {username} registrado com sucesso!", "user_key":user_key}), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao inserir no banco de dados: {str(e)}"}), 500

@app.route('/login-user', methods=['POST'])
def login():
    data = list(collection.find())
    user_key = request.form.get('user_key')
    cpf = request.form.get('cpf')

    if not user_key or not cpf:
        return jsonify({"error": "Chave de usuário e CPF são obrigatórios"}), 400
    
    user = collection.find_one({"user_key": user_key})
    username = user["user_name"]
    if user and check_password_hash(user["cpf"], cpf):
        return jsonify({"message": f"Login bem-sucedido, bem vindo {username}"}), 200
    else:
        return jsonify({"error": "Credenciais invalidas"}), 401

mongo = PyMongo(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)