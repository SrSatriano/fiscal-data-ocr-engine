import io

import pytest
from fastapi.testclient import TestClient

from fiscalocr.api import app
from fiscalocr.categorize import item_category
from fiscalocr.cli import main
from fiscalocr.engine import extract, extract_folder, summary, to_csv
from fiscalocr.validators import chave_dv, chave_valid, cnpj_valid, cpf_valid, parse_chave


def make_cnpj(base12: str) -> str:
    w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    def dv(ds, w):
        r = sum(int(d) * x for d, x in zip(ds, w, strict=True)) % 11
        return "0" if r < 2 else str(11 - r)

    d1 = dv(base12, w1)
    return base12 + d1 + dv(base12 + d1, [6] + w1)


EMIT = make_cnpj("112223330001")
DEST = make_cnpj("445556660001")


def make_chave(cnpj: str, numero: int = 1234, modelo: str = "55") -> str:
    first = f"35{'2611'}{cnpj}{modelo}001{numero:09d}1{'12345678'}"
    return first + str(chave_dv(first))


def nfe_xml(itens, total_prod=None, chave=None, emit=EMIT) -> bytes:
    chave = chave or make_chave(emit)
    dets = "".join(
        f"""<det nItem="{i + 1}"><prod><cProd>{i + 1}</cProd><xProd>{d}</xProd><NCM>{ncm}</NCM>
        <CFOP>5102</CFOP><qCom>{q}</qCom><vUnCom>{v}</vUnCom><vProd>{q * v:.2f}</vProd></prod></det>"""
        for i, (d, ncm, q, v) in enumerate(itens)
    )
    soma = total_prod if total_prod is not None else sum(q * v for _, _, q, v in itens)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00"><NFe><infNFe Id="NFe{chave}" versao="4.00">
