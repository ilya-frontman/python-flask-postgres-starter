from os import environ # for .env use
from flask import Flask, jsonify, request
from db import db
from  Product import Product


app = Flask(__name__)

# app.config['SECRET_KEY'] = environ.get('SECRET_KEY') # example use vars from .env
DB_PORT = environ.get('DB_PORT')

'''
config connection with postgres database

postgres://username:password@container_name/database_name
'''

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{environ.get('DB_USER')}:{environ.get('DB_PASSWORD')}@pgdb/{environ.get('DB_NAME')}"
db.init_app(app)

# curl -v http://localhost:5000/products
@app.route('/products')
def get_products():
    products = [product.json for product in Product.find_all()]
    return jsonify(products)


# curl -v http://localhost:5000/product/1
@app.route('/product/<int:id>')
def get_product(id):
    product = Product.find_by_id(id)
    if product:
        return jsonify(product)
    return f'Product with id {id} not found', 404


# curl --header "Content-type: application/json" --request POST --data '{"name": "Product 3"}' -v http://localhost:5000/product
@app.route('/product', methods=['POST'])
def post_product():
    # Retrieve the product from request body
    request_product = request.json

    # Create new product
    product = Product(None, request_product['name'])

    # Save new product to db
    product.save_to_db()

    return jsonify(product.json), 201


# curl --header "Content-type: application/json" --request PUT --data '{"name": "Updated Product 2"}' -v http://localhost:5000/product/2
@app.route('/product/<int:id>', methods=['PUT'])
def put_product(id):
    
    existing_product = Product.find_by_id(id)

    if existing_product:
        # Get the request payload
        updated_product = request.json

        existing_product.name = updated_product['name']
        existing_product.save_to_db()

        return jsonify(existing_product.json), 200

    return f"Product with id {id} not found", 404


# curl --request DELETE -v http://localhost:5000/product/2
@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    existing_product = Product.find_by_id(id)

    if existing_product:
        existing_product.delete_from_db()
        return jsonify({'message':f'Product with id {id} deleted'}), 200

    return f'Product with id {id} not found', 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') # default 0.0.0.0
