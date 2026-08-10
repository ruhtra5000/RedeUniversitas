import streamlit as st
from modulos.academico.academico_service import listarTurmaCodigo, listarTurmaId
from modulos.utils.view_utils import limpar_consulta_turma
from modulos.utils.view_visual import (AcaoView, CampoBusca, CampoView, SecaoView, renderizarCabecalhoView, renderizarFormularioBusca, renderizarMensagemInicial, renderizarRegistroView)

# Tela de visualização de turma
def telaViewTurma():

    if "turma_id" in st.session_state:
        st.session_state["consulta_turma_id"] = st.session_state.pop("turma_id")

    turma = None

    # Função de navegação 
    def voltar():
        from modulos.rotas import listagem_turma_page

        st.switch_page(listagem_turma_page)

    renderizarCabecalhoView(categoria="View", titulo="Consultar turma", descricao=("Localize uma turma utilizando " "o código ou o identificador."), ao_voltar=voltar, prefixo_chave="turma")

    buscar, valores = renderizarFormularioBusca(
        campos=[
            CampoBusca(
                nome="codigo",
                rotulo="Código",
                placeholder="Ex.: 1-00001",
                proporcao=1,
                chave="consulta_turma_codigo",
            ),
            CampoBusca(
                nome="id",
                rotulo="ID",
                placeholder="Ex.: 1",
                proporcao=1,
                chave="consulta_turma_id_digitado",
            ),
        ],
        prefixo_chave="turma",
        titulo="Localizar turma",
        descricao=("Informe somente o código ou somente o ID."),
    )

    if buscar:
        st.session_state.pop("consulta_turma_id", None)

        codigo = valores["codigo"].strip()
        idTurma = valores["id"].strip()

        if not codigo and not idTurma:
            st.warning("Informe um código ou um ID.")

        elif codigo and idTurma:
            st.warning("Informe somente o código ou somente o ID.")

        elif codigo:
            turma = listarTurmaCodigo(codigo)

            if turma is None:
                st.error("Turma não encontrada.")

            else:
                st.session_state["consulta_turma_id"] = turma.id

        elif not idTurma.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            turma = listarTurmaId(int(idTurma))

            if turma is None:
                st.error("Turma não encontrada.")

            else:
                st.session_state["consulta_turma_id"] = turma.id

    turmaId = st.session_state.get("consulta_turma_id")

    if turma is None and turmaId is not None:
        turma = listarTurmaId(turmaId)

    if turma is None:
        if not buscar:
            renderizarMensagemInicial(
                "Informe um código ou ID para " "consultar uma turma."
            )

        return

    # Função para edição de turma
    def editar(registro):
        st.session_state["edicao_turma_id"] = registro.id

        from modulos.rotas import editar_turma_page

        st.switch_page(editar_turma_page)

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
            titulo="Dados da turma",
            descricao=("Identificação e período acadêmico."),
            linhas=[
                [
                    CampoView(
                        rotulo="ID",
                        valor=lambda item: item.id,
                        proporcao=1,
                    ),
                    CampoView(
                        rotulo="Código",
                        valor=lambda item: (item.codigo or "Não informado"),
                        proporcao=2.5,
                    ),
                    CampoView(
                        rotulo="Semestre",
                        valor=lambda item: (item.semestre),
                        proporcao=2.5,
                        tipo="badge",
                    ),
                ],
            ],
        ),
        SecaoView(
            titulo="Vínculos acadêmicos",
            descricao=("Curso, disciplina e professor " "responsável."),
            linhas=[
                [
                    CampoView(
                        rotulo="Curso",
                        valor=lambda item: (
                            item.curso.nome if item.curso else "Não informado"
                        ),
                        proporcao=1,
                    ),
                    CampoView(
                        rotulo="Disciplina",
                        valor=lambda item: (
                            item.disciplina.nome if item.disciplina else "Não informado"
                        ),
                        proporcao=1,
                    ),
                ],
                [
                    CampoView(
                        rotulo="Professor",
                        valor=lambda item: (
                            item.professor.pessoa.nome
                            if item.professor and item.professor.pessoa
                            else "Não informado"
                        ),
                        proporcao=1,
                    ),
                ],
            ],
        ),
    ]

    renderizarRegistroView(
        registro=turma,
        nome=lambda item: (item.codigo or f"Turma {item.id}"),
        tipo_registro="Turma",
        meta=lambda item: (
            item.disciplina.nome if item.disciplina else "Disciplina não informada"
        ),
        status=lambda item: item.semestre,
        secoes=secoes,
        prefixo_chave="turma",
        ao_limpar=limpar_consulta_turma,
        acoes=acoes,
    )
