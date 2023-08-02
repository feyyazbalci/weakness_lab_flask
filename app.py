from flask import Flask, jsonify, request,render_template_string
from werkzeug.datastructures import Headers
from werkzeug.utils import secure_filename
import subprocess
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER']="/home/kali/Desktop/upload"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

DATABASE = 'deneme.db'



@app.route('/products', methods=['GET'])
def get_urunler():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM products')
    data = cursor.fetchall()

    connection.close()

    import logging
    logging.basicConfig(filename="database.log", filemode='w', level=logging.DEBUG)
    logging.debug(data)

    return jsonify(data)

# SQL Injection

@app.route('/urun/<string:name>', methods=['GET'])
def search_urun(name):
 
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("select * from products where name = '%s'" % name)
    data = str(cursor.fetchall())

    connection.close()
    import logging
    logging.basicConfig(filename="database.log", filemode='w', level=logging.DEBUG)
    logging.debug(data)
    return jsonify(data=data),200


# Command Injection

@app.route("/execute_command", methods=['GET'])
def execute_command():
    try:
        command = request.args.get('command')
        data = subprocess.check_output(command, shell=True)
        return data
    except Exception as e:
        error_message = str(e)
        return jsonify(error=error_message), 500

# Server-Side Template Injection (SSTI)

@app.route('/honey')
def hello_ssti():
    name = request.args.get('name', 'Guest')
    template = f'<h1>Hello, {name}!</h1>'
    import logging
    logging.basicConfig(filename="database.log", filemode='w', level=logging.DEBUG)
    logging.debug(str(template))
    return render_template_string(template)

# Brute Force

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user_data = cursor.fetchone()
    connection.close()

    if user_data:
        return jsonify(message="Login successful"), 200
    else:
        return jsonify(message="Login failed"), 401

@app.route('/users', methods=['GET'])
def get_users():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()

    connection.close()

    import logging
    logging.basicConfig(filename="database.log", filemode='w', level=logging.DEBUG)
    logging.debug(data)

    return jsonify(data)


if __name__ == '__main__':


    app.run(debug=True)
