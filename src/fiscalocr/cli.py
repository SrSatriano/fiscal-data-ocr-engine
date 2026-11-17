"""fiscalocr — extrai dados de notas fiscais (XML, PDF, texto, imagem)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import extract, extract_folder, summary, to_csv


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fiscalocr")
    sub = p.add_subparsers(dest="cmd", required=True)
    one = sub.add_parser("extract", help="extrai um arquivo ou uma pasta")
    one.add_argument("path")
    one.add_argument("--csv", help="grava a planilha (separador ;) neste arquivo")
    one.add_argument("--json", action="store_true", help="imprime o JSON completo")
    srv = sub.add_parser("serve", help="sobe a API")
    srv.add_argument("--port", type=int, default=8090)
    args = p.parse_args(argv)

    if args.cmd == "serve":
        import uvicorn

        from .api import app

        uvicorn.run(app, host="127.0.0.1", port=args.port)
        return 0

    path = Path(args.path)
    docs = extract_folder(path) if path.is_dir() else [extract(path.read_bytes(), str(path))]
    if args.csv:
        Path(args.csv).write_text(to_csv(docs), encoding="utf-8-sig")
    if args.json:
        print(json.dumps([d.model_dump() for d in docs], ensure_ascii=False, indent=2))
    else:
        for d in docs:
            alert = f"  ⚠ {'; '.join(d.alertas)}" if d.alertas else ""
            total = (
                f"R$ {d.totais.nota:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                if d.totais.nota
                else "-"
            )
            nome = Path(d.arquivo or "").name
            print(f"{nome:30} {d.data_emissao or '-':10} {d.emitente_cnpj or '-':14} {total:>14}  {d.categoria}{alert}")
        print(json.dumps(summary(docs), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
