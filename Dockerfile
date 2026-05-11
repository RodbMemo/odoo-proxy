FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV ODOO_URL=https://memorable-tours.odoo.com
ENV ODOO_API_KEY=3dbbaf8a97daae173757d71ce37ddb515402a7ab
ENV ALLOWED_ORIGINS=*

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
