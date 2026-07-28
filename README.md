# Rede Universitas

Rede Universitas trata-se de uma solução de software para o gerenciamento e acompanhamento de uma rede privada de universidades multi-campi, contando com: lançamento de notas, criação de bolsas, gerenciamento de estoque e compras, geração automática de mensalidades, controle e visualização de fluxo de caixa, visualização de dashboards, etc.

---

## Equipe

- Arthur de Sá Tenório
- Guilherme Paes Cavalcanti
- Victor Cauã Tavares Inácio

---

## Requisitos de Software

Antes de executar o projeto, certifique-se de possuir instalado:

| Software | Versão |
|----------|---------|
| Python | **3.14.3** ou superior |
| pip | **25.3** ou superior |
| PostgreSQL | **17** ou superior |

---

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

---

## Configuração do banco de dados

### Criação do banco em si

Na pasta `.streamlit/secrets.toml` há os dados padrões para conexão com o banco de dados, mas eles podem ser modificados. Portanto, basta criar um novo database no Postgresql seguindo os dados lá contidos, ou atualizar o arquivo com as novas credenciais.

### Criação das tabelas

Executar o comando:

```bash
# Função built-in (c/ SQLAlchemy)
python -m database.CriarTabelas
```

ou 

```bash
# Arquivo schema.sql (sem alterações no secrets.toml)
psql -U user_universitas -d rede_universitas -f schema.sql

# Arquivo schema.sql (caso tenha alterado o secrets.toml, substituir "nome_usuario" e "nome_banco")
psql -U nome_usuario -d nome_banco -f schema.sql
```

### População do banco (recomendado)

Caso deseje popular o banco de dados com um conjunto inicial de dados, execute o seguinte comando:

```bash
# to do
```

### Executar com Streamlit

Executar o comando:

```bash
streamlit run app.py
```