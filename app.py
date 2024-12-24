from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient #conecta com o banco de dados
from bson.objectid import ObjectId

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', nome="Usuário")

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

# Rota para ler todos os registros
@app.route('/read', methods=['GET'])
def read_records():
    try:
        records = list(collection.find())
        for record in records:
            record['_id'] = str(record['_id'])  # Converte ObjectId para string
        return jsonify(records), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para atualizar um registro
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

# Rota para deletar um registro
@app.route('/delete/<id>', methods=['DELETE'])
def delete_record(id):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Registro não encontrado!"}), 404
        return jsonify({"message": "Registro deletado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

mongo = PyMongo(app)
if __name__ == '__main__':
    app.run(debug=True)