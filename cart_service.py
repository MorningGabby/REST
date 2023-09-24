from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Storage for carts
carts = {}

# URL of the deployed Product Service on Render
PRODUCT_SERVICE_URL = 'https://saas-assignment2-iw8y.onrender.com'

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart = carts.get(user_id, {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return jsonify({'cart': list(cart.values()), 'total_price': total_price})

@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    quantity = request.json.get('quantity', 1)
    
    response = requests.get(f'{PRODUCT_SERVICE_URL}/products/{product_id}')
    if response.status_code != 200:
        return jsonify({'message': 'Product not found'}), 404

    product = response.json()
    cart = carts.setdefault(user_id, {})
    
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {'id': product_id, 'name': product['name'], 'price': product['price'], 'quantity': quantity}
    
    return jsonify(cart[product_id])

@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    cart = carts.get(user_id, {})
    if product_id not in cart:
        return jsonify({'message': 'Product not in cart'}), 404

    quantity = request.json.get('quantity', cart[product_id]['quantity'])
    cart[product_id]['quantity'] -= quantity
    
    if cart[product_id]['quantity'] <= 0:
        del cart[product_id]
    
    return jsonify({'message': 'Product quantity updated'})

if __name__ == '__main__':
    app.run(port=5001, debug=True)

