from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from pprint import pprint

app = Flask(__name__)

# Конфиг для M1 (используем mysql-connector вместо flask-mysqldb)
db_config = {
    'host': 'localhost',
    'user': 'praktika_user',
    'password': 'your_password',
    'database': 'praktika_db',
    'auth_plugin': 'mysql_native_password'  # Важно для M1!
}

def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except Error as e:
        print(f"Ошибка подключения: {e}")
        return None

@app.route('/clubs', methods=['GET'])
def get_clubs():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    cursor = conn.cursor(dictionary=True)  # Возвращает словари вместо кортежей
    cursor.execute("SELECT * FROM clubs")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"clubs": result})

# ... остальные роуты остаются такими же, как в предыдущем примере ...

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')