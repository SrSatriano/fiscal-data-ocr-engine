"""Leitura do XML da NF-e / NFC-e (layout 4.00 do Portal da Nota Fiscal)."""

from __future__ import annotations

from xml.etree import ElementTree as ET

from .categorize import document_category, item_category
from .models import Documento, Item, Totais
from .validators import chave_valid, cnpj_valid, cpf_valid, only_digits

NS = {"n": "http://www.portalfiscal.inf.br/nfe"}


def _t(el, path: str) -> str | None:
    found = el.find(path, NS) if el is not None else None
    return found.text.strip() if found is not None and found.text else None


def _f(el, path: str) -> float | None:
    v = _t(el, path)
    return float(v) if v not in (None, "") else None


def parse_nfe_xml(data: bytes, arquivo: str | None = None) -> Documento:
    # Proteção básica contra XML malicioso: sem DTD/entidades.
    if b"<!DOCTYPE" in data[:2048] or b"<!ENTITY" in data[:4096]:
        raise ValueError("XML com DTD/entidades não é aceito")
    root = ET.fromstring(data)
    inf = root.find(".//n:infNFe", NS)
    if inf is None:
        raise ValueError("não é um XML de NF-e (infNFe ausente)")

    doc = Documento(origem="xml", arquivo=arquivo, confianca=1.0)
    chave = only_digits(inf.get("Id", ""))
    if not chave:
        chave = only_digits(_t(root, ".//n:protNFe/n:infProt/n:chNFe") or "")
    doc.chave = chave or None
    doc.chave_valida = chave_valid(chave) if chave else None
    if doc.chave and not doc.chave_valida:
        doc.alertas.append("dígito verificador da chave de acesso não confere")

    ide = inf.find("n:ide", NS)
    doc.modelo = _t(ide, "n:mod")
    doc.serie = int(_t(ide, "n:serie") or 0)
    doc.numero = int(_t(ide, "n:nNF") or 0)
    dh = _t(ide, "n:dhEmi") or _t(ide, "n:dEmi")
    doc.data_emissao = dh[:10] if dh else None

    emit = inf.find("n:emit", NS)
    doc.emitente_cnpj = _t(emit, "n:CNPJ") or _t(emit, "n:CPF")
    doc.emitente_nome = _t(emit, "n:xNome")
    if doc.emitente_cnpj and len(doc.emitente_cnpj) == 14 and not cnpj_valid(doc.emitente_cnpj):
        doc.alertas.append("CNPJ do emitente inválido")

    dest = inf.find("n:dest", NS)
    if dest is not None:
        doc.destinatario_doc = _t(dest, "n:CNPJ") or _t(dest, "n:CPF")
        doc.destinatario_nome = _t(dest, "n:xNome")
        d = doc.destinatario_doc or ""
        if (len(d) == 14 and not cnpj_valid(d)) or (len(d) == 11 and not cpf_valid(d)):
            doc.alertas.append("documento do destinatário inválido")

    cats: list[tuple[str, float]] = []
    for det in inf.findall("n:det", NS):
        prod = det.find("n:prod", NS)
        desc = _t(prod, "n:xProd") or ""
        ncm, cfop = _t(prod, "n:NCM"), _t(prod, "n:CFOP")
        item = Item(
            codigo=_t(prod, "n:cProd"),
            descricao=desc,
            ncm=ncm,
            cfop=cfop,
            quantidade=_f(prod, "n:qCom"),
            valor_unitario=_f(prod, "n:vUnCom"),
            valor_total=_f(prod, "n:vProd") or 0.0,
            categoria=item_category(desc, ncm, cfop),
        )
        doc.itens.append(item)
        cats.append((item.categoria, item.valor_total))

    tot = inf.find("n:total/n:ICMSTot", NS)
    doc.totais = Totais(
        produtos=_f(tot, "n:vProd"),
        nota=_f(tot, "n:vNF"),
        icms=_f(tot, "n:vICMS"),
        ipi=_f(tot, "n:vIPI"),
        pis=_f(tot, "n:vPIS"),
        cofins=_f(tot, "n:vCOFINS"),
        desconto=_f(tot, "n:vDesc"),
        frete=_f(tot, "n:vFrete"),
    )
    soma = round(sum(i.valor_total for i in doc.itens), 2)
    if doc.totais.produtos is not None and abs(soma - doc.totais.produtos) > 0.01:
        doc.alertas.append(f"soma dos itens ({soma:.2f}) difere do total de produtos ({doc.totais.produtos:.2f})")
    doc.categoria = document_category(cats)
    return doc
