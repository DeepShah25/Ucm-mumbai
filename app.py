from flask import Flask, request, jsonify,send_file
from flask_cors import CORS
import sqlite3
import pandas as pd  
import os

app = Flask(__name__)
CORS(app)

# ✅ Create database + table
def init_db():
    conn = sqlite3.connect('leads.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT UNIQUE,
            location TEXT,
            service TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ✅ Test route
@app.route('/')
def home():
    return "Backend is running 🚀"

# ✅ Save data to DB
@app.route('/submit', methods=['POST'])
def submit():
    data = request.json

    try:
        conn = sqlite3.connect('leads.db')
        c = conn.cursor()

        c.execute(
            "INSERT INTO leads (name, phone, location, service) VALUES (?, ?, ?, ?)",
            (data['name'], data['phone'], data['location'], data['service'])
        )

        conn.commit()
        conn.close()

        return jsonify({"message": "Saved successfully"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Duplicate or error"}), 400


# ✅ View all data (for testing)
@app.route('/leads', methods=['GET'])
def get_leads():
    conn = sqlite3.connect('leads.db')
    c = conn.cursor()

    c.execute("SELECT * FROM leads")
    rows = c.fetchall()

    conn.close()

    return jsonify(rows)
@app.route('/export', methods=['GET'])
def export():
    try:
        # 1. Connect and Read
        conn = sqlite3.connect('leads.db')
        df = pd.read_sql_query("SELECT * FROM leads", conn)
        conn.close()

        # 2. Check if data exists
        if df.empty:
            return jsonify({"message": "No leads found to export"}), 404

        # 3. Create the Excel file
        file_path = "leads.xlsx"
        df.to_excel(file_path, index=False)

        # 4. Send the file to the user
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        # This is the 'except' clause your code was missing!
        print(f"Export Error: {e}")
        return jsonify({"error": "Could not generate Excel file"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)