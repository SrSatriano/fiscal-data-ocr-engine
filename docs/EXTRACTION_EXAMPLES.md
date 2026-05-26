# Exemplos de extração

## NF-e XML (ideal)

Parse direto do XML — OCR não necessário. 100% precisão em campos padronizados.

## PDF nativo

Extrair texto com pdfplumber; regex para CNPJ e valores.

## PDF escaneado

Pipeline OCR completo + validação.

## Categorias

| Categoria | Regras |
|-----------|--------|
| material_escritorio | keywords: papel, caneta |
| servicos_ti | CNPJ segmento + keywords |
| combustivel | ANP, posto |

LLM refina quando regras empatarem.
