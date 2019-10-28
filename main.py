from app import app
import pymysql
from db_config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/products', methods=['POST'])
def add():
    try: 
        _json = request.json        
        _name = _json['name']
        _description = _json['description']
        _price = _json['price']
        _stock = _json['stock']

        if request.method == 'POST':
            sql = 'INSERT INTO products(name, description, price, stock) VALUES (%s, %s, %s, %s)'
            data = (_name, _description, _price, _stock)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Product Saved')
            resp.status_code = 200
            return resp
        else:
            return 'not_found'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/products', methods=['GET'])
def all():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM products')
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally: 
        cursor.close()
        conn.close()

@app.route('/products/<int:id>')
def findById(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM PRODUCTS WHERE ID = $s', id)
        row = cursor.fetchone(id)
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally: 
        cursor.close()
        conn.close()

@app.route('/products/<int:id>', methods=['PUT'])
def update(id):
    try:
        _json = request.json
        _id = id
        _name = _json['name']
        _description = _json['description']
        _price = _json['price']
        _stock = _json['stock']

        if request.method == 'PUT':
            sql = 'UPDATE products SET name=%s, description=%s, price=%s, stock=%s WHERE id=%s'
            data = (_name, _description, _price, _stock, _id)
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Product updated')
            resp.status_code = 200
            return resp
    except Exception as e:
        print(e)
    finally: 
        cursor.close()
        conn.close()

@app.route('/products/<int:id>', methods=['DELETE'])
def delete(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM products WHERE id=%s", (id))
		conn.commit()
		resp = jsonify('Product deleted')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()       

if __name__ == "__main__":
    app.run(debug=True, host='192.168.137.2')
