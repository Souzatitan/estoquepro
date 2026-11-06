import pyodbc
from django.conf import settings
from django.core.cache import cache


SQL_BASE = """
SELECT
    SAL.PRODCODESTR AS COD_ESTRUTURAL,
    PROD.PRODCODALT AS COD_ALTERNATIVO,
    PROD.PRODNOME AS NOME_PRODUTO,
    SAL.SALDOESTQDATA AS DATA_ULT_ESTQ,
    SAL.SALDOESTQDATAQTD AS QNT_ESTOQUE,
    SAL.SALDOESTQDATAVAL AS VAL_ESTQ
FROM (
    SELECT
        SD.PRODCODESTR,
        SD.SALDOESTQDATA,
        SD.SALDOESTQDATAQTD,
        SD.SALDOESTQDATAVAL,
        DENSE_RANK() OVER (
            PARTITION BY SD.PRODCODESTR
            ORDER BY SD.SALDOESTQDATA DESC NULLS LAST
        ) AS RN_DATA
    FROM SALDO_ESTQ_DATA SD
) SAL
JOIN PRODUTO PROD
    ON PROD.PRODCODESTR = SAL.PRODCODESTR
WHERE SAL.RN_DATA = 1
"""

SQL_FILTRO = """
(
    UPPER(NVL(estoque.COD_ESTRUTURAL, ' ')) LIKE UPPER(?)
    OR UPPER(NVL(estoque.COD_ALTERNATIVO, ' ')) LIKE UPPER(?)
    OR UPPER(NVL(estoque.NOME_PRODUTO, ' ')) LIKE UPPER(?)
)
"""

COLUNAS = [
    "COD_ESTRUTURAL",
    "COD_ALTERNATIVO",
    "NOME_PRODUTO",
    "DATA_ULT_ESTQ",
    "QNT_ESTOQUE",
    "VAL_ESTQ",
]


def _conectar_oracle():
    """Abre uma conexão Oracle usando as configurações do Django."""
    if not settings.ORACLE_UID or not settings.ORACLE_PASSWORD:
        raise ValueError(
            "As credenciais Oracle não estão configuradas no .env."
        )

    return pyodbc.connect(
        f"DSN={settings.ORACLE_DSN};"
        f"UID={settings.ORACLE_UID};"
        f"PWD={settings.ORACLE_PASSWORD}",
        timeout=15,
        autocommit=False,
    )


