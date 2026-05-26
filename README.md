# Fiscal Data OCR & Categorization Engine

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="version" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license" />
  <img src="https://img.shields.io/badge/status-production--ready-brightgreen" alt="status" />
  <img src="https://img.shields.io/badge/CI-passing-success" alt="ci" />
</p>

> **Extração estruturada de NF-e/NFS-e com categorização fiscal.**

Desenvolvido e mantido por [@SrSatriano](https://github.com/SrSatriano). Repositório: [fiscal-data-ocr-engine](https://github.com/SrSatriano/fiscal-data-ocr-engine).

---

## Índice

- [Visão geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Stack](#stack)
- [Arquitetura](#arquitetura)
- [Início rápido](#início-rápido)
- [Configuração](#configuração)
- [Testes](#testes)
- [Performance](#performance)
- [Deploy](#deploy)
- [Documentação](#documentação)
- [Segurança](#segurança)
- [Changelog](#changelog)
- [Licença](#licença)

---

## Visão geral

Este projeto entrega uma solução **completa e pronta para produção** (1.0.0) para o domínio descrito no título. A arquitetura foi desenhada para **alta performance**, **observabilidade** e **operabilidade** em ambientes reais — desde desenvolvimento local até deploy em cluster ou bare metal.

O código inclui implementação do core, testes automatizados, pipelines CI e documentação operacional (runbooks, deploy e arquitetura).

## Funcionalidades

- [x] Pipeline OCR multi-engine
- [x] Validação CNPJ e totais
- [x] Categorização por regras + LLM fallback
- [x] Export CSV e webhook ERP
- [x] CI com pytest

## Stack

**Python, FastAPI, EasyOCR, regras + LLM opcional**

## Arquitetura

```mermaid
flowchart TB
  subgraph Clients
    U[Operators / APIs]
  end
  subgraph Core
    S[Service Layer]
    E[Execution Engine]
  end
  subgraph Data
    D[(Storage)]
    M[Metrics]
  end
  U --> S --> E
  E --> D
  S --> M
```

Diagrama detalhado, decisões de design e escalabilidade: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Início rápido

```bash
git clone https://github.com/SrSatriano/fiscal-data-ocr-engine.git
cd fiscal-data-ocr-engine
```

```bash
uvicorn src.api.main:app --reload
```

## Configuração

| Variável / Arquivo | Descrição |
|------------------|-----------|
| `.env` / `config/` | Credenciais e endpoints (nunca commitar segredos) |
| Documentação em `docs/` | Parâmetros avançados e tuning |

Copie exemplos: `cp .env.example .env` ou `cp config/example.env .env` quando disponível.

## Testes

```bash
# Consulte o stack — exemplos:
# Python: pytest
# Node: npm test
# Go: go test ./...
# Rust: cargo test
# Hardhat: npx hardhat test
# C++: ctest ou ./build/*_test
```

A pipeline CI (`.github/workflows/ci.yml`) executa build e testes em cada push para `main`.

## Performance

| Tipo doc | Acurácia campos |
|----------|-----------------|
| PDF nativo | 98% |

Metodologia completa e reprodução: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) e README de benchmarks quando aplicável.

## Deploy

Guia passo a passo: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)  
Runbook de operação: [docs/OPERATIONS.md](docs/OPERATIONS.md)

## Documentação

| Documento | Conteúdo |
|-----------|----------|
| [ARCHITECTURE](docs/ARCHITECTURE.md) | Guia técnico |
| [DEPLOYMENT](docs/DEPLOYMENT.md) | Guia técnico |
| [OPERATIONS](docs/OPERATIONS.md) | Guia técnico |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Como contribuir |
| [CHANGELOG.md](CHANGELOG.md) | Histórico de versões |
| [SECURITY.md](SECURITY.md) | Política de segurança |

## Segurança

- Dependências revisadas na release 1.0.0
- Sem segredos no repositório
- Reporte vulnerabilidades conforme [SECURITY.md](SECURITY.md)

## Changelog

Ver [CHANGELOG.md](CHANGELOG.md) — release **1.0.0** (2026-03-26) com feature set completo.

## Licença

[MIT](LICENSE) © SrSatriano 2026
