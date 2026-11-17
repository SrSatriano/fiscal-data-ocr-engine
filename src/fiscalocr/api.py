from __future__ import annotations

from fastapi import FastAPI, File, HTTPException, UploadFile

from .engine import extract
from .models import Documento

app = FastAPI(title="Fiscal Data OCR Engine", version="1.1.0")
MAX_BYTES = 10 * 1024 * 1024


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/extract", response_model=Documento)
async def extract_endpoint(file: UploadFile = File(...)) -> Documento:
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "arquivo maior que 10 MB")
    try:
        return extract(data, file.filename or "documento.txt")
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(422, str(exc)) from exc
