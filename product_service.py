from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.serialize for product in products])

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.serialize)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'], quantity=data['quantity'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.serialize), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Product.query.count() == 0:  #Check if the products table is empty
            #Adding sample products
            sample_products = [
                {'name': 'Apple', 'price': 1.0, 'quantity': 100},
                {'name': 'Banana', 'price': 0.5, 'quantity': 150},
                {'name': 'Orange', 'price': 0.8, 'quantity': 80}
            ]
            for product in sample_products:
                db.session.add(Product(**product))
            db.session.commit()
    app.run(port=5000, debug=True)
