from flask import Flask, render_template, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Azure App Service Environment Variables වලින් දත්ත ගනී
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'password')
DB_NAME = os.environ.get('DB_NAME', 'student_db')

def get_db_connection():
    # මෙතනින් කියන්නේ: 
    # Computer එකේ 'DB_HOST' කියලා Setting එකක් තියෙනවා නම් ඒක ගන්න.
    # නැත්නම් Default එක විදියට DigitalOcean IP එක (165.22.110.232) ගන්න.
    
    db_host = os.environ.get('DB_HOST', '165.22.110.232')
    db_user = os.environ.get('DB_USER', 'remote_user')
    db_pass = os.environ.get('DB_PASS', 'Chathu@12345')
    db_name = os.environ.get('DB_NAME', 'student_db')

    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name
        )
        return conn
    except Exception as e:
        print(f"Connection Failed to {db_host}: {e}")
        return None

@app.route('/')
def index():
    conn = get_db_connection()
    students = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students ORDER BY id DESC LIMIT 50")
        students = cursor.fetchall()
        conn.close()
    return render_template('index.html', students=students)

# 1. DB Connection Status Check Endpoint (AJAX මගින් තත්පරයෙන් තත්පරයට අමතයි)
@app.route('/db-status')
def db_status():
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({"status": "connected", "color": "green"})
    else:
        return jsonify({"status": "disconnected", "color": "red"})

# 2. Add User Endpoint
@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    phone = "569586"  # Dummy fixed part
    course = request.form['course'] # Example: "MSc in IT"
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, phone, course) VALUES (%s, %s, %s)", (name, phone, course))
        conn.commit()
        conn.close()
        return jsonify({"message": "User Added!"})
    return jsonify({"message": "DB Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)