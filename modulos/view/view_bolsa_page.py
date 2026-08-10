import streamlit as st
from modulos.academico.academico_service import listarBolsaId
from modulos.utils.view_utils import (formatar_data, formatar_percentual, formatar_status, limpar_consulta_bolsa,)
from modulos.utils.view_visual import (CampoBusca, CampoView, SecaoView, renderizarCabecalhoView, renderizarFormularioBusca, renderizarMensagemInicial, renderizarRegistroView)

# Tela de visualização de bolsa
def telaViewBolsa():

    if "bolsa_id" in st.session_state:
        st.session_state["consulta_bolsa_id"] = st.session_state.pop("bolsa_id")

    bolsa = None

    # Função de navegação 
    def voltar():
        from modulos.rotas import listagem_bolsa_page

        st.switch_page(listagem_bolsa_page)

    renderizarCabecalhoView(categoria="View", titulo="Consultar bolsa", descricao=("Localize uma bolsa acadêmica utilizando " "o seu identificador."), ao_voltar=voltar, prefixo_chave="bolsa",)

    buscar, valores = renderizarFormularioBusca(
        campos=[
            CampoBusca(
                nome="id",
                rotulo="ID da bolsa",
                placeholder="Ex.: 1",
                proporcao=1,
                chave="consulta_bolsa_id_digitado",
            ),
        ],
        prefixo_chave="bolsa",
        titulo="Localizar bolsa",
        descricao="Informe o ID da bolsa.",
    )

    if buscar:
        st.session_state.pop("consulta_bolsa_id", None)

        idBolsa = valores["id"].strip()

        if not idBolsa:
            st.warning("Informe o ID da bolsa.")

        elif not idBolsa.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            bolsa = listarBolsaId(int(idBolsa))

            if bolsa is None:
                st.error("Bolsa não encontrada.")

            else:
                st.session_state["consulta_bolsa_id"] = bolsa.id

    idBolsa = st.session_state.get("consulta_bolsa_id")

    if bolsa is None and idBolsa is not None:
        bolsa = listarBolsaId(idBolsa)

    if bolsa is None:
        if not buscar:
            renderizarMensagemInicial("Informe o ID para consultar uma bolsa.")

        return

    secoes = [
        SecaoView(
            titulo="Aluno",
            descricao=("Beneficiário vinculado à bolsa."),
            linhas=[
                [
                    CampoView(
                        rotulo="ID da bolsa",
                        valor=lambda item: item.id,
                        proporcao=1,
                    ),
                    CampoView(
                        rotulo="Aluno",
                        valor=lambda item: (item.aluno.pessoa.nome),
                        proporcao=3,
                    ),
                    CampoView(
                        rotulo="Matrícula",
                        valor=lambda item: (item.aluno.matricula),
                        proporcao=2,
                    ),
                ],
            ],
        ),
        SecaoView(
            titulo="Dados da bolsa",
            descricao=("Benefício, vigência e situação atual."),
            linhas=[
                [
                    CampoView(
                        rotulo="Tipo",
                        valor=lambda item: getattr(
                            item.tipo_bolsa,
                            "value",
                            item.tipo_bolsa,
                        ),
                        proporcao=2,
                    ),
                    CampoView(
                        rotulo="Desconto",
                        valor=lambda item: (
                            formatar_percentual(item.percentual_desconto)
                        ),
                        proporcao=2,
                        tipo="destaque",
                    ),
                    CampoView(
                        rotulo="Status",
                        valor=lambda item: (formatar_status(item.status)),
                        proporcao=2,
                        tipo="badge",
                    ),
                ],
                [
                    CampoView(
                        rotulo="Data de início",
                        valor=lambda item: formatar_data(item.data_inicio),
                        proporcao=1,
                    ),
                    CampoView(
                        rotulo="Data de término",
                        valor=lambda item: formatar_data(item.data_fim),
                        proporcao=1,
                    ),
                ],
            ],
        ),
    ]

    renderizarRegistroView(
        registro=bolsa,
        nome=lambda item: f"Bolsa #{item.id}",
        tipo_registro="Bolsa acadêmica",
        meta=lambda item: item.aluno.pessoa.nome,
        status=lambda item: formatar_status(item.status),
        secoes=secoes,
        prefixo_chave="bolsa",
        ao_limpar=limpar_consulta_bolsa,
    )
