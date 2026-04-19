from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd  

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
    conn = sqlite3.connect('leads.db')
    df = pd.read_sql_query("SELECT * FROM leads", conn)
    conn.close()

    df.to_excel("leads.xlsx", index=False)
    print("Export triggered")
    return jsonify({"message": "Excel file created"})

if __name__ == '__main__':
    app.run(debug=True)