"""Categorização de despesas por NCM (capítulo/posição), CFOP e palavras-chave."""

from __future__ import annotations

import unicodedata

# Prefixos de NCM → categoria. O prefixo mais longo vence.
NCM_PREFIX = {
    "2710": "combustivel",
    "2711": "combustivel",
    "8471": "informatica",
    "8473": "informatica",
    "8517": "telecom",
    "8523": "informatica",
    "4802": "material_escritorio",
    "4820": "material_escritorio",
    "9608": "material_escritorio",
    "8443": "material_escritorio",
    "3004": "saude",
    "3005": "saude",
    "9018": "saude",
    "02": "alimentacao",
    "04": "alimentacao",
    "07": "alimentacao",
    "08": "alimentacao",
    "09": "alimentacao",
    "10": "alimentacao",
    "16": "alimentacao",
    "17": "alimentacao",
    "19": "alimentacao",
    "20": "alimentacao",
    "21": "alimentacao",
    "2201": "alimentacao",
    "2202": "alimentacao",
    "3401": "limpeza",
    "3402": "limpeza",
    "8703": "veiculos",
    "8708": "veiculos",
    "4011": "veiculos",
    "94": "moveis",
}

KEYWORDS = {
    "combustivel": ["gasolina", "diesel", "etanol", "gnv", "combustivel"],
    "servicos_ti": ["software", "licenca", "cloud", "saas", "hospedagem", "dominio", "suporte tecnico"],
    "informatica": ["notebook", "monitor", "teclado", "mouse", "ssd", "memoria ram"],
    "material_escritorio": ["papel a4", "caneta", "toner", "cartucho", "grampeador"],
    "alimentacao": ["refeicao", "lanche", "restaurante", "cafe", "agua mineral"],
    "telecom": ["internet", "telefonia", "plano movel", "fibra"],
    "transporte": ["uber", "99app", "taxi", "pedagio", "estacionamento", "passagem"],
    "saude": ["medicamento", "farmacia", "consulta"],
}


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def by_ncm(ncm: str | None) -> str | None:
    if not ncm:
        return None
    for size in (4, 2):
        cat = NCM_PREFIX.get(ncm[:size])
        if cat:
            return cat
    return None


def by_text(text: str) -> str | None:
    t = _norm(text)
    best, hits = None, 0
    for cat, words in KEYWORDS.items():
        n = sum(1 for w in words if w in t)
        if n > hits:
            best, hits = cat, n
    return best


def item_category(descricao: str, ncm: str | None, cfop: str | None) -> str:
    if cfop and cfop[1:] in {"933", "949"} and by_text(descricao) == "servicos_ti":
        return "servicos_ti"
    return by_ncm(ncm) or by_text(descricao) or "outros"


def document_category(item_cats: list[tuple[str, float]], fallback_text: str = "") -> str:
    """Categoria do documento = a que concentra mais valor entre os itens."""
    if item_cats:
        weights: dict[str, float] = {}
        for cat, valor in item_cats:
            weights[cat] = weights.get(cat, 0.0) + valor
        return max(weights, key=weights.get)
    return by_text(fallback_text) or "outros"
