from __future__ import annotations

import csv
import io
from pathlib import Path

from .models import Documento
from .nfe_xml import parse_nfe_xml
from .text_extract import parse_text, text_from_bytes

SUPPORTED = {".xml", ".txt", ".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}


def extract(data: bytes, name: str) -> Documento:
    if Path(name).suffix.lower() == ".xml" or data.lstrip()[:5] == b"<?xml":
        return parse_nfe_xml(data, name)
    text, origem = text_from_bytes(data, name)
    return parse_text(text, origem, name)


def extract_folder(folder: str | Path) -> list[Documento]:
    out = []
    for f in sorted(Path(folder).rglob("*")):
        if f.suffix.lower() not in SUPPORTED:
            continue
        try:
            out.append(extract(f.read_bytes(), str(f)))
        except Exception as exc:  # um arquivo ruim não derruba o lote
            out.append(Documento(origem="erro", arquivo=str(f), alertas=[f"falha ao ler: {exc}"]))
    return out


CSV_FIELDS = [
    "arquivo",
    "origem",
    "modelo",
    "numero",
    "serie",
    "data_emissao",
    "emitente_cnpj",
    "emitente_nome",
    "destinatario_doc",
    "valor_nota",
    "icms",
    "ipi",
    "categoria",
    "chave",
    "chave_valida",
    "confianca",
    "alertas",
]


def to_csv(docs: list[Documento]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CSV_FIELDS, delimiter=";")
    w.writeheader()
    for d in docs:
        w.writerow(
            {
                "arquivo": d.arquivo,
                "origem": d.origem,
                "modelo": d.modelo,
                "numero": d.numero,
                "serie": d.serie,
                "data_emissao": d.data_emissao,
                "emitente_cnpj": d.emitente_cnpj,
                "emitente_nome": d.emitente_nome,
                "destinatario_doc": d.destinatario_doc,
                "valor_nota": d.totais.nota,
                "icms": d.totais.icms,
                "ipi": d.totais.ipi,
                "categoria": d.categoria,
                "chave": d.chave,
                "chave_valida": d.chave_valida,
                "confianca": d.confianca,
                "alertas": " | ".join(d.alertas),
            }
        )
    return buf.getvalue()


def summary(docs: list[Documento]) -> dict:
    by_cat: dict[str, float] = {}
    for d in docs:
        if d.totais.nota:
            by_cat[d.categoria] = round(by_cat.get(d.categoria, 0.0) + d.totais.nota, 2)
    return {
        "documentos": len(docs),
        "com_alerta": sum(1 for d in docs if d.alertas),
        "total": round(sum(d.totais.nota or 0 for d in docs), 2),
        "por_categoria": dict(sorted(by_cat.items(), key=lambda kv: -kv[1])),
    }
