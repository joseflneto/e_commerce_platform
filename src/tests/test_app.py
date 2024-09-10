import unittest
import json
from app import app, hash_password, load_data, save_data, create_default_admin, USERS_FILE, PRODUCTS_FILE

class TestLogin(unittest.TestCase):

    def setUp(self):
        # Cria uma aplicação Flask de teste
        self.app = app.test_client()
        self.app.testing = True
        
        # Configura o ambiente de teste
        self.clear_users()
        self.create_test_user()

    def tearDown(self):
        self.clear_users()

    def clear_users(self):
        # Cria um arquivo JSON válido com um dicionário vazio
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)

    def create_test_user(self):
        # Adiciona um usuário de teste
        users = load_data(USERS_FILE)
        users['testuser'] = hash_password('testpassword')
        save_data(USERS_FILE, users)

    def test_login_success(self):
        # Teste de login com credenciais corretas
        response = self.app.post('/login', json=dict(
            username='testuser',
            password='testpassword'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

    def test_login_failure(self):
        # Teste de login com credenciais incorretas
        response = self.app.post('/login', json=dict(
            username='testuser',
            password='wrongpassword'
        ))
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid credentials', response.data)


class TestLoginAndProductAddition(unittest.TestCase):

    def setUp(self):
        # Cria uma aplicação Flask de teste
        self.app = app.test_client()
        self.app.testing = True
        
        # Configura o ambiente de teste
        self.clear_users()
        self.create_test_user()
        self.clear_products()

    def tearDown(self):
        self.clear_users()
        self.clear_products()

    def clear_users(self):
        # Cria um arquivo JSON válido com um dicionário vazio
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)

    def clear_products(self):
        # Cria um arquivo JSON válido com um dicionário vazio
        with open(PRODUCTS_FILE, 'w') as f:
            json.dump({}, f)

    def create_test_user(self):
        # Adiciona um usuário admin com senha admin
        users = load_data(USERS_FILE)
        users['admin'] = hash_password('admin')
        save_data(USERS_FILE, users)

    def login(self, username, password):
        response = self.app.post('/login', json=dict(
            username=username,
            password=password
        ))
        return response

    def add_product(self, product_name, product_price):
        # Adiciona um produto se o usuário estiver logado
        response = self.app.post('/add_product', json=dict(
            name=product_name,
            price=product_price
        ))
        return response

    def test_add_product_success(self):
        # Login como admin
        login_response = self.login('admin', 'admin')
        self.assertEqual(login_response.status_code, 200)
        self.assertIn(b'Login successful', login_response.data)

        # Adiciona um produto
        add_product_response = self.add_product('Test Product', 99.99)
        self.assertEqual(add_product_response.status_code, 201) 
        self.assertIn(b'Product added successfully', add_product_response.data)

        # Verifica se o produto foi adicionado
        products = load_data(PRODUCTS_FILE)[0]
        self.assertEqual(products['name'], "Test Product")
        self.assertEqual(products['price'], 99.99)

    def test_add_product_without_login(self):
        # Tenta adicionar um produto sem estar logado
        add_product_response = self.add_product('Test Product', 99.99)
        self.assertEqual(add_product_response.status_code, 403)
        self.assertIn(b'{"error":"Unauthorized"}', add_product_response.data)


if __name__ == '__main__':
    unittest.main()
