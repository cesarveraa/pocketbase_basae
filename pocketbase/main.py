# main.py
import os
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel

POCKETBASE_URL = os.getenv("POCKETBASE_URL", "http://localhost:8090")
# Si tienes autenticación, usa un token de Admin o de la colección:
ADMIN_TOKEN = os.getenv("PB_ADMIN_TOKEN")  # opcional

headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"} if ADMIN_TOKEN else {}

app = FastAPI()

class RecordData(BaseModel):
    # acepta cualquier JSON
    __root__: Dict[str, Any]

@app.get("/api/custom/{coleccion}")
async def list_records(coleccion: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{POCKETBASE_URL}/api/collections/{coleccion}/records",
            headers=headers
        )
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, resp.text)
    return resp.json()

@app.post("/api/custom/{coleccion}", status_code=201)
async def create_record(coleccion: str, data: RecordData):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{POCKETBASE_URL}/api/collections/{coleccion}/records",
            json=data.__root__,
            headers=headers
        )
    if resp.status_code >= 400:
        raise HTTPException(resp.status_code, resp.text)
    return resp.json()

@app.get("/api/custom/{coleccion}/{id}")
async def get_record(coleccion: str, id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{POCKETBASE_URL}/api/collections/{coleccion}/records/{id}",
            headers=headers
        )
    if resp.status_code == 404:
        raise HTTPException(404, "No encontrado")
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, resp.text)
    return resp.json()

@app.put("/api/custom/{coleccion}/{id}")
async def update_record(coleccion: str, id: str, data: RecordData):
    async with httpx.AsyncClient() as client:
        resp = await client.patch(
            f"{POCKETBASE_URL}/api/collections/{coleccion}/records/{id}",
            json=data.__root__,
            headers=headers
        )
    if resp.status_code >= 400:
        raise HTTPException(resp.status_code, resp.text)
    return resp.json()

@app.delete("/api/custom/{coleccion}/{id}", status_code=204)
async def delete_record(coleccion: str, id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.delete(
            f"{POCKETBASE_URL}/api/collections/{coleccion}/records/{id}",
            headers=headers
        )
    if resp.status_code >= 400:
        raise HTTPException(resp.status_code, resp.text)
    return
