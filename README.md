# 📦 Sistema de Controle de Estoque

**Projeto Integrador — Engenharia da Computação | UNIVESP**

Aplicação web para consulta e análise de saldos de estoque, desenvolvida com Python e Django, com integração opcional ao Oracle e modo de demonstração com dados sintéticos em JSON.

---

## 📑 Sumário

- [🎯 Objetivo](#-objetivo)
- [✨ Funcionalidades](#-funcionalidades)
- [🛠️ Tecnologias e requisitos](#️-tecnologias-e-requisitos)
- [📥 Instalação do projeto](#-instalação-do-projeto)
- [⚙️ Configuração do ambiente](#️-configuração-do-ambiente)
- [▶️ Como executar](#️-como-executar)
- [🧪 Testes](#-testes)
- [🗄️ Fontes de dados](#️-fontes-de-dados)
- [🔌 Integração com Oracle](#-integração-com-oracle)
- [📁 Estrutura do projeto](#-estrutura-do-projeto)
- [🤝 Trabalho em equipe com Git](#-trabalho-em-equipe-com-git)
- [🛡️ Segurança](#️-segurança)
- [❓ Solução de problemas](#-solução-de-problemas)

---

## 🎯 Objetivo

Desenvolver uma aplicação web para facilitar a consulta, a visualização e a análise de informações de estoque, aplicando conhecimentos de desenvolvimento de software, integração com banco de dados, construção de interfaces web, testes e controle de versão.

O sistema foi desenvolvido como parte do Projeto Integrador do curso de Engenharia da Computação da Universidade Virtual do Estado de São Paulo (UNIVESP).

## ✨ Funcionalidades

- 🔎 Pesquisa de produtos.
- 📊 Consulta de saldos de estoque.
- 🏷️ Filtros por situação do estoque.
- ↕️ Ordenação dos resultados.
- 📄 Paginação dos registros.
- 📈 Indicadores de estoque.
- 📤 Exportação de dados para CSV.
- 🧪 Modo de demonstração com dados sintéticos em JSON.
- 🗄️ Integração opcional com Oracle, mediante autorização e configuração do ambiente.

## 🛠️ Tecnologias e requisitos

| Tecnologia | Versão ou requisito |
|---|---|
| Sistema operacional | Windows 10 ou 11 |
| Python | 3.12.x recomendado |
| Django | 5.2.x |
| pyodbc | 5.2 ou superior, abaixo da versão 6 |
| python-dotenv | 1.x |
| Oracle | Opcional; requer acesso autorizado |
| Git | Versão compatível com o sistema operacional |
| Navegador | Chrome, Edge, Firefox ou equivalente |
| Editor recomendado | Visual Studio Code |

### 📥 Programas necessários

Instale os programas abaixo, caso ainda não estejam disponíveis no computador:

- **Python:** https://www.python.org/downloads/
- **Git:** https://git-scm.com/downloads
- **Visual Studio Code:** https://code.visualstudio.com/

Durante a instalação do Python no Windows, recomenda-se habilitar a opção **Add Python to PATH**.

## 📥 Instalação do projeto

### 1. Clonar o repositório

Abra o PowerShell e execute:

```powershell
git clone https://github.com/rafabrunini/sistema_controle_estoque.git
```

Entre na pasta do projeto:

```powershell
cd sistema_controle_estoque
```

Se o projeto já estiver clonado no computador, entre na pasta existente e atualize os arquivos:

```powershell
git pull origin main
```

### 2. Criar o ambiente virtual

Na pasta raiz do projeto, execute:

```powershell
py -3.12 -m venv .venv
```

Se o comando `py -3.12` não funcionar, verifique se o Python 3.12 está instalado corretamente.

### 3. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação do ambiente virtual, utilize diretamente o executável Python da pasta `.venv`, conforme os exemplos das próximas seções.

### 4. Instalar as dependências

Com o ambiente virtual ativado:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

As dependências também podem ser instaladas sem ativar o ambiente virtual:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## ⚙️ Configuração do ambiente

O projeto utiliza variáveis de ambiente para configurar a execução local.

### 1. Criar o arquivo `.env`

Na pasta raiz do repositório, crie um arquivo chamado `.env`.

Uma maneira de abrir o arquivo no VS Code é:

```powershell
code .env
```

Caso ele ainda não exista, o VS Code permitirá criá-lo.

### 2. Gerar uma chave local do Django

Cada integrante deve gerar sua própria chave secreta. Não utilize nem compartilhe a chave secreta de outro integrante.

Execute no PowerShell:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Copie o resultado diretamente para o arquivo `.env`, sem publicá-lo no GitHub.

### 3. Configurar o modo de demonstração

O arquivo `.env` deve conter, no mínimo, as configurações abaixo:

```dotenv
SECRET_KEY=COLOQUE_AQUI_SUA_CHAVE_GERADA_LOCALMENTE
FONTE_ESTOQUE=demo
ESTOQUE_DEMO_ARQUIVO=estoque_demo.json
```

Substitua `COLOQUE_AQUI_SUA_CHAVE_GERADA_LOCALMENTE` pela chave gerada no passo anterior.

**Importante:** o arquivo `.env` é individual e não deve ser enviado ao repositório.

O projeto utiliza o modo `demo` por padrão quando a fonte de dados não é configurada de outra forma.

## ▶️ Como executar

### 1. Preparar o banco de dados local do Django

Na pasta raiz do projeto, execute:

```powershell
.\.venv\Scripts\python.exe .\backend\manage.py migrate
```

### 2. Verificar a configuração

```powershell
.\.venv\Scripts\python.exe .\backend\manage.py check
```

O resultado esperado é uma mensagem indicando que não foram identificados problemas.

### 3. Iniciar o servidor

```powershell
.\.venv\Scripts\python.exe .\backend\manage.py runserver
```

### 4. Acessar o sistema

Abra o navegador e acesse:

**http://127.0.0.1:8000/**

Para encerrar o servidor, volte ao terminal e pressione `Ctrl + C`.

## 🧪 Testes

O projeto possui testes automatizados para verificar funcionalidades da aplicação.

Para executar os testes:

```powershell
.\.venv\Scripts\python.exe .\backend\manage.py test gestao_materiais
```

Para verificar novamente a configuração do Django:

```powershell
.\.venv\Scripts\python.exe .\backend\manage.py check
```

Execute os testes depois de realizar alterações no código para verificar se as funcionalidades continuam funcionando corretamente.

## 🗄️ Fontes de dados

O sistema foi preparado para trabalhar com duas fontes de dados.

### 🧪 Modo de demonstração

O modo de demonstração utiliza dados sintéticos armazenados em um arquivo JSON:

```text
backend/gestao_materiais/dados/estoque_demo.json
```

Essa é a opção recomendada para instalação inicial, apresentações acadêmicas e desenvolvimento em equipe.

Os registros de demonstração não representam necessariamente o estoque real da empresa.

**Vantagens:**

- Não exige conexão com o Oracle.
- Não depende de credenciais corporativas.
- Permite que todos os integrantes executem o projeto localmente.
- Evita a exposição de informações empresariais.
- Facilita testes e demonstrações acadêmicas.

### 🗄️ Modo Oracle

A integração com Oracle é opcional e depende de autorização, instalação do driver necessário e configuração das credenciais no ambiente local.

A conexão deve ser utilizada somente para as consultas autorizadas, respeitando as regras de segurança e acesso ao ERP.

## 🔌 Integração com Oracle

Para utilizar o Oracle, o integrante precisa ter:

- Autorização para acessar o banco de dados.
- Oracle Client ou driver ODBC compatível, conforme a configuração adotada.
- Fonte de dados configurada no ambiente local.
- Credenciais individuais autorizadas.
- Permissões suficientes para executar as consultas necessárias.

O arquivo `.env` pode receber as configurações de conexão, conforme os nomes utilizados pelo projeto:

```dotenv
FONTE_ESTOQUE=oracle
ORACLE_DSN=IBPRD
ORACLE_UID=SEU_USUARIO_AUTORIZADO
ORACLE_PWD=SUA_SENHA_LOCAL
```

Os valores acima são exemplos de configuração. Utilize somente as variáveis efetivamente reconhecidas pela implementação e as informações fornecidas pelo responsável pelo ambiente.

**Atenção:** não utilize essas configurações sem autorização do responsável pelo banco de dados. A configuração Oracle não é necessária para executar o modo de demonstração.

## 📁 Estrutura do projeto

A estrutura principal do repositório é organizada da seguinte forma:

```text
sistema_controle_estoque/
│
├── backend/
│   ├── config/
│   │   └── settings.py
│   │
│   ├── gestao_materiais/
│   │   ├── dados/
│   │   │   └── estoque_demo.json
│   │   ├── services/
│   │   │   └── oracle.py
│   │   ├── templates/
│   │   │   └── gestao_materiais/
│   │   │       └── lista_estoque.html
│   │   └── ...
│   │
│   ├── scripts/
│   └── manage.py
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── .venv/
```

A estrutura acima é ilustrativa: alguns arquivos e diretórios podem variar conforme a versão do projeto.

O ambiente virtual `.venv/` e o arquivo `.env` são locais e não devem ser compartilhados pelo Git.

O arquivo `estoque_oracle_local.json`, quando utilizado para testes autorizados, também deve permanecer fora do repositório.

## 🤝 Trabalho em equipe com Git

Para facilitar a colaboração, cada integrante deve desenvolver e testar suas alterações localmente, utilizando o GitHub para compartilhar somente os arquivos autorizados.

### 1. Atualizar a versão local

Antes de começar a trabalhar:

```powershell
git pull origin main
```

### 2. Criar uma branch para a tarefa

Utilize uma branch específica para cada funcionalidade:

```powershell
git switch -c feature/nome-da-funcionalidade
```

Substitua `nome-da-funcionalidade` por um nome curto que descreva a tarefa.

### 3. Verificar as alterações

```powershell
git status
git diff
```

### 4. Adicionar e registrar as alterações

```powershell
git add .
git diff --cached --check
git commit -m "Descreve a alteração realizada"
```

Antes de executar `git add .`, confira se não há arquivos locais, credenciais ou dados empresariais que não devam ser enviados.

### 5. Enviar a branch ao GitHub

```powershell
git push -u origin feature/nome-da-funcionalidade
```

Depois, abra um Pull Request no GitHub para revisar e integrar as alterações à branch `main`.

### Boas práticas de colaboração

- Cada integrante deve trabalhar em sua própria branch.
- Atualize a branch antes de iniciar uma nova tarefa.
- Execute os testes antes de enviar as alterações.
- Utilize mensagens de commit claras.
- Revise as alterações antes de abrir um Pull Request.
- Não envie arquivos locais de configuração ou dados confidenciais.
- Evite trabalhar diretamente na `main` quando a equipe estiver utilizando revisão por Pull Request.

## 🛡️ Segurança

A segurança das informações deve ser considerada durante todo o desenvolvimento.

- Nunca publique senhas, tokens ou chaves secretas.
- Não envie o arquivo `.env` ao GitHub.
- Não compartilhe credenciais corporativas entre integrantes.
- Não publique dados reais de estoque, arquivos extraídos do ERP ou informações empresariais sem autorização expressa.
- Mantenha arquivos locais com dados reais excluídos do controle de versão.
- Utilize somente acessos autorizados ao banco Oracle.
- Prefira o modo de demonstração para apresentações e testes acadêmicos.
- Verifique o conteúdo dos arquivos antes de realizar commits e pushes.

O arquivo `.gitignore` deve proteger arquivos locais e confidenciais, mas essa proteção não substitui a revisão do que será enviado ao repositório.

## ❓ Solução de problemas

### Erro: Python não encontrado

Verifique a instalação:

```powershell
py --version
```

Se necessário, instale o Python 3.12 e recrie o ambiente virtual.

### Erro: dependências não instaladas

Execute:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Erro ao acessar a página

Verifique se o servidor está em execução e se o terminal apresenta erros.

Acesse:

```text
http://127.0.0.1:8000/
```

### Erro ao carregar os dados

Confirme se o arquivo de demonstração existe em:

```text
backend/gestao_materiais/dados/estoque_demo.json
```

Verifique também se o arquivo `.env` contém:

```dotenv
FONTE_ESTOQUE=demo
ESTOQUE_DEMO_ARQUIVO=estoque_demo.json
```

Depois, reinicie o servidor.

### Erro de conexão com Oracle

Confirme a autorização de acesso, o driver instalado, o DSN e as credenciais locais.

Se o objetivo for apenas testar a aplicação, volte ao modo de demonstração, que não depende da conexão com Oracle.

---

## 👥 Equipe e desenvolvimento acadêmico

Projeto desenvolvido no âmbito do **Projeto Integrador do curso de Engenharia da Computação da UNIVESP**.

A colaboração é realizada por meio de desenvolvimento local, versionamento com Git e compartilhamento de código no GitHub.

---

**Sistema de Controle de Estoque — UNIVESP**

*Desenvolvimento de software, consulta de dados e integração com banco de dados.*