def consultar_estoque(
    termo="",
    situacao="todos",
    pagina=1,
    por_pagina=25,
    exportar=False,
    ordenar="COD_ESTRUTURAL",
    direcao="asc",
):
    """Consulta o estoque com pesquisa, filtros, ordenação e paginação."""
    pagina = max(1, int(pagina))
    por_pagina = max(1, min(int(por_pagina), 100))

    # Colunas permitidas para ordenação.
    colunas_ordenacao = {
        "COD_ESTRUTURAL": "COD_ESTRUTURAL",
        "COD_ALTERNATIVO": "COD_ALTERNATIVO",
        "NOME_PRODUTO": "NOME_PRODUTO",
        "DATA_ULT_ESTQ": "DATA_ULT_ESTQ",
        "QNT_ESTOQUE": "QNT_ESTOQUE",
    }

    if ordenar not in colunas_ordenacao:
        ordenar = "COD_ESTRUTURAL"

    direcao_sql = "DESC" if direcao == "desc" else "ASC"
    coluna_sql = colunas_ordenacao[ordenar]

    ordem_sql = (
        f"estoque.{coluna_sql} {direcao_sql} NULLS LAST"
    )

    # Desempate para manter os resultados consistentes.
    if ordenar != "COD_ESTRUTURAL":
        ordem_sql += ", estoque.COD_ESTRUTURAL ASC NULLS LAST"

    condicoes = []
    parametros = []

    if termo:
        condicoes.append(SQL_FILTRO)
        busca = f"%{termo}%"
        parametros.extend([busca, busca, busca])

    filtros_situacao = {
        "todos": None,
        "zerado": "NVL(estoque.QNT_ESTOQUE, 0) = 0",
        "positivo": "estoque.QNT_ESTOQUE > 0",
        "negativo": "estoque.QNT_ESTOQUE < 0",
    }

    if situacao not in filtros_situacao:
        situacao = "todos"

    filtro_situacao = filtros_situacao[situacao]

    if filtro_situacao:
        condicoes.append(filtro_situacao)

    filtro_sql = ""

    if condicoes:
        filtro_sql = "WHERE " + " AND ".join(
            f"({condicao})" for condicao in condicoes
        )

    conexao = _conectar_oracle()

    try:
        cursor = conexao.cursor()

        try:
            sql_contagem = f"""
                SELECT COUNT(*)
                FROM ({SQL_BASE}) estoque
                {filtro_sql}
            """

            cursor.execute(sql_contagem, parametros)
            total = int(cursor.fetchone()[0] or 0)

            if exportar:
                sql_dados = f"""
                    SELECT {", ".join(COLUNAS)}
                    FROM ({SQL_BASE}) estoque
                    {filtro_sql}
                    ORDER BY {ordem_sql}
                """

                cursor.execute(sql_dados, parametros)

            else:
                inicio = (pagina - 1) * por_pagina + 1
                fim = pagina * por_pagina

                sql_dados = f"""
                    SELECT {", ".join(COLUNAS)}
                    FROM (
                        SELECT
                            {", ".join(
                                f"estoque.{coluna}"
                                for coluna in COLUNAS
                            )},
                            ROW_NUMBER() OVER (
                                ORDER BY {ordem_sql}
                            ) AS RN
                        FROM ({SQL_BASE}) estoque
                        {filtro_sql}
                    )
                    WHERE RN BETWEEN ? AND ?
                    ORDER BY RN
                """

                cursor.execute(
                    sql_dados,
                    parametros + [inicio, fim],
                )

            produtos = [
                dict(zip(COLUNAS, linha))
                for linha in cursor.fetchall()
            ]

            return {
                "total": total,
                "produtos": produtos,
            }

        finally:
            cursor.close()

    finally:
        conexao.close()


def consultar_indicadores():
    """Retorna indicadores resumidos do estoque, em cache por 60 segundos."""
    chave_cache = "indicadores_estoque_v1"
    indicadores = cache.get(chave_cache)

    if indicadores is not None:
        return indicadores

    sql = f"""
        SELECT
            COUNT(*) AS TOTAL_PRODUTOS,
            SUM(
                CASE
                    WHEN NVL(estoque.QNT_ESTOQUE, 0) = 0
                    THEN 1 ELSE 0
                END
            ) AS ESTOQUE_ZERO,
            SUM(
                CASE
                    WHEN estoque.QNT_ESTOQUE > 0
                    THEN 1 ELSE 0
                END
            ) AS ESTOQUE_POSITIVO,
            SUM(
                CASE
                    WHEN estoque.QNT_ESTOQUE < 0
                    THEN 1 ELSE 0
                END
            ) AS ESTOQUE_NEGATIVO,
            SUM(NVL(estoque.VAL_ESTQ, 0)) AS VALOR_TOTAL
        FROM ({SQL_BASE}) estoque
    """

    conexao = _conectar_oracle()

    try:
        cursor = conexao.cursor()

        try:
            cursor.execute(sql)
            linha = cursor.fetchone()

            indicadores = {
                "total_produtos": linha[0] or 0,
                "estoque_zero": linha[1] or 0,
                "estoque_positivo": linha[2] or 0,
                "estoque_negativo": linha[3] or 0,
                "valor_total": linha[4] or 0,
            }

        finally:
            cursor.close()

    finally:
        conexao.close()

    cache.set(chave_cache, indicadores, 60)
    return indicadores

def _usar_demonstracao():
    """Informa se a fonte selecionada é a demonstração."""
    return settings.FONTE_ESTOQUE == "demo"


def consultar_estoque_selecionado(*args, **kwargs):
    """Encaminha a consulta para a fonte configurada."""
    if _usar_demonstracao():
        from .demonstracao import consultar_estoque as consultar_demo
        return consultar_demo(*args, **kwargs)

    return consultar_estoque(*args, **kwargs)


def consultar_indicadores_selecionados():
    """Encaminha os indicadores para a fonte configurada."""
    if _usar_demonstracao():
        from .demonstracao import (
            consultar_indicadores as indicadores_demo,
        )
        return indicadores_demo()

    return consultar_indicadores()