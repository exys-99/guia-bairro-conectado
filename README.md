# Guia Bairro Conectado (MVP)

Plataforma web responsiva (*Mobile-First*) desenvolvida para conectar microempreendedores, autônomos e comércios familiares periféricos aos moradores do bairro, unindo busca categorizada com redirecionamento direto ao WhatsApp sem taxas de intermediação.

## Arquitetura e Tecnologias
- **Padrão Arquitetural:** Cliente-Servidor em Camadas com API RESTful desacoplada.
- **Back-end:** Python 3.12, Flask 3.1, SQLAlchemy 2.0.
- **Front-end:** HTML5, CSS3 (Bootstrap 5.3) e JavaScript (Fetch API) com critérios de acessibilidade WCAG 2.1 AA.
- **Banco de Dados:** SQLite (desenvolvimento) e PostgreSQL (produção).
- **Testes Automatizados:** Pytest.

## Estrutura do Projeto
- `app/__init__.py` — Configuração da aplicação Flask, banco de dados e carga inicial de categorias.
- `app/models.py` — Entidades relacionais (`Categoria`, `Estabelecimento`, `ItemCatalogo`).
- `app/routes.py` — Endpoints RESTful (`RF01`, `RF02`, `RF03`) e validação no servidor.
- `app/templates/index.html` & `app/static/js/app.js` — Interface acessível e consumo da API com proteção anti-XSS.
- `tests/test_api.py` — Suíte de testes automatizados.
- `run.py` — Ponto de entrada da aplicação.

## Como Executar Localmente
1. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate