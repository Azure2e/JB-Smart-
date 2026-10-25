# JB Smart – Supermercado online (Django)

## Como correr
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations loja
python manage.py migrate
python manage.py seed           # produtos de exemplo
python manage.py createsuperuser
python manage.py runserver
```
- Loja: http://127.0.0.1:8000/
- Administração (produtos, promoções, stock, encomendas): http://127.0.0.1:8000/admin/

## Produção
Defina `DEBUG=0`, `SECRET_KEY` e `ALLOWED_HOSTS`; use PostgreSQL, Gunicorn, HTTPS
e `python manage.py collectstatic`. O PWA (instalar no telemóvel) exige HTTPS.
# JB-Smart-
