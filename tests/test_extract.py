from src.extraction.pipeline import extract_from_bytes
from src.categorization.rules import categorize


def test_extract_txt_cnpj():
    raw = b"CNPJ 12.345.678/0001-90 Valor Total R$ 1.234,56"
    data = extract_from_bytes(raw, "nota.txt")
    assert data["cnpj"] == "12345678000190"
    assert data["valor_total"] == 1234.56


def test_categorize_combustivel():
    raw = {"raw_text": "posto gasolina diesel", "cnpj": None}
    assert categorize(raw) == "combustivel"
