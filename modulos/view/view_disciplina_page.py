import streamlit as st
from modulos.academico.academico_service import (listarDisciplinaCodigo, listarDisciplinaId, listarPreRequisitosDisciplina)
from modulos.utils.view_utils import limpar_consulta_disciplina
from modulos.utils.view_visual import (AcaoView, CampoBusca, CampoView, SecaoView, renderizarCabecalhoView, renderizarFormularioBusca, renderizarMensagemInicial, renderizarRegistroView)

# Tela de visualização de disciplina
def telaViewDisciplina():

    if "disciplina_id" in st.session_state:
        st.session_state["consulta_disciplina_id"] = st.session_state.pop(
            "disciplina_id"
        )

    disciplina = None

    # Função de navegação 
    def voltar():
        from modulos.rotas import (
            listagem_disciplina_page,
        )

        st.switch_page(listagem_disciplina_page)

    renderizarCabecalhoView(categoria="View", titulo="Consultar disciplina", descricao=("Localize uma disciplina utilizando " "o código ou o identificador."), ao_voltar=voltar, prefixo_chave="disciplina")

    buscar, valores = renderizarFormularioBusca(
        campos=[
            CampoBusca(
                nome="codigo",
                rotulo="Código",
                placeholder="Ex.: 1-00001",
                proporcao=1,
                chave="consulta_disciplina_codigo",
            ),
            CampoBusca(
                nome="id",
                rotulo="ID",
                placeholder="Ex.: 1",
                proporcao=1,
                chave="consulta_disciplina_id_digitado",
            ),
        ],
        prefixo_chave="disciplina",
        titulo="Localizar disciplina",
        descricao=("Informe somente o código ou somente o ID."),
    )

    if buscar:
        st.session_state.pop(
            "consulta_disciplina_id",
            None,
        )

        codigo = valores["codigo"].strip()
        idDisciplina = valores["id"].strip()

        if not codigo and not idDisciplina:
            st.warning("Informe um código ou um ID.")

        elif codigo and idDisciplina:
            st.warning("Informe somente o código ou somente o ID.")

        elif codigo:
            disciplina = listarDisciplinaCodigo(codigo)

            if disciplina is None:
                st.error("Disciplina não encontrada.")

            else:
                st.session_state["consulta_disciplina_id"] = disciplina.id

        elif not idDisciplina.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            disciplina = listarDisciplinaId(int(idDisciplina))

            if disciplina is None:
                st.error("Disciplina não encontrada.")

            else:
                st.session_state["consulta_disciplina_id"] = disciplina.id

    disciplinaId = st.session_state.get("consulta_disciplina_id")

    if disciplina is None and disciplinaId is not None:
        disciplina = listarDisciplinaId(disciplinaId)

    if disciplina is None:
        if not buscar:
            renderizarMensagemInicial(
                "Informe um código ou ID para " "consultar uma disciplina."
            )

        return

    preRequisitos = listarPreRequisitosDisciplina(disciplina.id)

    textoPreRequisitos = (
        " • ".join(
            (f"{preRequisito.codigo or 'Sem código'}" f" — {preRequisito.nome}")
            for preRequisito in preRequisitos
        )
        if preRequisitos
        else "Esta disciplina não possui pré-requisitos."
    )

    # Função para edição de disciplina
    def editar(registro):
        st.session_state["edicao_disciplina_id"] = registro.id

        from modulos.rotas import (
            editar_disciplina_page,
        )

        st.switch_page(editar_disciplina_page)

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
            titulo="Dados da disciplina",
            descricao=("Identificação e informações " "acadêmicas."),
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
                        proporcao=1.8,
                    ),
                    CampoView(
                        rotulo="Nome",
                        valor=lambda item: item.nome,
                        proporcao=3.2,
                    ),
                ],
                [
                    CampoView(
                        rotulo="Carga horária",
                        valor=lambda item: (f"{item.carga_horaria} horas"),
                        proporcao=1.5,
                    ),
                    CampoView(
                        rotulo="Tipo",
                        valor=lambda item: (
                            "Obrigatória" if item.obrigatoria else "Optativa"
                        ),
                        proporcao=1.5,
                        tipo="badge",
                    ),
                    CampoView(
                        rotulo="Curso",
                        valor=lambda item: (
                            item.curso.nome if item.curso else "Não informado"
                        ),
                        proporcao=3,
                    ),
                ],
            ],
        ),
        SecaoView(
            titulo="Pré-requisitos",
            descricao=("Disciplinas exigidas antes " "deste componente curricular."),
            linhas=[
                [
                    CampoView(
                        rotulo="Disciplinas",
                        valor=textoPreRequisitos,
                        proporcao=1,
                    ),
                ],
            ],
        ),
    ]

    renderizarRegistroView(
        registro=disciplina,
        nome=lambda item: item.nome,
        tipo_registro="Disciplina",
        meta=lambda item: (item.codigo or "Código não informado"),
        status=lambda item: ("Obrigatória" if item.obrigatoria else "Optativa"),
        secoes=secoes,
        prefixo_chave="disciplina",
        ao_limpar=limpar_consulta_disciplina,
        acoes=acoes,
    )
