# Rede Universitas

Rede Universitas trata-se de uma solução de software para o gerenciamento e acompanhamento de uma rede privada de universidades multi-campi, contando com: lançamento de notas, criação de bolsas, gerenciamento de estoque e compras, geração automática de mensalidades, controle e visualização de fluxo de caixa, visualização de dashboards, etc.


## Equipe

- Arthur de Sá Tenório
- Guilherme Paes Cavalcanti
- Victor Cauã Tavares Inácio


## Requisitos de Software

Antes de executar o projeto, certifique-se de possuir instalado:

| Software | Versão |
|----------|---------|
| Python | **3.14.3** ou superior |
| pip | **25.3** ou superior |
| PostgreSQL | **17** ou superior |


## Como executar o projeto?

### Criação de ambiente virtual

```bash
# Linux / macOS
python -m venv .venv
source .venv/bin/activate
```

```powershell
# Windows
python -m venv .venv
.venv\Scripts\activate
```

### Instalação de bibliotecas

```bash
pip install -r requirements.txt
```

### Criação do banco de dados

1. No arquivo `.streamlit/example.toml` (aba "[database]"), preencha os campos necessários para realizar a conexão com o banco de dados
2. No Postgresql (console ou pgAdmin) crie um novo usuário e database com os dados preenchidos anteriormente
3. Por fim, modifique o nome do arquivo de `example.toml` para `secrets.toml`

### Criação das tabelas

Executar o comando:

```bash
# Função built-in (c/ SQLAlchemy)
python -m database.CriarTabelas
```

ou 

```bash
# Arquivo schema.sql (substituir "nome_usuario" e "nome_banco")
psql -U nome_usuario -d nome_banco -f schema.sql
```

### População do banco 

Para popular o banco de dados com um conjunto inicial de dados, execute o seguinte comando:

```bash
# Arquivo dados.sql (substituir "nome_usuario" e "nome_banco")
psql -U nome_usuario -d nome_banco -f dados.sql
```

Depois de executar o comando acima, é necessário que o arquivo `usuarioslogin.sql` seja modificado nas linhas comentadas. Nos campos de e-mail (especialmente de Admin e Aluno), informe e-mails que você detenha, pois é com eles que você conseguirá ter acesso ao sistema. Interagir com o sistema nas facetas de Admin e Aluno é suficiente para visualizar todas as funcionalidades do mesmo.

Após a modificação, execute o seguinte comando:

```bash
# Arquivo usuarioslogin.sql (substituir "nome_usuario" e "nome_banco")
psql -U nome_usuario -d nome_banco -f usuarioslogin.sql
```

### Recuperar backup do banco (opcional)

Se houve algum problema nas últimas etapas relacionadas ao banco de dados, apenas recrie o database normalmente, e tente recuperar o backup completo do banco:

```bash
# Arquivo banco.backup (substituir "nome_usuario" e "nome_banco")
pg_restore -U nome_usuario -d nome_banco banco.backup
```

Se foi feita a restauração pelo backup, modifique os dados em `usuarioslogin.sql`, e execute o comando como citado na seção de "População do banco".

### Configuração do login com OAuth

Para realizar login com Google na aplicação, basta seguir os passos a seguir:

1. Entre no link `https://console.cloud.google.com/apis/credentials`
2. Crie ou selecione um projeto
3. Na aba "Credenciais", clique em Criar Credenciais -> ID do Cliente OAuth
4. Selecione o tipo de aplicativo "Aplicativo da Web"
5. Dê um nome qualquer
6. Na seção "URIs de redirecionamento autorizados", adicione a URI `http://localhost:8501/oauth2callback`
7. Clique em Criar. Daí serão gerados o ID do cliente e a Chave secreta do cliente. Atualize o arquivo `.streamlit/example.toml` com esses dados (aba "[auth]")
8. Por fim, caso não tenha o feito antes, basta modificar o nome do arquivo de `example.toml` para `secrets.toml`

Caso tenha algum problema fazendo o login mesmo após a configuração, entre no link `https://console.cloud.google.com/auth/audience`, selecione o mesmo projeto anterior, e defina o "Status de publicação" como "Em produção"

### Executar com Streamlit

Executar o comando:

```bash
streamlit run app.py
```