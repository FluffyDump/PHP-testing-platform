from flask import Flask, request, jsonify, session
import psycopg2
import os
import bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'key'

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='PHP_Testing_System',
        user='postgres',
        password='Password1234'
    )
    return conn

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    password = data['password']

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the username already exists
        cur.execute('SELECT * FROM "User" WHERE username = %s', (username,))
        if cur.fetchone() is not None:
            return jsonify(message='Vartotojo vardas užimtas!'), 400

        # Check if the email already exists
        cur.execute('SELECT * FROM "User" WHERE email = %s', (email,))
        if cur.fetchone() is not None:
            return jsonify(message='Naudotojas su tokiu elektroniniu paštu jau registruotas!'), 400

        # If both username and email are available, insert the new user
        cur.execute(
            'INSERT INTO "User" (username, name, surname, email, password_hash, registration_date) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP) RETURNING user_id',
            (username, first_name, last_name, email, hashed_password)
        )

        user_id = cur.fetchone()[0]  # Retrieve the newly created user's ID

        # Insert the user ID into the student table
        cur.execute('INSERT INTO student (user_id) VALUES (%s)', (user_id,))
        
        conn.commit()
        return jsonify(message='Registracija sekminga.'), 201
    except Exception as e:
        print(error=str(e))
        return jsonify(message='Ivyko klaida registruojant naudotoją!'), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT user_id, password_hash FROM "User" WHERE username = %s', (username,))
        result = cur.fetchone()

        if result:
            user_id, password_hash = result
            # Verify the password
            if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                # Check if user is in student or teacher table
                cur.execute('SELECT COUNT(*) FROM student WHERE user_id = %s', (user_id,))
                is_student = cur.fetchone()[0] > 0
                
                cur.execute('SELECT COUNT(*) FROM teacher WHERE user_id = %s', (user_id,))
                is_teacher = cur.fetchone()[0] > 0
                
                # Start a session and store user ID and role
                session['user_id'] = user_id
                session['role'] = 'student' if is_student else 'teacher' if is_teacher else 'student'

                return jsonify(message='Login successful!', user_id=user_id, role=session['role']), 200
            else:
                return jsonify(message='Neteisingas vartotojo vardas arba slaptažodis!'), 401
        else:
            return jsonify(message='Neteisingas vartotojo vardas arba slaptažodis!'), 401
    except Exception as e:
        print(error=str(e))
        return jsonify(message='Serverio klaida!'), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/create_test', methods=['POST'])
def create_test():
    data = request.get_json()
    title = data['title']
    description = data.get('description', '')
    teacher_id = data['teacher_id']

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO Test (title, description, fk_teacheruser_id) VALUES (%s, %s, %s) RETURNING test_id',
            (title, description, teacher_id)
        )
        test_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()
        return jsonify(message='Test created successfully!', test_id=test_id), 201
    except Exception as e:
        return jsonify(message='Error creating test', error=str(e)), 500
    
@app.route('/create_question', methods=['POST'])
def create_question():
    data = request.get_json()
    question_text = data['question_text']
    correct_answer = data['correct_answer']
    test_id = data['test_id']

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO Question (question_text, correct_answer, fk_testtest_id) VALUES (%s, %s, %s)',
            (question_text, correct_answer, test_id)
        )

        conn.commit()
        cur.close()
        conn.close()
        return jsonify(message='Question created successfully!'), 201
    except Exception as e:
        return jsonify(message='Error creating question', error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
