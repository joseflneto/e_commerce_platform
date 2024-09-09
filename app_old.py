from flask import Flask, request, jsonify
import json
import hashlib

app = Flask(__name__)

# File paths
USERS_FILE = 'users.json'
PRODUCTS_FILE = 'products.json'
CARTS_FILE = 'carts.json'
ORDERS_FILE = 'orders.json'

def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    users = load_data(USERS_FILE)
    password_hash = hash_password(password)
    return users.get(username) == password_hash

def get_user_cart(username):
    carts = load_data(CARTS_FILE)
    return carts.get(username, [])

def add_to_cart(username, product_id):
    carts = load_data(CARTS_FILE)
    cart = carts.get(username, [])
    cart.append(product_id)
    carts[username] = cart
    save_data(CARTS_FILE, carts)

def place_order(username):
    carts = load_data(CARTS_FILE)
    orders = load_data(ORDERS_FILE)
    cart = carts.get(username, [])
    if not cart:
        return "Cart is empty"
    
    order_id = len(orders) + 1
    orders[order_id] = {'username': username, 'products': cart}
    save_data(ORDERS_FILE, orders)
    
    # Clear the cart
    carts[username] = []
    save_data(CARTS_FILE, carts)
    
    return order_id

def get_products():
    return load_data(PRODUCTS_FILE)

# Função para limpar todos os arquivos JSON
def clear_all_files():
    for file in FILES.values():
        open(file, 'w').close()  # Limpa o conteúdo do arquivo

# Rota para limpar todos os arquivos JSON
@app.route('/clear_all', methods=['POST'])
def clear_all():
    clear_all_files()
    return jsonify({"message": "All files have been cleared."}), 200

@app.route('/products', methods=['GET'])
def products():
    products = get_products()
    return jsonify(products), 200

@app.route('/cart', methods=['GET'])
def cart():
    username = request.args.get('username')
    if username:
        cart = get_user_cart(username)
        return jsonify({'cart': cart}), 200
    else:
        return jsonify({'error': 'Username required'}), 400

@app.route('/orders', methods=['GET'])
def orders():
    username = request.args.get('username')
    if username:
        orders = load_data(ORDERS_FILE)
        user_orders = {k: v for k, v in orders.items() if v['username'] == username}
        return jsonify({'orders': user_orders}), 200
    else:
        return jsonify({'error': 'Username required'}), 400

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username and password:
        users = load_data(USERS_FILE)
        if username in users:
            return jsonify({'error': 'User already exists'}), 400
        else:
            users[username] = hash_password(password)
            save_data(USERS_FILE, users)
            return jsonify({'message': 'User registered'}), 201
    else:
        return jsonify({'error': 'Username and password required'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if authenticate_user(username, password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart_route():
    data = request.json
    username = data.get('username')
    product_id = data.get('product_id')
    if username and product_id:
        add_to_cart(username, product_id)
        return jsonify({'message': 'Product added to cart'}), 200
    else:
        return jsonify({'error': 'Username and product_id required'}), 400

@app.route('/place_order', methods=['POST'])
def place_order_route():
    data = request.json
    username = data.get('username')
    if username:
        order_id = place_order(username)
        if isinstance(order_id, int):
            return jsonify({'order_id': order_id}), 200
        else:
            return jsonify({'error': order_id}), 400
    else:
        return jsonify({'error': 'Username required'}), 400

if __name__ == '__main__':
    app.run(port=8080, debug=True)
