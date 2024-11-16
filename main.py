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

def validate_request_data(data, required_fields):
    if not data:
        return {'success': False, 'error': 'Request must be JSON'}, HTTPStatus.BAD_REQUEST
    for field in required_fields:
        if field not in data:
            return {'success': False, 'error': f'{field} is required'}, HTTPStatus.BAD_REQUEST
    return None

@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.json
    required_fields = ['title', 'author', 'year']
    validation_error = validate_request_data(data, required_fields)
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]

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

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
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

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    required_fields = ['title', 'author', 'year']
    validation_error = validate_request_data(data, required_fields)
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]

    book = find_book(book_id)
    if not book:
        return jsonify({'success': False, 'error': 'Book not found'}), HTTPStatus.NOT_FOUND

    cursor = mysql.connection.cursor()
    query = "UPDATE books SET title = %s, author = %s, year = %s WHERE id = %s"
    cursor.execute(query, (data['title'], data['author'], data['year'], book_id))
    mysql.connection.commit()
    cursor.close()

    updated_book = {
        'id': book_id,
        'title': data['title'],
        'author': data['author'],
        'year': data['year']
    }
    return jsonify({'success': True, 'data': updated_book}), HTTPStatus.OK

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Not found'}), HTTPStatus.NOT_FOUND

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    # Automatically Creates the database and table
    initialize()
    app.run(debug=True)