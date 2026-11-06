import os
import sys
import json
import random
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

BASE_BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_BACKEND))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from gestao_materiais.services.oracle import (
    COLUNAS,
    SQL_BASE,
    _conectar_oracle,
)


QUANTIDADE = 100
SEMENTE = 42  # Seleção reproduzível para facilitar a demonstração


def serializar(valor):
    if isinstance(valor, (datetime, date)):
        return valor.isoformat()
    if isinstance(valor, Decimal):
        return float(valor)
    return valor


def main():
    conexao = _conectar_oracle()

    try:
        cursor = conexao.cursor()
        try:
            cursor.execute(
                f"""
                SELECT {", ".join(COLUNAS)}
                FROM ({SQL_BASE}) estoque
                ORDER BY DBMS_RANDOM.VALUE
                FETCH FIRST {QUANTIDADE} ROWS ONLY
                """
            )

            registros = [
                dict(zip(COLUNAS, linha))
                for linha in cursor.fetchall()
            ]
        finally:
            cursor.close()
    finally:
        conexao.close()

    if len(registros) < QUANTIDADE:
        raise RuntimeError(
            f"O Oracle retornou apenas {len(registros)} produtos; "
            f"eram esperados {QUANTIDADE}."
        )

    # Converte tipos Oracle para valores aceitos pelo JSON.
    registros = [
        {campo: serializar(valor) for campo, valor in produto.items()}
        for produto in registros
    ]

    destino = (
        Path(__file__).resolve().parents[1]
        / "gestao_materiais"
        / "dados"
        / "estoque_oracle_local.json"
    )

    destino.parent.mkdir(parents=True, exist_ok=True)

    with destino.open("w", encoding="utf-8") as arquivo:
        json.dump(
            registros,
            arquivo,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Arquivo gerado: {destino}")
    print(f"Produtos exportados: {len(registros)}")


if __name__ == "__main__":
    main()
