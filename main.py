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

@app.route('/api/books', methods=['POST'])
def create_book():
    if not request.json:
        return jsonify({'success': False, 'error': 'Request must be JSON'}), HTTPStatus.BAD_REQUEST
    data = request.json
    # Validation
    required_fields = ['title', 'author', 'year']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'error': f'{field} is required'}), HTTPStatus.BAD_REQUEST

    cursor = mysql.connection.cursor()
    query = "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)"
    cursor.execute(query, (data['title'], data['author'], data['year']))
    mysql.connection.commit()
    new_book_id = cursor.lastrowid
    cursor.close()

    new_book = {
        'id': new_book_id,
        'title': data['title'],
        'author': data['author'],
        'year': data['year']
    }
    return jsonify({'success': True, 'data': new_book}), HTTPStatus.CREATED

@app.route('/api/books/<int:book_id>/delete', methods=['DELETE'])
def delete_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({'success': False, 'error': 'Book not found'}), HTTPStatus.NOT_FOUND

    cursor = mysql.connection.cursor()
    query = "DELETE FROM books WHERE id = %s"
    cursor.execute(query, (book_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'success': True, 'message': 'Book deleted successfully'}), HTTPStatus.OK

if __name__ == '__main__':
    initialize()
    app.run(debug=True)