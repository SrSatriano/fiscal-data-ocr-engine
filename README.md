<div align="center">

# Motor de OCR e categorização fiscal

<p>
  <a href="https://github.com/SrSatriano/fiscal-data-ocr-engine"><img src="https://img.shields.io/badge/GitHub-fiscal-data-ocr-engine-24292e?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>
  <a href="https://srsatriano.github.io/portfolio-matheus-satriano/"><img src="https://img.shields.io/badge/Portfólio-web-0891b2?style=for-the-badge" alt="Portfólio" /></a>
</p>

<p>
  <img src="https://img.shields.io/badge/versão-1.0.0-0ea5e9?style=flat-square" alt="versão" />
  <img src="https://img.shields.io/badge/Tier-1-8b5cf6?style=flat-square" alt="tier" />
  <img src="https://img.shields.io/badge/demo-pronto-22c55e?style=flat-square" alt="demo" />
  <img src="https://img.shields.io/badge/licença-MIT-22c55e?style=flat-square" alt="licença" />
  <img src="https://img.shields.io/badge/idioma-pt--BR-blue?style=flat-square" alt="idioma" />
  <img src="https://img.shields.io/badge/CI-GitHub_Actions-8b5cf6?style=flat-square" alt="ci" />
</p>

<p><strong>Extração estruturada de NF-e/NFS-e com validação e categorização para o Brasil.</strong></p>

<p>
  Autor: <a href="https://github.com/SrSatriano">@SrSatriano</a> ·
  Release <strong>1.0.0</strong> (2026-03-26)
</p>

</div>

---

## Índice

1. [Visão geral](#visão-geral)
2. [Problema e solução](#problema-e-solução)
3. [Para quem é](#para-quem-é)
4. [Casos de uso](#casos-de-uso)
5. [Funcionalidades](#funcionalidades)
6. [Stack tecnológica](#stack-tecnológica)
7. [Arquitetura](#arquitetura)
8. [Estrutura do repositório](#estrutura-do-repositório)
9. [Pré-requisitos](#pré-requisitos)
10. [Instalação e execução](#instalação-e-execução)
11. [Configuração](#configuração)
12. [Testes](#testes)
13. [Performance](#performance)
14. [Deploy e operação](#deploy-e-operação)
15. [Limitações conhecidas](#limitações-conhecidas)
16. [Roadmap](#roadmap)
17. [Documentação complementar](#documentação-complementar)
18. [Segurança e licença](#segurança-e-licença)

---

## Visão geral

Este repositório faz parte do **portfólio de engenharia** mantido por [@SrSatriano](https://github.com/SrSatriano). A versão **1.0.0** entrega implementação do núcleo do produto, testes automatizados, pipeline de integração contínua e documentação operacional em **português brasileiro**.

O objetivo é permitir que você clone, execute e evolua o projeto com clareza — do desenvolvimento local ao deploy em produção.

## Problema e solução

| | |
|---|---|
| **Problema** | Digitar notas manualmente gera erros e atraso no fechamento contábil. |
| **Solução** | Upload de PDF/imagem, parsing de CNPJ e valores, categorização por regras. |

## Para quem é

Contadores, BPOs financeiros e ERPs brasileiros.

## Casos de uso

- Fechamento mensal de despesas
- Validação de CNPJ em lote

## Funcionalidades

- [x] Pipeline OCR multi-engine
- [x] Validação de CNPJ e totais
- [x] Categorização por regras (combustível, software, etc.)
- [x] Export CSV e webhook
- [x] Testes pytest

## Stack tecnológica

| Camada | Tecnologias |
|--------|-------------|
| **Principal** | Python, FastAPI, EasyOCR, regras fiscais |

## Arquitetura

```mermaid
flowchart LR
  UP[Upload NF] --> OCR[OCR / parsing]
  OCR --> VAL[Validação CNPJ]
  VAL --> CAT[Categorização fiscal]
  CAT --> ERP[Export CSV / webhook]
```

Detalhamento de componentes, fluxos de dados e decisões de design: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Estrutura do repositório

| Caminho | Descrição |
|---------|-----------|
| `src/extraction/` | Pipeline de extração |
| `src/categorization/` | Regras fiscais |
| `samples/` | Notas de exemplo |

## Pré-requisitos

Python 3.11+.

## Instalação e execução

```bash
git clone https://github.com/SrSatriano/fiscal-data-ocr-engine.git
cd fiscal-data-ocr-engine
```

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

## Configuração

| Variável | Descrição | Exemplo |
|----------|-----------|--------|
| `OCR_LANG` | Idioma EasyOCR | `pt` |

> **Importante:** nunca faça commit de arquivos `.env` com segredos reais. Use `.env.example` como referência.

## Testes

Execute a suíte de testes antes de abrir pull requests:

```bash
pytest tests/ -q
```

A pipeline [`.github/workflows/ci.yml`](.github/workflows/ci.yml) repete build e testes em cada push para `main`.

## Performance

| PDF nativo | Acurácia de campos |
|------------|--------------------|
| | ~98% |

Metodologia, hardware de referência e flags de compilação: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Deploy e operação

| Guia | Conteúdo |
|------|----------|
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Homologação, produção e rollback |
| [docs/OPERATIONS.md](docs/OPERATIONS.md) | Monitoramento, alertas e incidentes |

## Limitações conhecidas

- NF-e XML nativo é mais preciso que OCR em scan

## Roadmap

- Parser XML NF-e
- LLM fallback opcional

## Documentação complementar

| Documento | Descrição |
|-----------|-----------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Arquitetura e decisões técnicas |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Deploy passo a passo |
| [docs/OPERATIONS.md](docs/OPERATIONS.md) | Runbook operacional |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Como contribuir |
| [CHANGELOG.md](CHANGELOG.md) | Histórico de versões |
| [SECURITY.md](SECURITY.md) | Política de segurança |
| [AUTHORS.md](AUTHORS.md) | Créditos |

## Segurança e licença

- Dependências revisadas na release **1.0.0**
- Vulnerabilidades: siga [SECURITY.md](SECURITY.md)
- Licença: [MIT](LICENSE) © SrSatriano 2026

---

<p align="center">
  <a href="https://srsatriano.github.io/portfolio-matheus-satriano/">Portfólio completo</a> ·
  <a href="https://github.com/SrSatriano">@SrSatriano</a> ·
  <a href="https://github.com/SrSatriano/fiscal-data-ocr-engine">Este repositório</a>
</p>
