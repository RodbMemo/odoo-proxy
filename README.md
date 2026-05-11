# Odoo CORS Proxy — Memorable XP

Proxy liviano que reenvía llamadas JSON-RPC a Odoo desde el servidor,
eliminando restricciones de CORS para usarlo desde el browser o Claude.

---

## Opción 1 — Correr local (prueba rápida)

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Verificá que funciona:
```
GET http://localhost:8000/health
```

---

## Opción 2 — Docker

```bash
docker build -t odoo-proxy .
docker run -p 8000:8000 odoo-proxy
```

Con variables de entorno personalizadas:
```bash
docker run -p 8000:8000 \
  -e ODOO_URL=https://memorable-tours.odoo.com \
  -e ODOO_API_KEY=tu_api_key \
  -e ALLOWED_ORIGINS=https://tudominio.com \
  odoo-proxy
```

---

## Opción 3 — Deploy en Railway / Render / Fly.io (recomendado)

### Railway
1. Subí esta carpeta a un repositorio de GitHub
2. Creá un proyecto en railway.app y conectá el repo
3. Configurá las variables de entorno en el panel
4. Railway detecta el Dockerfile automáticamente

### Render
1. Nuevo servicio → Web Service → conectá tu repo
2. Runtime: Docker
3. Agregá las variables de entorno

---

## Uso desde el widget de Claude

Una vez desplegado, el proxy queda en una URL como:
`https://tu-proxy.railway.app`

Las llamadas van así:
```
POST https://tu-proxy.railway.app/odoo/web/dataset/call_kw
```
(mismo path que Odoo, pero con el prefijo /odoo/)

---

## Seguridad

- Cambiá `ALLOWED_ORIGINS=*` por tu dominio real en producción
- La API key está en la variable de entorno, no en el código fuente
- El proxy no almacena ningún dato, solo reenvía
