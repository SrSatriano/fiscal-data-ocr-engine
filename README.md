# Fiscal Data OCR & Categorization Engine

Ingere PDFs de notas fiscais, extrai dados estruturados (CNPJ, valores, impostos), categoriza gastos e exporta CSV ou envia a ERPs via webhook.

## Stack

- Python, EasyOCR / Tesseract
- OpenAI API ou LLM local (opcional)
- FastAPI

## Antes e depois do processamento

### Entrada (PDF escaneado)

```
[Imagem] NOTA FISCAL ELETRÔNICA
CNPJ: 12.345.678/0001-90
Valor Total: R$ 1.234,56
ICMS: R$ 123,45
```

### Saída (JSON)

```json
{
  "cnpj_emitente": "12345678000190",
  "valor_total": 1234.56,
  "icms": 123.45,
  "categoria": "material_escritorio",
  "confianca_ocr": 0.94
}
```

Mais exemplos: [samples/](samples/) | [docs/EXTRACTION_EXAMPLES.md](docs/EXTRACTION_EXAMPLES.md)

## Tolerância a falhas no OCR

1. **Pré-processamento**: deskew, binarização adaptativa, upscale 2×.
2. **Multi-engine**: Tesseract + EasyOCR; voto por campo.
3. **Validação**: checksum CNPJ, soma impostos ≈ total (±1%).
4. **LLM fallback**: campos com confiança < 0.8 passam por extração estruturada.
5. **Fila humana**: `status=review_required` no dashboard interno.

Detalhes: [docs/OCR_RESILIENCE.md](docs/OCR_RESILIENCE.md)

## Integração contínua (CI/CD)

```yaml
# .github/workflows/ci.yml
- run: pip install -r requirements.txt
- run: pytest tests/ -v
- run: python -m src.ocr.benchmark --samples samples/
```

## Webhook ERP

```bash
POST /export/webhook
{
  "erp_url": "https://erp.example/hooks/nfe",
  "document_ids": ["doc_001"]
}
```

## Uso

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
python -m src.ingestion.cli samples/nota_exemplo.pdf
```
