#Gabriella Rivera
#Assignment 2
from flask import Flask, jsonify, request

app = Flask(__name__)

#list of products
products = [
    {'id': 1, 'name': 'Apple', 'price': 1.0, 'quantity': 100},
    {'id': 2, 'name': 'Banana', 'price': 0.5, 'quantity': 150},
    {'id': 3, 'name': 'Orange', 'price': 0.8, 'quantity': 80},
]

@app.route('/products', methods=['GET'])
def get_products():
    #return list
    return jsonify(products)
    
#find product with product id
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((product for product in products if product['id'] == product_id), None)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product)

#adds new product to list by extracting data from request
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    product_id = max(product['id'] for product in products) + 1
    new_product = {'id': product_id, 'name': data['name'], 'price': data['price'], 'quantity': data['quantity']}
    products.append(new_product)
    return jsonify(new_product), 201

if __name__ == '__main__':
    app.run(port=5000, debug=True)

