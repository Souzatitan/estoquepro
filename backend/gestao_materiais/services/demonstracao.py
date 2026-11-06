import json
from datetime import date
from decimal import Decimal
from functools import lru_cache

from django.conf import settings


COLUNAS_ORDENACAO = {
    "COD_ESTRUTURAL": "COD_ESTRUTURAL",
    "COD_ALTERNATIVO": "COD_ALTERNATIVO",
    "NOME_PRODUTO": "NOME_PRODUTO",
    "DATA_ULT_ESTQ": "DATA_ULT_ESTQ",
    "QNT_ESTOQUE": "QNT_ESTOQUE",
}


@lru_cache(maxsize=1)
def _carregar_produtos():
    """Carrega os produtos do arquivo JSON configurado."""
    nome_arquivo = getattr(
        settings,
        "ESTOQUE_DEMO_ARQUIVO",
        "estoque_demo.json",
    )

    # Aceita somente um nome de arquivo, sem caminhos externos.
    if nome_arquivo not in {
        "estoque_demo.json",
        "estoque_oracle_local.json",
    }:
        raise ValueError("Arquivo de demonstração não permitido.")

    caminho = (
        settings.BASE_DIR
        / "gestao_materiais"
        / "dados"
        / nome_arquivo
    )

    with caminho.open("r", encoding="utf-8") as arquivo:
        produtos = json.load(arquivo)

    if not isinstance(produtos, list):
        raise ValueError("O arquivo JSON deve conter uma lista de produtos.")

    campos_obrigatorios = {
        "COD_ESTRUTURAL",
        "COD_ALTERNATIVO",
        "NOME_PRODUTO",
        "DATA_ULT_ESTQ",
        "QNT_ESTOQUE",
        "VAL_ESTQ",
    }

    for produto in produtos:
        if not isinstance(produto, dict):
            raise ValueError("Cada registro do JSON deve ser um objeto.")

        faltantes = campos_obrigatorios - produto.keys()
        if faltantes:
            raise ValueError(
                f"Registro sem campos obrigatórios: {sorted(faltantes)}"
            )

    return produtos


def _data_ordenacao(valor):
    if not valor:
        return date.min

    if isinstance(valor, date):
        return valor

    try:
        return date.fromisoformat(str(valor)[:10])
    except ValueError:
        return date.min


def consultar_estoque(
    termo="",
    situacao="todos",
    pagina=1,
    por_pagina=25,
    exportar=False,
    ordenar="COD_ESTRUTURAL",
    direcao="asc",
):
    """Pesquisa, filtra, ordena e pagina os dados fictícios."""
    pagina = max(1, int(pagina))
    por_pagina = max(1, min(int(por_pagina), 100))

    if ordenar not in COLUNAS_ORDENACAO:
        ordenar = "COD_ESTRUTURAL"

    if situacao not in {"todos", "zerado", "positivo", "negativo"}:
        situacao = "todos"

    produtos = list(_carregar_produtos())
    termo = termo.strip().casefold()

    if termo:
        produtos = [
            produto
            for produto in produtos
            if any(
                termo in str(produto.get(campo) or "").casefold()
                for campo in (
                    "COD_ESTRUTURAL",
                    "COD_ALTERNATIVO",
                    "NOME_PRODUTO",
                )
            )
        ]

    if situacao == "zerado":
        produtos = [
            p for p in produtos
            if Decimal(str(p.get("QNT_ESTOQUE") or 0)) == 0
        ]
    elif situacao == "positivo":
        produtos = [
            p for p in produtos
            if Decimal(str(p.get("QNT_ESTOQUE") or 0)) > 0
        ]
    elif situacao == "negativo":
        produtos = [
            p for p in produtos
            if Decimal(str(p.get("QNT_ESTOQUE") or 0)) < 0
        ]

    def chave(produto):
        valor = produto.get(ordenar)

        if ordenar == "QNT_ESTOQUE":
            return Decimal(str(valor or 0))
        if ordenar == "DATA_ULT_ESTQ":
            return _data_ordenacao(valor)
        if ordenar == "VAL_ESTQ":
            return Decimal(str(valor or 0))

        return str(valor or "").casefold()

    # Mantém o código estrutural como critério de desempate.
    produtos.sort(
        key=lambda p: str(p.get("COD_ESTRUTURAL") or "")
    )
    produtos.sort(
        key=chave,
        reverse=(direcao == "desc"),
    )

    total = len(produtos)

    if not exportar:
        inicio = (pagina - 1) * por_pagina
        produtos = produtos[inicio:inicio + por_pagina]

    return {
        "total": total,
        "produtos": produtos,
    }


def consultar_indicadores():
    """Calcula os indicadores com base nos registros fictícios."""
    produtos = _carregar_produtos()

    quantidades = [
        Decimal(str(p.get("QNT_ESTOQUE") or 0))
        for p in produtos
    ]

    valores = [
        Decimal(str(p.get("VAL_ESTQ") or 0))
        for p in produtos
    ]

    return {
        "total_produtos": len(produtos),
        "estoque_zero": sum(q == 0 for q in quantidades),
        "estoque_positivo": sum(q > 0 for q in quantidades),
        "estoque_negativo": sum(q < 0 for q in quantidades),
        "valor_total": sum(valores, Decimal("0")),
    }