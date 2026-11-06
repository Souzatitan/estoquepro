import getpass
import pyodbc

SQL_ESTOQUE = """
SELECT
    SAL.PRODCODESTR AS COD_ESTRUTURAL,
    PROD.PRODCODALT AS COD_ALTERNATIVO,
    PROD.PRODNOME AS NOME_PRODUTO,
    SAL.SALDOESTQDATA AS DATA_ULT_ESTQ,
    SAL.SALDOESTQDATAQTD AS QNT_ESTOQUE,
    SAL.SALDOESTQDATAVAL AS VAL_ESTQ
FROM SALDO_ESTQ_DATA SAL
JOIN PRODUTO PROD
    ON PROD.PRODCODESTR = SAL.PRODCODESTR
WHERE SAL.ROWID IN (
    SELECT SAL2.ROWID
    FROM SALDO_ESTQ_DATA SAL2
    WHERE SAL2.SALDOESTQDATA = (
        SELECT MAX(SAL3.SALDOESTQDATA)
        FROM SALDO_ESTQ_DATA SAL3
        WHERE SAL3.PRODCODESTR = SAL2.PRODCODESTR
    )
)
ORDER BY SAL.PRODCODESTR ASC
"""

usuario = input("Usuário Oracle: ")
senha = getpass.getpass("Senha Oracle: ")

conexao = None
cursor = None

try:
    conexao = pyodbc.connect(
        f"DSN=IBPRD;UID={usuario};PWD={senha}",
        timeout=15,
        autocommit=False,
    )

    cursor = conexao.cursor()
    cursor.execute(SQL_ESTOQUE)

    colunas = [coluna[0] for coluna in cursor.description]
    amostra = cursor.fetchmany(5)

    print("\nConsulta executada com sucesso.")
    print("Colunas retornadas:", ", ".join(colunas))
    print(f"Registros recebidos na amostra: {len(amostra)}")
    print("Dados dos produtos omitidos por segurança.")

except pyodbc.Error as erro:
    print("\nErro ao executar a consulta Oracle.")
    print("Confira as permissões e os nomes das tabelas e colunas.")
    print(f"Detalhes técnicos: {erro}")

finally:
    if cursor is not None:
        cursor.close()
    if conexao is not None:
        conexao.close()