from flask import Flask, request, jsonify
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)

@app.route('/dados', methods=['GET'])
def listar_dados():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM dados ORDER BY id DESC LIMIT 10")
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(resultados)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/dados', methods=['POST'])
def receber_dados():
    data = request.get_json()
    
    if not data:
        return jsonify({"erro": "JSON inválido ou ausente"}), 400

    try:
        conn = mysql.connector.connect(
            host='192.168.15.97',            # 192.168.0.33
            user='root',
            password='1234',
            database='aproterra'
        )
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO dados (umidade_ar, umidade_solo, vento, chuva, temperatura)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data['umidade_ar'],
            data['umidade_solo'],
            data['vento'],
            data['chuva'],
            data['temperatura']
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensagem": "Dados inseridos com sucesso"}), 200

    except Exception as e:
        print("Erro ao inserir no banco:", e)
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
