from typing import Any

KEYWORDS = {
    "material_escritorio": ["papel", "caneta", "toner"],
    "servicos_ti": ["software", "licença", "cloud", "saas"],
    "combustivel": ["gasolina", "diesel", "posto"],
}


def categorize(raw: dict[str, Any]) -> str:
    text = (raw.get("raw_text") or "").lower()
    for cat, words in KEYWORDS.items():
        if any(w in text for w in words):
            return cat
    return "outros"
