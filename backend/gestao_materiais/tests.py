from decimal import Decimal

from django.test import TestCase, override_settings

from .services import demonstracao


@override_settings(
    FONTE_ESTOQUE="demo",
    ESTOQUE_DEMO_ARQUIVO="estoque_demo.json",
)
class DemonstracaoTests(TestCase):
    """Testes do serviço de estoque em modo de demonstração."""

    def setUp(self):
        demonstracao._carregar_produtos.cache_clear()

    def tearDown(self):
        demonstracao._carregar_produtos.cache_clear()

    def test_carrega_os_cem_produtos_de_demonstracao(self):
        produtos = demonstracao._carregar_produtos()

        self.assertEqual(len(produtos), 100)
        self.assertTrue(all(isinstance(p, dict) for p in produtos))

    def test_pesquisa_por_nome(self):
        todos = demonstracao.consultar_estoque(exportar=True)
        nome = todos["produtos"][0]["NOME_PRODUTO"]

        resultado = demonstracao.consultar_estoque(termo=nome)

        self.assertGreater(resultado["total"], 0)
        self.assertTrue(
            any(
                p["NOME_PRODUTO"] == nome
                for p in resultado["produtos"]
            )
        )

    def test_filtros_de_situacao_do_estoque(self):
        todos = demonstracao.consultar_estoque(
            exportar=True,
            situacao="todos",
        )

        zerados = demonstracao.consultar_estoque(
            exportar=True,
            situacao="zerado",
        )

        positivos = demonstracao.consultar_estoque(
            exportar=True,
            situacao="positivo",
        )

        negativos = demonstracao.consultar_estoque(
            exportar=True,
            situacao="negativo",
        )

        quantidade = lambda p: Decimal(str(p["QNT_ESTOQUE"] or 0))

        self.assertTrue(all(quantidade(p) == 0 for p in zerados["produtos"]))
        self.assertTrue(all(quantidade(p) > 0 for p in positivos["produtos"]))
        self.assertTrue(all(quantidade(p) < 0 for p in negativos["produtos"]))

        self.assertEqual(
            todos["total"],
            zerados["total"] + positivos["total"] + negativos["total"],
        )

    def test_ordenacao_por_codigo_estrutural(self):
        resultado = demonstracao.consultar_estoque(
            exportar=True,
            ordenar="COD_ESTRUTURAL",
            direcao="asc",
        )

        codigos = [
            p["COD_ESTRUTURAL"].casefold()
            for p in resultado["produtos"]
        ]

        self.assertEqual(codigos, sorted(codigos))

    def test_paginacao_retorna_os_itens_corretos(self):
        todos = demonstracao.consultar_estoque(
            exportar=True,
            ordenar="COD_ESTRUTURAL",
            direcao="asc",
        )

        segunda_pagina = demonstracao.consultar_estoque(
            pagina=2,
            por_pagina=3,
            ordenar="COD_ESTRUTURAL",
            direcao="asc",
        )

        self.assertEqual(
            segunda_pagina["produtos"],
            todos["produtos"][3:6],
        )
        self.assertEqual(segunda_pagina["total"], todos["total"])

    def test_exportacao_do_servico_inclui_todos_os_produtos(self):
        resultado = demonstracao.consultar_estoque(
            pagina=2,
            por_pagina=3,
            exportar=True,
        )

        self.assertEqual(resultado["total"], 100)
        self.assertEqual(len(resultado["produtos"]), 100)

    def test_indicadores_sao_consistentes(self):
        indicadores = demonstracao.consultar_indicadores()
        produtos = demonstracao._carregar_produtos()

        self.assertEqual(indicadores["total_produtos"], len(produtos))

        self.assertEqual(
            indicadores["estoque_zero"]
            + indicadores["estoque_positivo"]
            + indicadores["estoque_negativo"],
            len(produtos),
        )

        valor_esperado = sum(
            (Decimal(str(p["VAL_ESTQ"] or 0)) for p in produtos),
            Decimal("0"),
        )

        self.assertEqual(indicadores["valor_total"], valor_esperado)

    def test_pagina_inicial_e_exportacao_csv(self):
        pagina = self.client.get("/")
        csv_response = self.client.get("/exportar/csv/")

        self.assertEqual(pagina.status_code, 200)
        self.assertEqual(csv_response.status_code, 200)
        self.assertIn("text/csv", csv_response["Content-Type"])

        linhas = csv_response.content.decode("utf-8-sig").splitlines()

        total_produtos = demonstracao.consultar_estoque(
            exportar=True
        )["total"]

        self.assertEqual(len(linhas), total_produtos + 1)