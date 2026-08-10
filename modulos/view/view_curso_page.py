import streamlit as st
from modulos.academico.academico_service import listarCursoId
from modulos.utils.view_utils import (formatar_mensalidade, formatar_modalidade, limpar_consulta_curso)
from modulos.utils.view_visual import (AcaoView, CampoBusca, CampoView, SecaoView, renderizarCabecalhoView, renderizarFormularioBusca, renderizarMensagemInicial, renderizarRegistroView)

# Tela de visualização de curso
def telaViewCurso():

    if "curso_id" in st.session_state:
        st.session_state["consulta_curso_id"] = st.session_state.pop("curso_id")

    curso = None

    # Função de navegação 
    def voltar():
        from modulos.rotas import listagem_cursos_page

        st.switch_page(listagem_cursos_page)

    renderizarCabecalhoView(categoria="View", titulo="Consultar curso", descricao=("Localize um curso utilizando " "o seu identificador."), ao_voltar=voltar, prefixo_chave="curso",)

    buscar, valores = renderizarFormularioBusca(
        campos=[
            CampoBusca(
                nome="id",
                rotulo="ID do curso",
                placeholder="Ex.: 1",
                proporcao=1,
                chave="consulta_curso_busca",
            ),
        ],
        prefixo_chave="curso",
        titulo="Localizar curso",
        descricao="Informe o ID do curso.",
    )

    if buscar:
        st.session_state.pop("consulta_curso_id", None)

        idCurso = valores["id"].strip()

        if not idCurso:
            st.warning("Informe o ID do curso.")

        elif not idCurso.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            curso = listarCursoId(int(idCurso))

            if curso is None:
                st.error("Curso não encontrado.")

            else:
                st.session_state["consulta_curso_id"] = curso.id

    cursoId = st.session_state.get("consulta_curso_id")

    if curso is None and cursoId is not None:
        curso = listarCursoId(cursoId)

    if curso is None:
        if not buscar:
            renderizarMensagemInicial("Informe um ID para consultar um curso.")

        return

    # Função para edição de curso
    def editar(registro):
        st.session_state["edicao_curso_id"] = registro.id

        from modulos.rotas import editar_curso_page

        st.switch_page(editar_curso_page)

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
            titulo="Dados principais",
            descricao=("Informações acadêmicas e financeiras " "do curso."),
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
                        proporcao=3.2,
                    ),
                    CampoView(
                        rotulo="Modalidade",
                        valor=lambda item: (formatar_modalidade(item.modalidade)),
                        proporcao=1.8,
                        tipo="badge",
                    ),
                ],
                [
                    CampoView(
                        rotulo="Mensalidade base",
                        valor=lambda item: (
                            formatar_mensalidade(item.mensalidade_base)
                        ),
                        proporcao=2,
                        tipo="destaque",
                    ),
                    CampoView(
                        rotulo="Carga horária",
                        valor=lambda item: (f"{item.carga_horaria} horas"),
                        proporcao=2,
                    ),
                    CampoView(
                        rotulo="Duração",
                        valor=lambda item: (
                            f"{item.dur_min_semestre} a "
                            f"{item.dur_max_semestre} "
                            "semestres"
                        ),
                        proporcao=2,
                    ),
                ],
            ],
        ),
        SecaoView(
            titulo="Vínculos institucionais",
            descricao=("Campus e coordenação responsáveis."),
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
                    CampoView(
                        rotulo="Coordenador",
                        valor=lambda item: (
                            item.coordenador.pessoa.nome
                            if item.coordenador
                            else ("Nenhum coordenador " "definido")
                        ),
                        proporcao=1,
                    ),
                ],
            ],
        ),
    ]

    renderizarRegistroView(
        registro=curso,
        nome=lambda item: item.nome,
        tipo_registro="Curso",
        meta=lambda item: (item.campus.nome if item.campus else "Campus não informado"),
        status=lambda item: formatar_modalidade(item.modalidade),
        secoes=secoes,
        prefixo_chave="curso",
        ao_limpar=limpar_consulta_curso,
        acoes=acoes,
    )