<ide><mod>55</mod><serie>1</serie><nNF>1234</nNF><dhEmi>2026-11-10T10:30:00-03:00</dhEmi></ide>
<emit><CNPJ>{emit}</CNPJ><xNome>Fornecedor Exemplo LTDA</xNome></emit>
<dest><CNPJ>{DEST}</CNPJ><xNome>Cliente SA</xNome></dest>
{dets}
<total><ICMSTot><vProd>{soma:.2f}</vProd><vICMS>36.00</vICMS><vIPI>0.00</vIPI><vNF>{soma:.2f}</vNF></ICMSTot></total>
</infNFe></NFe></nfeProc>""".encode()


# ---------- validadores ----------
def test_cnpj_cpf_validation():
    assert cnpj_valid(EMIT) and cnpj_valid("11.222.333/0001-81")
    assert not cnpj_valid("11.222.333/0001-82") and not cnpj_valid("00000000000000")
    assert cpf_valid("529.982.247-25") and not cpf_valid("529.982.247-24") and not cpf_valid("111.111.111-11")


def test_chave_dv_and_parse():
    chave = make_chave(EMIT, numero=987, modelo="65")
    assert chave_valid(chave) and len(chave) == 44
    assert not chave_valid(chave[:-1] + str((int(chave[-1]) + 1) % 10))
    info = parse_chave(chave)
    assert info["cnpj_emitente"] == EMIT and info["modelo"] == "65" and info["numero"] == 987


# ---------- XML ----------
def test_parse_nfe_xml_full():
    doc = extract(
        nfe_xml([("Notebook 14 polegadas", "84713012", 2, 3500.0), ("Papel A4 500 folhas", "48025610", 10, 29.9)]),
        "n.xml",
    )
    assert doc.origem == "xml" and doc.chave_valida and doc.confianca == 1.0
    assert doc.emitente_cnpj == EMIT and doc.destinatario_doc == DEST
    assert doc.data_emissao == "2026-11-10" and doc.numero == 1234
    assert [i.categoria for i in doc.itens] == ["informatica", "material_escritorio"]
    assert doc.categoria == "informatica"  # concentra mais valor
    assert doc.totais.nota == 7299.0 and doc.totais.icms == 36.0
    assert doc.alertas == []


def test_xml_inconsistencies_become_alerts():
    bad_chave = make_chave(EMIT)[:-1] + "9"
    if chave_valid(bad_chave):
        bad_chave = make_chave(EMIT)[:-1] + "8"
    doc = extract(nfe_xml([("Gasolina comum", "27101259", 40, 6.0)], total_prod=999.0, chave=bad_chave), "x.xml")
    assert doc.categoria == "combustivel"
    assert any("chave" in a for a in doc.alertas)
    assert any("soma dos itens" in a for a in doc.alertas)


def test_xml_rejects_entities():
    with pytest.raises(ValueError):
        extract(b'<?xml version="1.0"?><!DOCTYPE x [<!ENTITY a "b">]><x>&a;</x>', "evil.xml")


# ---------- texto / PDF ----------
TEXTO = f"""NOTA FISCAL DE SERVIÇO ELETRÔNICA
Prestador CNPJ: {EMIT[:2]}.{EMIT[2:5]}.{EMIT[5:8]}/{EMIT[8:12]}-{EMIT[12:]}
Tomador CNPJ: 11.222.333/0001-82
Emissão: 05/11/2026
Descrição: Licença de software SaaS - hospedagem cloud
Valor do ICMS: R$ 0,00
VALOR TOTAL DA NOTA: R$ 2.450,00
"""


def test_text_extraction_validates_and_flags_ocr_noise():
    doc = extract(TEXTO.encode("utf-8"), "servico.txt")
    assert doc.emitente_cnpj == EMIT
    assert doc.destinatario_doc is None  # o segundo CNPJ tem DV inválido e é descartado
    assert any("dígito verificador" in a for a in doc.alertas)
    assert doc.totais.nota == 2450.0 and doc.data_emissao == "2026-11-05"
    assert doc.categoria == "servicos_ti"
    assert doc.confianca >= 0.6


def test_danfe_text_reads_chave_with_spaces():
    chave = make_chave(EMIT, numero=55)
    spaced = " ".join(chave[i : i + 4] for i in range(0, 44, 4))
    doc = extract(f"DANFE\nCHAVE DE ACESSO\n{spaced}\nVALOR TOTAL DA NOTA 1.000,00".encode(), "danfe.txt")
    assert doc.chave == chave and doc.numero == 55 and doc.totais.nota == 1000.0


def test_pdf_extraction():
    pytest.importorskip("reportlab")
    from reportlab.pdfgen import canvas

    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    for i, line in enumerate(TEXTO.splitlines()):
        c.drawString(40, 800 - 16 * i, line)
    c.save()
    doc = extract(buf.getvalue(), "nota.pdf")
    assert doc.origem == "pdf" and doc.totais.nota == 2450.0 and doc.emitente_cnpj == EMIT


def test_cfop_service_and_keywords():
    assert item_category("Assinatura software de gestão", None, "5933") == "servicos_ti"
    assert item_category("Refeição executiva", None, "5102") == "alimentacao"
    assert item_category("Item genérico", None, None) == "outros"


# ---------- lote, CSV, CLI e API ----------
def test_folder_csv_and_summary(tmp_path, capsys):
    (tmp_path / "a.xml").write_bytes(nfe_xml([("Diesel S10", "27101921", 100, 5.8)]))
    (tmp_path / "b.txt").write_text(TEXTO, encoding="utf-8")
    (tmp_path / "c.xml").write_text("isto não é xml", encoding="utf-8")
    docs = extract_folder(tmp_path)
    assert len(docs) == 3 and docs[2].origem == "erro"
    s = summary(docs)
    assert s["por_categoria"]["combustivel"] == 580.0 and s["total"] == 3030.0
    csv_text = to_csv(docs)
    assert csv_text.splitlines()[0].startswith("arquivo;origem")
    assert main(["extract", str(tmp_path), "--csv", str(tmp_path / "out.csv")]) == 0
    assert (tmp_path / "out.csv").exists() and "combustivel" in capsys.readouterr().out


def test_api():
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}
    r = client.post(
        "/extract", files={"file": ("n.xml", nfe_xml([("Mouse óptico", "84716053", 3, 50.0)]), "application/xml")}
    )
    assert r.status_code == 200 and r.json()["categoria"] == "informatica"
    r = client.post("/extract", files={"file": ("bad.xml", b"<?xml version='1.0'?><a/>", "application/xml")})
    assert r.status_code == 422
