from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from src.extraction.pipeline import extract_from_bytes
from src.categorization.rules import categorize

app = FastAPI(title="Fiscal OCR Engine", version="0.1.0")


class ExtractionResult(BaseModel):
    cnpj_emitente: str | None
    valor_total: float | None
    icms: float | None
    categoria: str
    confianca_ocr: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/extract", response_model=ExtractionResult)
async def extract(file: UploadFile = File(...)):
    data = await file.read()
    raw = extract_from_bytes(data, file.filename or "doc.pdf")
    cat = categorize(raw)
    return ExtractionResult(
        cnpj_emitente=raw.get("cnpj"),
        valor_total=raw.get("valor_total"),
        icms=raw.get("icms"),
        categoria=cat,
        confianca_ocr=raw.get("confidence", 0.0),
    )
