from __future__ import annotations

from pydantic import BaseModel, Field


class Item(BaseModel):
    codigo: str | None = None
    descricao: str
    ncm: str | None = None
    cfop: str | None = None
    quantidade: float | None = None
    valor_unitario: float | None = None
    valor_total: float
    categoria: str = "outros"


class Totais(BaseModel):
    produtos: float | None = None
    nota: float | None = None
    icms: float | None = None
    ipi: float | None = None
    pis: float | None = None
    cofins: float | None = None
    desconto: float | None = None
    frete: float | None = None


class Documento(BaseModel):
    origem: str  # "xml" | "texto" | "pdf" | "imagem"
    arquivo: str | None = None
    modelo: str | None = None  # "55" NF-e, "65" NFC-e
    chave: str | None = None
    chave_valida: bool | None = None
    numero: int | None = None
    serie: int | None = None
    data_emissao: str | None = None
    emitente_cnpj: str | None = None
    emitente_nome: str | None = None
    destinatario_doc: str | None = None
    destinatario_nome: str | None = None
    itens: list[Item] = Field(default_factory=list)
    totais: Totais = Field(default_factory=Totais)
    categoria: str = "outros"
    alertas: list[str] = Field(default_factory=list)
    confianca: float = 0.0  # 1.0 para XML; heurística para texto/OCR
