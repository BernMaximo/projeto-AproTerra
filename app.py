from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient #conecta com o banco de dados
from bson.objectid import ObjectId
#from werkzeug.security import generate_password_hash

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', nome="Usuário")

@app.route('/add-user', methods=['GET']) #rota para exibir o formulário 
def register_form():
    return render_template('create-login.html')

app.config['MONGO_URI'] = 'mongodb+srv://gustavomaximo072:400515@aprodatabase.cnvcr.mongodb.net/?retryWrites=true&w=majority'
connection_string = "mongodb+srv://gustavomaximo072:400515@aprodatabase.cnvcr.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
db_connection = client["AproDatabase"] #conexão com o banco de dados

collection = db_connection.get_collection("AproCollection") #conexão com a colecão

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
    
    # Validação básica dos dados
    if not username or not celular or not email or not cpf:
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400

    # Hash da senha para segurança
    #hashed_password = generate_password_hash(data['password'])

    # Simulação de inserção no banco de dados
    #db_connection.collection.insert_one({
        #"username": data['username'],
        #"password": hashed_password,
        #"celular": data['celular'],
        #"email": data['email'],
        #"cpf": data['cpf']
    #})
    try:
        collection.insert_one({"username": username, "celular": celular, "email": email, "cpf": cpf})
        return jsonify({"message": f"Usuário {username} registrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao inserir no banco de dados: {str(e)}"}), 500

mongo = PyMongo(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)