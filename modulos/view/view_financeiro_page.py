import re
import streamlit as st
from modulos.financeiro.financeiro_service import (listarFinanceiroCpf, listarFinanceiroId)
from modulos.utils.view_utils import formatar_cpf, limpar_consulta_financeiro
from modulos.utils.view_visual import (AcaoView, CampoBusca, CampoView, SecaoView, renderizarCabecalhoView, renderizarFormularioBusca, renderizarMensagemInicial, renderizarRegistroView)

# Tela de visualização de financeiro
def telaViewFinanceiro():

    if "financeiro_id" in st.session_state:
        st.session_state["consulta_financeiro_id"] = st.session_state.pop(
            "financeiro_id"
        )

    financeiro = None

    # Função de navegação 
    def voltar():
        from modulos.rotas import (
            listagem_financeiro_page,
        )

        st.switch_page(listagem_financeiro_page)

    renderizarCabecalhoView(categoria="View", titulo="Consultar financeiro", descricao=("Localize um funcionário utilizando " "o CPF ou o identificador."), ao_voltar=voltar, prefixo_chave="financeiro")

    buscar, valores = renderizarFormularioBusca(
        campos=[
            CampoBusca(
                nome="cpf",
                rotulo="CPF",
                placeholder="Somente números",
                proporcao=1,
                chave="consulta_financeiro_cpf",
            ),
            CampoBusca(
                nome="id",
                rotulo="ID",
                placeholder="Ex.: 1",
                proporcao=1,
                chave="consulta_financeiro_id_digitado",
            ),
        ],
        prefixo_chave="financeiro",
        titulo="Localizar funcionário",
        descricao=("Informe somente o CPF ou somente o ID."),
    )

    if buscar:
        st.session_state.pop(
            "consulta_financeiro_id",
            None,
        )

        cpf = re.sub(r"\D", "", valores["cpf"])
        idPessoa = valores["id"].strip()

        if not cpf and not idPessoa:
            st.warning("Informe um CPF ou um ID.")

        elif cpf and idPessoa:
            st.warning("Informe somente o CPF ou somente o ID.")

        elif cpf:
            if len(cpf) != 11:
                st.error("O CPF deve possuir 11 números.")

            else:
                financeiro = listarFinanceiroCpf(cpf)

                if financeiro is None:
                    st.error("Funcionário não encontrado.")

                else:
                    st.session_state["consulta_financeiro_id"] = financeiro.pessoa_id

        elif not idPessoa.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            financeiro = listarFinanceiroId(int(idPessoa))

            if financeiro is None:
                st.error("Funcionário não encontrado.")

            else:
                st.session_state["consulta_financeiro_id"] = financeiro.pessoa_id

    idPessoa = st.session_state.get("consulta_financeiro_id")

    if financeiro is None and idPessoa is not None:
        financeiro = listarFinanceiroId(idPessoa)

    if financeiro is None:
        if not buscar:
            renderizarMensagemInicial("Informe um CPF ou ID para consultar.")

        return

    # Função para edição de financeiro
    def editar(registro):
        st.session_state["edicao_financeiro_id"] = registro.pessoa_id

        from modulos.rotas import (
            editar_financeiro_page,
        )

        st.switch_page(editar_financeiro_page)

    acoes = []

    if "ADMIN" in st.session_state.get("roles", []):
        acoes.append(
            AcaoView(
                rotulo="Editar",
                icone=":material/edit:",
                tipo="secondary",
                chave="editar",
                ao_clicar=editar,
            )
        )

    secoes = [
        SecaoView(
            titulo="Dados pessoais",
            descricao=("Informações de identificação " "e contato do funcionário."),
            linhas=[
                [
                    CampoView(
                        rotulo="ID",
                        valor=lambda item: (item.pessoa_id),
                        proporcao=1,
                    ),
                    CampoView(
                        rotulo="Nome",
                        valor=lambda item: (item.pessoa.nome),
                        proporcao=3,
                    ),
                    CampoView(
                        rotulo="CPF",
                        valor=lambda item: formatar_cpf(item.pessoa.cpf),
                        proporcao=2,
                    ),
                ],
                [
                    CampoView(
                        rotulo="E-mail",
                        valor=lambda item: (item.pessoa.email),
                        proporcao=3.5,
                        tipo="email",
                    ),
                    CampoView(
                        rotulo="Telefone",
                        valor=lambda item: (item.pessoa.telefone or "Não informado"),
                        proporcao=2.5,
                    ),
                ],
            ],
        ),
        SecaoView(
            titulo="Vínculo institucional",
            descricao=("Campus ao qual o funcionário " "está vinculado."),
            linhas=[
                [
                    CampoView(
                        rotulo="Campus",
                        valor=lambda item: (
                            item.campus.nome if item.campus else "Não informado"
                        ),
                        proporcao=1,
                        tipo="badge",
                    ),
                ],
            ],
        ),
    ]

    renderizarRegistroView(
        registro=financeiro,
        nome=lambda item: item.pessoa.nome,
        tipo_registro="Financeiro",
        meta=lambda item: (item.campus.nome if item.campus else "Campus não informado"),
        status="Registro localizado",
        secoes=secoes,
        prefixo_chave="financeiro",
        ao_limpar=limpar_consulta_financeiro,
        acoes=acoes,
    )
