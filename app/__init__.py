import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///guia_bairro.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()
        seed_categorias_iniciais()

    return app


def seed_categorias_iniciais():
    from app.models import Categoria

    if Categoria.query.count() == 0:
        iniciais = [
            Categoria(nome="Alimentação", descricao="Marmitas, lanches e doces"),
            Categoria(nome="Reparos", descricao="Manutenção e consertos"),
            Categoria(nome="Beleza", descricao="Salão, barbearia e estética"),
            Categoria(nome="Comércio", descricao="Mercadinhos e variedades"),
        ]
        db.session.add_all(iniciais)
        db.session.commit()