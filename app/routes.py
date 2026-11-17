import re
from datetime import datetime
from urllib.parse import quote
from flask import Blueprint, jsonify, render_template, request
from app import db
from app.models import Categoria, Estabelecimento, ItemCatalogo

bp = Blueprint("main", __name__)


def limpar_texto(valor: str) -> str:
    return re.sub(r"<[^>]*?>", "", (valor or "").strip())


@bp.route("/")
def index():
    categorias = Categoria.query.filter_by(status="ativo").all()
    return render_template("index.html", categorias=categorias)


@bp.route("/api/categorias", methods=["GET"])
def listar_categorias():
    categorias = Categoria.query.filter_by(status="ativo").all()
    return jsonify([{"id": c.id_categoria, "nome": c.nome} for c in categorias])


@bp.route("/api/estabelecimentos", methods=["GET"])
def listar_estabelecimentos():
    categoria_id = request.args.get("categoria", type=int)
    termo = limpar_texto(request.args.get("q", "")).lower()
    hora_agora = datetime.now().strftime("%H:%M")

    query = Estabelecimento.query.filter_by(status_cadastro="ativo")
    if categoria_id:
        query = query.filter_by(id_categoria=categoria_id)

    resultados = []
    for est in query.all():
        itens_ativos = [i for i in est.itens if i.disponivel]
        texto_busca = f"{est.nome_negocio} {est.ponto_referencia} " + " ".join(
            i.titulo for i in itens_ativos
        )
        if termo and termo not in texto_busca.lower():
            continue

        aberto = est.esta_aberto(hora_agora)
        msg = quote(f"Olá! Vi o perfil de {est.nome_negocio} no Guia Bairro Conectado.")
        link_whatsapp = f"https://api.whatsapp.com/send?phone=55{est.telefone_whatsapp}&text={msg}"

        resultados.append(
            {
                "id": est.id_estabelecimento,
                "nome_negocio": est.nome_negocio,
                "categoria": est.categoria.nome,
                "ponto_referencia": est.ponto_referencia,
                "horario": f"{est.horario_abertura}–{est.horario_fechamento}",
                "aberto_agora": aberto,
                "link_whatsapp": link_whatsapp,
                "itens": [
                    {
                        "titulo": item.titulo,
                        "descricao": item.descricao_curta or "",
                        "preco": item.preco_referencia,
                    }
                    for item in itens_ativos
                ],
            }
        )

    return jsonify(resultados)


@bp.route("/api/estabelecimentos", methods=["POST"])
def cadastrar_estabelecimento():
    dados = request.get_json(silent=True) or {}

    nome = limpar_texto(dados.get("nome_negocio"))
    id_categoria = dados.get("id_categoria")
    telefone = re.sub(r"\D", "", str(dados.get("telefone_whatsapp", "")))
    referencia = limpar_texto(dados.get("ponto_referencia"))
    abertura = limpar_texto(dados.get("horario_abertura"))
    fechamento = limpar_texto(dados.get("horario_fechamento"))
    item_titulo = limpar_texto(dados.get("item_titulo"))
    item_preco = dados.get("item_preco")

    if not all([nome, id_categoria, telefone, referencia, abertura, fechamento]):
        return jsonify({"erro": "Preencha todos os campos obrigatórios."}), 400

    if not re.fullmatch(r"\d{10,11}", telefone):
        return (
            jsonify(
                {
                    "erro": "Informe o número de WhatsApp completo com DDD (10 ou 11 dígitos)."
                }
            ),
            400,
        )

    if Estabelecimento.query.filter_by(telefone_whatsapp=telefone).first():
        return jsonify({"erro": "Este número de WhatsApp já está cadastrado."}), 409

    categoria = db.session.get(Categoria, int(id_categoria))
    if not categoria:
        return jsonify({"erro": "Categoria inválida."}), 400

    novo = Estabelecimento(
        id_categoria=categoria.id_categoria,
        nome_negocio=nome,
        telefone_whatsapp=telefone,
        ponto_referencia=referencia,
        horario_abertura=abertura,
        horario_fechamento=fechamento,
    )
    db.session.add(novo)
    db.session.flush()

    if item_titulo:
        preco_val = float(item_preco) if item_preco not in (None, "") else None
        db.session.add(
            ItemCatalogo(
                id_estabelecimento=novo.id_estabelecimento,
                titulo=item_titulo,
                preco_referencia=preco_val,
            )
        )

    db.session.commit()
    return jsonify({"mensagem": "Negócio publicado com sucesso!", "id": novo.id_estabelecimento}), 201