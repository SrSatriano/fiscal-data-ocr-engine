# Guia de contribuição

Obrigado por considerar uma contribuição para **Motor de OCR e categorização fiscal**.

## Como começar

1. Faça um fork do repositório [fiscal-data-ocr-engine](https://github.com/SrSatriano/fiscal-data-ocr-engine).
2. Crie uma branch: `git checkout -b feat/minha-melhoria`
3. Instale dependências conforme o [README](README.md).
4. Execute os testes: `pytest tests/ -q`
5. Abra um Pull Request descrevendo **o quê** e **por quê**.

## Padrões de código

- Código claro e autoexplicativo; comentários apenas para invariantes não óbvios.
- Commits no estilo [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `perf:`, `test:`.
- Sem segredos, tokens ou `.env` com credenciais reais.
- Mantenha benchmarks **reproduzíveis** com flags documentadas.

## Pull requests

Inclua:

- Resumo das mudanças
- Como testou (`pytest tests/ -q`)
- Screenshots ou gravações se houver interface visual
- Checklist de breaking changes (se houver)

## Documentação

Alterações de comportamento devem atualizar:

- `README.md`
- Arquivos em `docs/` quando afetar deploy ou arquitetura
- `CHANGELOG.md` na seção *Unreleased* ou nova versão

## Código de conduta

Mantenha discussões respeitosas, técnicas e focadas no mérito da proposta.
