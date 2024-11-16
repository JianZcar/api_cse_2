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

def find_book(book_id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM books WHERE id = %s"
    cursor.execute(query, (book_id,))
    book = cursor.fetchone()
    cursor.close()
    return book

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = find_book(book_id)
    if book:
        return jsonify({'success': True, 'data': book}), HTTPStatus.OK
    return jsonify({'success': False, 'error': 'Book not found'}), HTTPStatus.NOT_FOUND

if __name__ == '__main__':
    initialize()
    app.run(debug=True)