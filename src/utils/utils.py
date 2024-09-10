import json
import hashlib

USERS_FILE = 'data/users.json'
PRODUCTS_FILE = 'data/products.json'
CARTS_FILE = 'data/carts.json'
ORDERS_FILE = 'data/orders.json'

def create_default_admin():
    users = load_data(USERS_FILE)
    if 'admin' not in users:
        users['admin'] = hash_password('admin')
        save_data(USERS_FILE, users)

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
    
    # Limpar o carrinho após o pedido
    carts[username] = []
    save_data(CARTS_FILE, carts)
    
    return order_id

def get_products():
    return load_data(PRODUCTS_FILE)

def clear_all_files():
    open(USERS_FILE, 'w').close()
    open(PRODUCTS_FILE, 'w').close()
    open(CARTS_FILE, 'w').close()
    open(ORDERS_FILE, 'w').close()
