from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
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

@app.route('/generate', methods=['POST'])
def generate_band_name():
    data = request.json
    city = data['city']
    pet = data['pet']
    band_name = f"{city} {pet}"
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO band_names (city, pet, band_name)
        VALUES (?, ?, ?)
    ''', (city, pet, band_name))
    conn.commit()
    conn.close()
    
    return jsonify(bandName=band_name)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
