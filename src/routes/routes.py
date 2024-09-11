from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from utils.utils import (
    load_data,
    save_data,
    hash_password,
    authenticate_user,
    get_products,
    add_to_cart,
    place_order,
    load_orders,
    get_product_price,
    clear_all_files
)

routes = Blueprint('routes', __name__)

USERS_FILE = 'data/users.json'
PRODUCTS_FILE = 'data/products.json'
CARTS_FILE = 'data/carts.json'
ORDERS_FILE = 'data/orders.json'

@routes.route('/')
def index():
    logged_in = 'username' in session
    username = session.get('username')
    return render_template('index.html', logged_in=logged_in, username=username)

@routes.route('/product/<product_id>')
def product_detail(product_id):
    products = get_products()
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product_detail.html', product=product)
    else:
        return "Product not found", 404

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
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
    return render_template('register.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        if authenticate_user(username, password):
            session['username'] = username
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    return render_template('login.html')

@routes.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect('/')

@routes.route('/products', methods=['GET'])
def products():
    if 'username' not in session:
        return jsonify({'error': 'You must be logged in to view products'}), 401

    username = session['username']
    products = get_products()
    return render_template('products.html', products=products, username=username)

@routes.route('/product', methods=['GET'])
def product_page():
    if 'username' not in session or session['username'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    return render_template('product.html')

@routes.route('/cart', methods=['GET'])
def cart():
    if 'username' not in session:
        return jsonify({'error': 'You must be logged in to view your cart'}), 401

    username = session['username']
    carts = load_data(CARTS_FILE)
    user_cart = carts.get(username, [])
    products = get_products()
    product_dict = {product['id']: product for product in products}
    user_cart_products = [product_dict.get(pid, {}) for pid in user_cart]
    return render_template('cart.html', cart=user_cart_products, username=username)

@routes.route('/add_to_cart', methods=['POST'])
def add_to_cart_route():
    data = request.json
    username = data.get('username')
    product_id = data.get('product_id')
    if not username or not product_id:
        return jsonify({'error': 'Username and product_id required'}), 400

    carts = load_data(CARTS_FILE)
    if username not in carts:
        carts[username] = []

    carts[username].append(product_id)
    save_data(CARTS_FILE, carts)
    return jsonify({'message': f'Product {product_id} added to {username}\'s cart'}), 200

@routes.route('/place_order', methods=['POST'])
def place_order_route():
    if 'username' not in session:
        return jsonify({'error': 'You must be logged in to place an order'}), 401
    
    username = session['username']  # Get the username from the session
    order_id = place_order(username)

    if isinstance(order_id, str):
        # Redirect to the order screen for the newly created order
        return redirect(url_for('routes.get_order', order_id=order_id))
    else:
        return jsonify({'error': order_id}), 400
    

@routes.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    orders = load_orders()
    products = get_products()  # Assume this returns a list of products
    
    current_username = session.get('username', None)
    if order_id in orders:
        order = orders[order_id]
        if order.get('username') == current_username:
            total = 0
            order_items = []
            
            for product_id, count in order['products'].items():
                price = get_product_price(product_id, products)
                total += price * count
                order_items.append({
                    'id': product_id,
                    'name': next((p['name'] for p in products if p['id'] == product_id), 'Unknown'),
                    'price': price,
                    'count': count
                })
            
            return render_template('order.html', order_items=order_items, order_id=order_id, total=total)
    

@routes.route('/clear_all', methods=['POST'])
def clear_all_route():
    clear_all_files()
    return jsonify({"message": "All files have been cleared."}), 200

@routes.route('/orders')
def orders():
    if 'username' not in session:
        return jsonify({'error': 'You must be logged in to view your orders'}), 401

    username = session['username']
    orders = load_data(ORDERS_FILE)
    user_orders = [order for order in orders.values() if order['username'] == username]
    return render_template('orders.html', orders=user_orders)

@routes.route('/add_product', methods=['POST'])
def add_product():
    if 'username' not in session or session['username'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    name = data.get('name')
    price = data.get('price')
    description = data.get('description', '')
    if not name or not price:
        return jsonify({'error': 'Product name and price required'}), 400

    products = load_data(PRODUCTS_FILE)
    if not isinstance(products, list):
        products = []

    new_id = str(len(products) + 1)
    new_product = {'id': new_id, 'name': name, 'price': price, 'description': description}
    products.append(new_product)
    save_data(PRODUCTS_FILE, products)
    return jsonify({'message': 'Product added successfully'}), 201

@routes.route('/edit_product', methods=['POST'])
def edit_product():
    if 'username' not in session or session['username'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    product_id = data.get('product_id')
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    if not product_id or not name or not price:
        return jsonify({'error': 'Product ID, name, and price are required'}), 400

    products = load_data(PRODUCTS_FILE)
    if not isinstance(products, list):
        return jsonify({'error': 'Product list is corrupted'}), 500

    product_found = False
    for product in products:
        if product['id'] == product_id:
            product['name'] = name
            product['price'] = price
            product['description'] = description
            product_found = True
            break

    if not product_found:
        return jsonify({'error': 'Product not found'}), 404

    save_data(PRODUCTS_FILE, products)
    return jsonify({'message': 'Product updated successfully'}), 200

@routes.route('/remove_product', methods=['POST'])
def remove_product():
    if 'username' not in session or session['username'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    product_id = data.get('product_id')
    if not product_id:
        return jsonify({'error': 'Product ID required'}), 400

    products = load_data(PRODUCTS_FILE)
    if not isinstance(products, list):
        return jsonify({'error': 'Product list is corrupted'}), 500

    new_products = [product for product in products if product['id'] != product_id]
    if len(new_products) == len(products):
        return jsonify({'error': 'Product not found'}), 404

    save_data(PRODUCTS_FILE, new_products)
    return jsonify({'message': 'Product removed successfully'}), 200
