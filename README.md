# Fiscal Data OCR Engine

[![CI](https://github.com/SrSatriano/fiscal-data-ocr-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/SrSatriano/fiscal-data-ocr-engine/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![licença](https://img.shields.io/badge/licen%C3%A7a-MIT-22c55e)

Extrai, valida e categoriza dados de notas fiscais brasileiras: o **XML da NF-e/NFC-e**, o **DANFE em PDF**, a **nota de serviço em texto** e **fotos de cupom** (com OCR opcional). Processa uma pasta inteira e gera uma planilha com o total gasto por categoria.

## O que ele faz

- **XML da NF-e 4.00:** lê chave, número, série, data, emitente, destinatário, itens (NCM, CFOP, quantidade, valores) e totais (produtos, nota, ICMS, IPI, PIS, COFINS).
- **Validação de verdade:** confere o dígito verificador de CNPJ, CPF e da chave de acesso. Também confere se a soma dos itens bate com o total. Tudo que não confere aparece como alerta.
- **PDF, texto e imagem:** acha a chave (mesmo com espaços), CNPJs, data e valores rotulados. O CNPJ que o OCR leu errado é descartado pelo DV, em vez de virar dado errado.
- **Categoria da despesa:** pelo NCM (combustível, informática, material de escritório, saúde, alimentação…), pelo CFOP de serviço e por palavras-chave. A nota fica com a categoria que concentra mais valor.
- **Lote:** processa uma pasta, gera CSV (separador `;`, pronto para Excel) e mostra o resumo por categoria. Um arquivo ruim não derruba o lote.

## Uso

```bash
pip install -e .            # + ".[ocr]" para fotos (precisa do Tesseract com o idioma por)
fiscalocr extract examples/
fiscalocr extract ~/notas --csv despesas.csv
fiscalocr extract nota.xml --json
fiscalocr serve             # API em http://127.0.0.1:8090/docs
```

```
nfe_exemplo.xml                2026-11-10 11222333000181    R$ 7.299,00  informatica
nfse_exemplo.txt               2026-11-05 11222333000181    R$ 2.450,00  servicos_ti  ⚠ 1 CNPJ(s) com dígito verificador inválido ignorado(s) — possível erro de OCR
{"documentos": 2, "com_alerta": 1, "total": 9749.0, "por_categoria": {"informatica": 7299.0, "servicos_ti": 2450.0}}
```

API: `POST /extract` com o arquivo (multipart). A resposta é um JSON com documento, itens, totais, categoria, alertas e confiança.

## Testes

São 11 testes:
- validadores de CNPJ, CPF e chave;
- XML completo e com inconsistências;
- recusa de XML com entidades;
- texto com ruído de OCR;
- chave do DANFE com espaços;
- PDF gerado no próprio teste;
- categorias, lote, CSV, CLI e API.

O CI roda em Linux e Windows.

## Limitações

- NFS-e não tem layout nacional único (cada prefeitura tem o seu); por isso a nota de serviço é lida pela rota de texto.
- O OCR de foto depende da qualidade da imagem. A validação por DV evita dado errado, mas não recupera dígito ilegível.

## Autor

Matheus Rodrigues Satriano — [github.com/SrSatriano](https://github.com/SrSatriano)
