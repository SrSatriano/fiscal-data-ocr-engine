"""Extração a partir de texto livre: DANFE em PDF, nota de serviço, cupom ou OCR.

O texto vem do próprio arquivo (.txt), do PDF (pypdf) ou de OCR de imagem
(Tesseract, opcional). Os campos são achados por padrões e só são aceitos se
passarem na validação (DV de CNPJ e da chave), o que filtra lixo de OCR.
"""

from __future__ import annotations

import io
import re
from pathlib import Path

from .categorize import by_text
from .models import Documento, Totais
from .validators import chave_valid, cnpj_valid, only_digits, parse_chave

_CNPJ = re.compile(r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b")
_CHAVE = re.compile(r"(?:\d[\s.]?){44}")
_MONEY = r"(?:R\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})"
_DATE = re.compile(r"\b(\d{2})/(\d{2})/(\d{4})\b")
_LABELS = {
    "nota": [r"valor\s+total\s+(?:da\s+nota|a\s+pagar)", r"valor\s+(?:l[ií]quido|total)", r"total\s+(?:da\s+nota|r\$)"],
    "icms": [r"valor\s+(?:do\s+)?icms(?!\s*st)"],
    "ipi": [r"valor\s+(?:do\s+)?ipi"],
    "desconto": [r"desconto"],
}


def br_float(s: str) -> float:
    return float(s.replace(".", "").replace(",", "."))


def text_from_bytes(data: bytes, name: str) -> tuple[str, str]:
    """Devolve (texto, origem)."""
    suffix = Path(name).suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(data))
        return "\n".join(p.extract_text() or "" for p in reader.pages), "pdf"
    if suffix in {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}:
        try:
            import pytesseract
            from PIL import Image
        except ImportError as exc:
            raise RuntimeError("OCR de imagem precisa do extra 'ocr' e do Tesseract instalado") from exc
        return pytesseract.image_to_string(Image.open(io.BytesIO(data)), lang="por"), "imagem"
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return data.decode(enc), "texto"
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1", errors="ignore"), "texto"


def _labeled_value(text: str, patterns: list[str]) -> float | None:
    for pat in patterns:
        m = re.search(pat + r"[^\d\n]{0,25}" + _MONEY, text, re.IGNORECASE)
        if m:
            return br_float(m.group(1))
    return None


def parse_text(text: str, origem: str = "texto", arquivo: str | None = None) -> Documento:
    doc = Documento(origem=origem, arquivo=arquivo)
    score = 0.0

    for m in _CHAVE.finditer(text):
        d = only_digits(m.group(0))
        if chave_valid(d):
            info = parse_chave(d)
            doc.chave, doc.chave_valida = d, True
            doc.modelo, doc.serie, doc.numero = info["modelo"], info["serie"], info["numero"]
            doc.emitente_cnpj = info["cnpj_emitente"]
            score += 0.4
            break

    cnpjs = [only_digits(m.group(0)) for m in _CNPJ.finditer(text)]
    valid = [c for c in cnpjs if cnpj_valid(c)]
    if not doc.emitente_cnpj and valid:
        doc.emitente_cnpj = valid[0]
    if doc.emitente_cnpj:
        score += 0.2
        others = [c for c in valid if c != doc.emitente_cnpj]
        if others:
            doc.destinatario_doc = others[0]
    invalid = [c for c in cnpjs if c not in valid]
    if invalid:
        doc.alertas.append(f"{len(invalid)} CNPJ(s) com dígito verificador inválido ignorado(s) — possível erro de OCR")

    m = _DATE.search(text)
    if m:
        doc.data_emissao = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
        score += 0.1

    totais = {k: _labeled_value(text, pats) for k, pats in _LABELS.items()}
    if totais["nota"] is None:
        valores = [br_float(v) for v in re.findall(_MONEY, text)]
        if valores:
            totais["nota"] = max(valores)
            doc.alertas.append("valor total inferido como o maior valor do documento")
    else:
        score += 0.3
    doc.totais = Totais(nota=totais["nota"], icms=totais["icms"], ipi=totais["ipi"], desconto=totais["desconto"])

    doc.categoria = by_text(text) or "outros"
    doc.confianca = round(min(score, 1.0), 2)
    return doc
