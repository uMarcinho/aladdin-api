# API de Integração Aladdin

API feita em Django + Django REST Framework que consulta preços de tapetes de um serviço externo e retorna os dados junto com a data informada.

## Tecnologias

- Python 3.10+
- Django 6.0
- Django REST Framework
- drf-yasg (Swagger)
- requests

## Como rodar

Clone o repositório e entre na pasta:

```bash
git clone https://github.com/uMarcinho/aladdin-api.git
cd aladdin-api
```

Crie e ative o ambiente virtual:

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Rode as migrações e suba o servidor:

```bash
python manage.py migrate
python manage.py runserver
```

## Como usar

Acesse a documentação interativa em `http://localhost:8000/swagger/` e teste pelo "Try it out".

Ou direto no navegador:

```
http://localhost:8000/api/precos/?data=2025-06-01
```

## Testes

```bash
python manage.py test precos
```
