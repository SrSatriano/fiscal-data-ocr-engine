"""Dígitos verificadores de CNPJ, CPF e chave de acesso da NF-e (módulo 11)."""

from __future__ import annotations

import re

_DIGITS = re.compile(r"\D")


def only_digits(s: str) -> str:
    return _DIGITS.sub("", s or "")


def _mod11(digits: str, weights: list[int]) -> int:
    total = sum(int(d) * w for d, w in zip(digits, weights, strict=True))
    r = total % 11
    return 0 if r < 2 else 11 - r


def cnpj_valid(value: str) -> bool:
    d = only_digits(value)
    if len(d) != 14 or d == d[0] * 14:
        return False
    w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    w2 = [6] + w1
    return _mod11(d[:12], w1) == int(d[12]) and _mod11(d[:13], w2) == int(d[13])


def cpf_valid(value: str) -> bool:
    d = only_digits(value)
    if len(d) != 11 or d == d[0] * 11:
        return False
    dv1 = (sum(int(d[i]) * (10 - i) for i in range(9)) * 10) % 11 % 10
    dv2 = (sum(int(d[i]) * (11 - i) for i in range(10)) * 10) % 11 % 10
    return dv1 == int(d[9]) and dv2 == int(d[10])


def chave_dv(first43: str) -> int:
    """DV da chave de acesso: pesos 2..9 da direita para a esquerda."""
    weights = [2, 3, 4, 5, 6, 7, 8, 9]
    total = sum(int(c) * weights[i % 8] for i, c in enumerate(reversed(first43)))
    r = total % 11
    return 0 if r < 2 else 11 - r


def chave_valid(value: str) -> bool:
    d = only_digits(value)
    return len(d) == 44 and chave_dv(d[:43]) == int(d[43])


def parse_chave(value: str) -> dict:
    """Decompõe a chave: UF, AAMM, CNPJ, modelo (55 NF-e / 65 NFC-e), série, número."""
    d = only_digits(value)
    return {
        "uf": d[0:2],
        "ano_mes": f"20{d[2:4]}-{d[4:6]}",
        "cnpj_emitente": d[6:20],
        "modelo": d[20:22],
        "serie": int(d[22:25]),
        "numero": int(d[25:34]),
        "tipo_emissao": d[34],
    }
