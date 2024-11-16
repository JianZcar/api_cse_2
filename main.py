from sql_init import initialize_database
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from http import HTTPStatus

def initialize():
    config = {
        'user': 'root',
        'password': '',
        'host': '127.0.0.1'
    }

    initialize_database(config)

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'api_cse2'
app.config['MYSQL_HOST'] = '127.0.0.1'

mysql = MySQL(app)

@app.route('/api/books', methods=['GET'])
def get_books():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    return jsonify({'success': True, 'data': books, 'total': len(books)}), HTTPStatus.OK

if __name__ == '__main__':
    initialize()
    app.run(debug=True)