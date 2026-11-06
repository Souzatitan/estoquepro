import csv
from math import ceil
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .services.oracle import (
    consultar_estoque_selecionado as consultar_estoque,
    consultar_indicadores_selecionados as consultar_indicadores,
)
@login_required
def dashboard(request):
    try:
        indicadores = consultar_indicadores()
        erro = None

    except Exception:
        indicadores = None
        erro = (
            "Não foi possível carregar os indicadores. "
            "Verifique a conexão e as configurações."
        )

    contexto = {
        "indicadores": indicadores,
        "erro": erro,
    }

    return render(
        request,
        "gestao_materiais/dashboard.html",
        contexto,
    )
@login_required
def lista_estoque(request):
    termo = request.GET.get("q", "").strip()

    situacoes_validas = {"todos", "zerado", "positivo", "negativo"}
    situacao = request.GET.get("situacao", "todos")

    if situacao not in situacoes_validas:
        situacao = "todos"

    try:
        pagina = int(request.GET.get("page", "1"))
    except (TypeError, ValueError):
        pagina = 1

    pagina = max(1, pagina)
    por_pagina = 25

    try:
        indicadores = consultar_indicadores()

        resultado = consultar_estoque(
            termo=termo,
            situacao=situacao,
            pagina=pagina,
            por_pagina=por_pagina,
        )

        total = resultado["total"]
        total_paginas = max(1, ceil(total / por_pagina))

        if pagina > total_paginas:
            pagina = total_paginas
            resultado = consultar_estoque(
                termo=termo,
                situacao=situacao,
                pagina=pagina,
                por_pagina=por_pagina,
            )
            total = resultado["total"]
            total_paginas = max(1, ceil(total / por_pagina))

        contexto = {
            "produtos": resultado["produtos"],
            "termo": termo,
            "situacao": situacao,
            "total": total,
            "pagina_atual": pagina,
            "total_paginas": total_paginas,
            "tem_anterior": pagina > 1,
            "tem_proxima": pagina < total_paginas,
            "erro": None,
            "indicadores": indicadores,
        }

    except Exception:
        contexto = {
            "produtos": [],
            "termo": termo,
            "situacao": situacao,
            "total": 0,
            "pagina_atual": 1,
            "total_paginas": 1,
            "tem_anterior": False,
            "tem_proxima": False,
            "indicadores": None,
            "erro": (
                "Não foi possível consultar o estoque. "
                "Verifique a conexão e as configurações."
            ),
        }

    return render(
        request,
        "gestao_materiais/lista_estoque.html",
        contexto,
    )

@login_required
def exportar_estoque_csv(request):
    termo = request.GET.get("q", "").strip()

    situacoes_validas = {"todos", "zerado", "positivo", "negativo"}
    situacao = request.GET.get("situacao", "todos")

    if situacao not in situacoes_validas:
        situacao = "todos"

    try:
        resultado = consultar_estoque(
            termo=termo,
            situacao=situacao,
            exportar=True,
        )
    except Exception:
        return HttpResponse(
            "Não foi possível exportar o estoque. "
            "Verifique a conexão com o Oracle.",
            status=503,
            content_type="text/plain; charset=utf-8",
        )

    resposta = HttpResponse(
        content_type="text/csv; charset=utf-8",
    )
    resposta.write("\ufeff")
    resposta["Content-Disposition"] = (
        'attachment; filename="estoque.csv"'
    )

    gravador = csv.writer(resposta, delimiter=";")

    gravador.writerow([
        "Código estrutural",
        "Código alternativo",
        "Produto",
        "Data do último estoque",
        "Quantidade em estoque",
    ])

    for produto in resultado["produtos"]:
        gravador.writerow([
            produto.get("COD_ESTRUTURAL"),
            produto.get("COD_ALTERNATIVO"),
            produto.get("NOME_PRODUTO"),
            produto.get("DATA_ULT_ESTQ"),
            produto.get("QNT_ESTOQUE"),
        ])

    return resposta