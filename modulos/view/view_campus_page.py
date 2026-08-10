import re
import streamlit as st
from modulos.academico.academico_service import listarCampusCnpj, listarCampusId
from modulos.utils.view_utils import formatar_cnpj, limpar_consulta_campus
from modulos.utils.view_visual import (AcaoView, CampoBusca, CampoView, SecaoView, renderizarCabecalhoView, renderizarFormularioBusca, renderizarMensagemInicial, renderizarRegistroView)

# Tela de visualização de campus
def telaViewCampus():

    if "campus_id" in st.session_state:
        st.session_state["consulta_campus_id"] = st.session_state.pop("campus_id")

    campus = None

    # Função de navegação 
    def voltar():
        from modulos.rotas import listagem_campus_page

        st.switch_page(listagem_campus_page)

    renderizarCabecalhoView(categoria="View", titulo="Consultar campus", descricao=("Localize uma unidade utilizando o CNPJ " "ou o identificador."), ao_voltar=voltar, prefixo_chave="campus")

    buscar, valores = renderizarFormularioBusca(
        campos=[
            CampoBusca(
                nome="cnpj",
                rotulo="CNPJ",
                placeholder="Somente números",
                proporcao=1,
                chave="consulta_campus_cnpj",
            ),
            CampoBusca(
                nome="id",
                rotulo="ID",
                placeholder="Ex.: 1",
                proporcao=1,
                chave="consulta_campus_id_digitado",
            ),
        ],
        prefixo_chave="campus",
        titulo="Localizar campus",
        descricao=("Informe somente o CNPJ ou somente o ID."),
    )

    if buscar:
        st.session_state.pop("consulta_campus_id", None)

        cnpj = re.sub(r"\D", "", valores["cnpj"])
        idCampus = valores["id"].strip()

        if not cnpj and not idCampus:
            st.warning("Informe um CNPJ ou um ID.")

        elif cnpj and idCampus:
            st.warning("Informe somente o CNPJ ou somente o ID.")

        elif cnpj:
            if len(cnpj) != 14:
                st.error("O CNPJ deve possuir 14 números.")

            else:
                campus = listarCampusCnpj(cnpj)

                if campus is None:
                    st.error("Campus não encontrado.")

                else:
                    st.session_state["consulta_campus_id"] = campus.id

        elif not idCampus.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            campus = listarCampusId(int(idCampus))

            if campus is None:
                st.error("Campus não encontrado.")

            else:
                st.session_state["consulta_campus_id"] = campus.id

    campusId = st.session_state.get("consulta_campus_id")

    if campus is None and campusId is not None:
        campus = listarCampusId(campusId)

    if campus is None:
        if not buscar:
            renderizarMensagemInicial(
                "Informe um CNPJ ou ID para consultar " "um campus."
            )

        return

    # Função para edição de campus
    def editar(registro):
        st.session_state["edicao_campus_id"] = registro.id

        from modulos.rotas import editar_campus_page

        st.switch_page(editar_campus_page)

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
            titulo="Dados do campus",
            descricao=("Informações institucionais e de contato."),
            linhas=[
                [
                    CampoView(
                        rotulo="ID",
                        valor=lambda item: item.id,
                        proporcao=1,
                    ),
                    CampoView(
                        rotulo="Nome",
                        valor=lambda item: item.nome,
                        proporcao=3,
                    ),
                    CampoView(
                        rotulo="CNPJ",
                        valor=lambda item: formatar_cnpj(item.cnpj),
                        proporcao=2,
                    ),
                ],
                [
                    CampoView(
                        rotulo="E-mail",
                        valor=lambda item: (item.email or "Não informado"),
                        proporcao=3.5,
                        tipo="email",
                    ),
                    CampoView(
                        rotulo="Telefone",
                        valor=lambda item: (item.telefone or "Não informado"),
                        proporcao=2.5,
                    ),
                ],
            ],
        ),
    ]

    renderizarRegistroView(
        registro=campus,
        nome=lambda item: item.nome,
        tipo_registro="Campus",
        meta=lambda item: formatar_cnpj(item.cnpj),
        status="Registro localizado",
        secoes=secoes,
        prefixo_chave="campus",
        ao_limpar=limpar_consulta_campus,
        acoes=acoes,
    )
