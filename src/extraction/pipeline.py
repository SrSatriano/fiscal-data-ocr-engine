import re
from typing import Any


def extract_from_bytes(data: bytes, filename: str) -> dict[str, Any]:
    text = data.decode("utf-8", errors="ignore") if filename.endswith(".txt") else _ocr_extract(data)
    cnpj = _find_cnpj(text)
    valores = re.findall(r"R\$\s*([\d.,]+)", text)
    total = _parse_br_float(valores[0]) if valores else None
    return {
        "cnpj": cnpj,
        "valor_total": total,
        "icms": None,
        "confidence": 0.85 if cnpj else 0.3,
        "raw_text": text[:500],
    }


def _ocr_extract(data: bytes) -> str:
    return data.decode("latin-1", errors="ignore")


def _find_cnpj(text: str) -> str | None:
    m = re.search(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", text)
    return m.group(0).replace(".", "").replace("/", "").replace("-", "") if m else None


def _parse_br_float(s: str) -> float:
    return float(s.replace(".", "").replace(",", "."))
