from flask import Flask
from config import config
from database.db import create_new_table

# Routes
from routes import infoRoutes

app = Flask(__name__)


def page_not_found(error):
    return '<h1>Not found page</h1>'  # Esto se puede hacer mejor con templates


if __name__ == '__main__':
    app.config.from_object(config['development'])

    # Inicializar database
    create_new_table()

    # Blueprints
    app.register_blueprint(infoRoutes.main, url_prefix='/api/info')

    # Error handlers
    app.register_error_handler(404, page_not_found)
    app.run()
