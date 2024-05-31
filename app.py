from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DATABASE = 'database.db'

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS band_names (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                pet TEXT NOT NULL,
                band_name TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized.")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/generate', methods=['POST'])
def generate_band_name():
    data = request.json
    city = data.get('city')
    pet = data.get('pet')
    
    if not city or not pet:
        return jsonify(error="City and pet names are required"), 400
    
    band_name = f"{city} {pet}"
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO band_names (city, pet, band_name)
            VALUES (?, ?, ?)
        ''', (city, pet, band_name))
        conn.commit()
    except sqlite3.Error as e:
        return jsonify(error=str(e)), 500
    finally:
        conn.close()
    
    return jsonify(bandName=band_name)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
