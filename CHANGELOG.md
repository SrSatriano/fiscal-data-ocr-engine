# Changelog

Todas as mudanças notáveis deste projeto são documentadas neste arquivo.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

## [1.1.0] — 2026-11-17

### Adicionado

- Leitura estruturada do XML da NF-e/NFC-e 4.00, com itens e totais.
- Validação de DV de CNPJ, CPF e chave de acesso, e conferência da soma dos itens.
- Extração de PDF (pypdf) e OCR opcional de imagem (Tesseract).
- Categorização por NCM, CFOP e palavras-chave.
- Processamento em lote com CSV e resumo; CLI `fiscalocr`; 11 testes; CI em Linux e Windows.

### Removido

- O "OCR" anterior, que só decodificava bytes como latin-1, e a documentação de deploy que não correspondia ao código.

## [1.0.0] — 2026-03-26

### Adicionado

- Documentação completa em português brasileiro (README e `docs/`)
- Implementação do núcleo descrito no README
- Suíte de testes: `pytest tests/ -q`
- Pipeline CI em `.github/workflows/ci.yml`

### Desempenho

- Benchmarks documentados no README e em `docs/ARCHITECTURE.md`

### Segurança

- Política em [SECURITY.md](SECURITY.md)
- Revisão de dependências na release 1.0.0

## [0.9.0] — 2026-02-15

### Adicionado

- Release candidate com contratos de API estáveis
- Testes de carga em homologação

## [0.1.0] — 2026-01-10

### Adicionado

- Estrutura inicial do repositório e prova de conceito
