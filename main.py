"""
Odoo CORS Proxy — Memorable XP
Reenvía llamadas JSON-RPC a Odoo desde el servidor, eliminando restricciones de CORS.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(title="Odoo Proxy — Memorable XP")

# ── Configuración ──────────────────────────────────────────────
ODOO_URL = os.getenv("ODOO_URL", "https://memorable-tours.odoo.com")
ODOO_API_KEY = os.getenv("ODOO_API_KEY", "3dbbaf8a97daae173757d71ce37ddb515402a7ab")

# Orígenes permitidos — agregá tu dominio de producción si corresponde
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

# ── Proxy principal ────────────────────────────────────────────
@app.post("/odoo/{path:path}")
async def proxy(path: str, request: Request):
    body = await request.json()
    target = f"{ODOO_URL}/{path}"

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.post(
                target,
                json=body,
                headers={
                    "Content-Type": "application/json",
                    "X-Api-Key": ODOO_API_KEY,
                },
            )
            return resp.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok", "odoo": ODOO_URL}
