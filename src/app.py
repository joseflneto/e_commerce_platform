from flask import Flask
from routes.routes import routes
from utils.utils import create_default_admin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

# Registra o Blueprint
app.register_blueprint(routes)

if __name__ == '__main__':
    create_default_admin()
    app.run(host='0.0.0.0', port=8080)
