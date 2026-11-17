# Arquitetura

```
src/fiscalocr/
  validators.py    DV de CNPJ, CPF e chave de acesso (módulo 11); decomposição da chave
  nfe_xml.py       XML da NF-e/NFC-e 4.00: ide, emit, dest, det/prod, ICMSTot
  text_extract.py  texto de .txt, PDF (pypdf) ou imagem (Tesseract) → campos por padrão
  categorize.py    categoria por prefixo de NCM, CFOP de serviço e palavras-chave
  engine.py        roteamento por tipo, lote de pasta, CSV e resumo por categoria
  api.py / cli.py  FastAPI e linha de comando
```

## Duas rotas de extração

1. **XML (precisão total).** Leitura estruturada do layout oficial. Mesmo assim, a chave e os documentos passam pela validação de DV, e a soma dos itens é conferida contra `vProd`. Divergências viram `alertas`, nunca são escondidas.
2. **Texto, PDF ou imagem (heurística).** Cada campo é achado por padrão:
   - **chave:** 44 dígitos, mesmo separados por espaço;
   - **CNPJ:** com ou sem pontuação;
   - **datas:** no formato brasileiro;
   - **valores:** procurados perto de rótulos como "valor total da nota", "valor do ICMS".

   Só é aceito o que passa na validação. Um CNPJ que o OCR leu errado tem o DV quebrado, é descartado e vira alerta. A `confianca` soma pesos dos campos achados: chave 0,4, CNPJ 0,2, data 0,1 e total rotulado 0,3.

## Categorias

A categoria de cada item vem do NCM (o prefixo mais longo vence). Sem NCM, vem das palavras-chave da descrição. A categoria do documento é a que concentra mais **valor** entre os itens; em texto livre, são as palavras-chave do documento inteiro.

## Segurança

- XML com DTD/ENTITY é recusado (proteção contra XXE e "billion laughs").
- A API limita uploads a 10 MB e só escuta em 127.0.0.1 quando iniciada pela CLI.
