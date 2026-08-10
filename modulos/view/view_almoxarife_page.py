import re
import streamlit as st
from modulos.estoque.estoque_service import listarAlmoxarifeCpf, listarAlmoxarifeId
from modulos.utils.view_utils import formatar_cpf, limpar_consulta_almoxarife
from modulos.utils.view_visual import (AcaoView, CampoBusca, CampoView, SecaoView, renderizarCabecalhoView, renderizarFormularioBusca, renderizarMensagemInicial, renderizarRegistroView)

# Tela de visualização de almoxarife
def telaViewAlmoxarife():

    if "almoxarife_id" in st.session_state:
        st.session_state["consulta_almoxarife_id"] = st.session_state.pop(
            "almoxarife_id"
        )

    almoxarife = None

    # Função de navegação 
    def voltar():
        from modulos.rotas import (
            listagem_almoxarife_page,
        )

        st.switch_page(listagem_almoxarife_page)

    renderizarCabecalhoView(categoria="View",titulo="Consultar almoxarife",descricao=("Localize um profissional utilizando " "o CPF ou o identificador."),ao_voltar=voltar,prefixo_chave="almoxarife")

    buscar, valores = renderizarFormularioBusca(
        campos=[
            CampoBusca(
                nome="cpf",
                rotulo="CPF",
                placeholder="Somente números",
                proporcao=1,
                chave="consulta_almoxarife_cpf",
            ),
            CampoBusca(
                nome="id",
                rotulo="ID",
                placeholder="Ex.: 1",
                proporcao=1,
                chave="consulta_almoxarife_id_digitado",
            ),
        ],
        prefixo_chave="almoxarife",
        titulo="Localizar almoxarife",
        descricao=("Informe somente o CPF ou somente o ID."),
    )

    if buscar:
        st.session_state.pop(
            "consulta_almoxarife_id",
            None,
        )

        cpf = re.sub(
            r"\D",
            "",
            valores["cpf"],
        )

        idPessoa = valores["id"].strip()

        if not cpf and not idPessoa:
            st.warning("Informe um CPF ou um ID.")

        elif cpf and idPessoa:
            st.warning("Informe somente o CPF " "ou somente o ID.")

        elif cpf:
            if len(cpf) != 11:
                st.error("O CPF deve possuir 11 números.")

            else:
                almoxarife = listarAlmoxarifeCpf(cpf)

                if almoxarife is None:
                    st.error("Almoxarife não encontrado.")

                else:
                    st.session_state["consulta_almoxarife_id"] = almoxarife.pessoa_id

        elif not idPessoa.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            almoxarife = listarAlmoxarifeId(int(idPessoa))

            if almoxarife is None:
                st.error("Almoxarife não encontrado.")

            else:
                st.session_state["consulta_almoxarife_id"] = almoxarife.pessoa_id

    idPessoa = st.session_state.get("consulta_almoxarife_id")

    if almoxarife is None and idPessoa is not None:
        almoxarife = listarAlmoxarifeId(idPessoa)

    if almoxarife is None:
        if not buscar:
            renderizarMensagemInicial(
                "Informe um CPF ou ID para consultar " "o almoxarife."
            )

        return

    # Função para edição de almoxarife
    def editar(registro):
        st.session_state["edicao_almoxarife_id"] = registro.pessoa_id

        from modulos.rotas import (
            editar_almoxarife_page,
        )

        st.switch_page(editar_almoxarife_page)

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
            descricao=("Informações de identificação " "e contato do profissional."),
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
                        valor=lambda item: (item.pessoa.telefone),
                        proporcao=2.5,
                    ),
                ],
            ],
        ),
        SecaoView(
            titulo="Vínculo institucional",
            descricao=(
                "Unidade institucional à qual " "o profissional está vinculado."
            ),
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

    campus = almoxarife.campus.nome if almoxarife.campus else "Campus não informado"

    renderizarRegistroView(
        registro=almoxarife,
        nome=lambda item: item.pessoa.nome,
        tipo_registro="Almoxarife",
        meta=lambda item: (f"{campus}"),
        status="Registro localizado",
        secoes=secoes,
        prefixo_chave="almoxarife",
        ao_limpar=limpar_consulta_almoxarife,
        acoes=acoes,
    )
