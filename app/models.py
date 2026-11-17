from datetime import datetime, timezone
from app import db


class Categoria(db.Model):
    __tablename__ = "categorias"

    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="ativo")

    estabelecimentos = db.relationship("Estabelecimento", backref="categoria", lazy=True)


class Estabelecimento(db.Model):
    __tablename__ = "estabelecimentos"

    id_estabelecimento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_categoria = db.Column(
        db.Integer, db.ForeignKey("categorias.id_categoria"), nullable=False
    )
    nome_negocio = db.Column(db.String(120), nullable=False)
    telefone_whatsapp = db.Column(db.String(15), unique=True, nullable=False)
    ponto_referencia = db.Column(db.String(200), nullable=False)
    horario_abertura = db.Column(db.String(5), nullable=False)
    horario_fechamento = db.Column(db.String(5), nullable=False)
    status_cadastro = db.Column(db.String(20), nullable=False, default="ativo")
    data_criacao = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    itens = db.relationship(
        "ItemCatalogo", backref="estabelecimento", lazy=True, cascade="all, delete-orphan"
    )

    def esta_aberto(self, hora_atual_str: str) -> bool:
        if self.horario_abertura <= self.horario_fechamento:
            return self.horario_abertura <= hora_atual_str <= self.horario_fechamento
        return hora_atual_str >= self.horario_abertura or hora_atual_str <= self.horario_fechamento


class ItemCatalogo(db.Model):
    __tablename__ = "itens_catalogo"

    id_item = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_estabelecimento = db.Column(
        db.Integer, db.ForeignKey("estabelecimentos.id_estabelecimento"), nullable=False
    )
    titulo = db.Column(db.String(120), nullable=False)
    descricao_curta = db.Column(db.String(250), nullable=True)
    preco_referencia = db.Column(db.Float, nullable=True)
    disponivel = db.Column(db.Boolean, nullable=False, default=True)