from flask import Flask, request, jsonify, render_template, session, redirect
import json
import hashlib

app = Flask(__name__)

# Defina uma chave secreta para usar sessões de forma segura
app.config['SECRET_KEY'] = 'secret_key' 

# Caminhos dos arquivos JSON
USERS_FILE = 'users.json'
PRODUCTS_FILE = 'products.json'
CARTS_FILE = 'carts.json'
ORDERS_FILE = 'orders.json'

# Funções auxiliares
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

# Função para limpar todos os arquivos JSON
def clear_all_files():
    open(USERS_FILE, 'w').close()
    open(PRODUCTS_FILE, 'w').close()
    open(CARTS_FILE, 'w').close()
    open(ORDERS_FILE, 'w').close()

# Rotas

@app.route('/')
def index():
    logged_in = 'username' in session
    username = session.get('username')
    return render_template('index.html', logged_in=logged_in, username=username)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form  # Mudança para request.form, pois estamos lidando com HTML forms
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




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        if authenticate_user(username, password):
            session['username'] = username  # Armazena o username na sessão
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Remove o username da sessão ao fazer logout
    return redirect('/')


@app.route('/products', methods=['GET'])
def products():
    if 'username' not in session:
        return jsonify({'error': 'You must be logged in to view products'}), 401
    
    username = session['username']
    products = get_products()  # Carregar produtos do arquivo JSON
    return render_template('products.html', products=products, username=username)



@app.route('/cart', methods=['GET'])
def cart():
    if 'username' not in session:
        return jsonify({'error': 'You must be logged in to view your cart'}), 401
    
    username = session['username']
    carts = load_data(CARTS_FILE)
    user_cart = carts.get(username, [])
    
    products = get_products()  # Carregar a lista de produtos
    
    # Transformar a lista de produtos em um dicionário para facilitar a busca pelo ID
    product_dict = {product['id']: product for product in products}
    
    # Obter detalhes dos produtos no carrinho usando o dicionário
    user_cart_products = [product_dict.get(pid, {}) for pid in user_cart]
    
    return render_template('cart.html', cart=user_cart_products, username=username)





@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    username = data.get('username')
    product_id = data.get('product_id')
    
    if not username or not product_id:
        return jsonify({'error': 'Username and product_id required'}), 400

    carts = load_data(CARTS_FILE)
    if username not in carts:
        carts[username] = []
    
    # Adiciona o produto ao carrinho do usuário
    carts[username].append(product_id)
    save_data(CARTS_FILE, carts)
    
    return jsonify({'message': f'Product {product_id} added to {username}\'s cart'}), 200


@app.route('/place_order', methods=['POST'])
def place_order_route():
    if 'username' not in session:
        return jsonify({'error': 'You must be logged in to place an order'}), 401
    
    username = session['username']  # Obtém o nome de usuário da sessão
    order_id = place_order(username)
    if isinstance(order_id, int):
        return jsonify({'order_id': order_id}), 200
    else:
        return jsonify({'error': order_id}), 400


@app.route('/clear_all', methods=['POST'])
def clear_all():
    clear_all_files()
    return jsonify({"message": "All files have been cleared."}), 200


@app.route('/orders')
def orders():
    if 'username' not in session:
        return jsonify({'error': 'You must be logged in to view your orders'}), 401
    
    username = session['username']
    orders = load_data(ORDERS_FILE)
    
    # Filtra os pedidos do usuário logado
    user_orders = [order for order in orders.values() if order['username'] == username]
    
    return render_template('orders.html', orders=user_orders)



if __name__ == '__main__':
    app.run(port=8080, debug=True)
