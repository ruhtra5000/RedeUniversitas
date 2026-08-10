import streamlit as st
from modulos.academico.academico_service import (definirCoordenador, definirReitor, listarCampus, listarCursos, listarProfessoresCampus, removerCoordenador, removerReitor)
from modulos.utils.academico_visual import (marcarAcoesPagina, painelPagina, renderizarDivisorPagina, renderizarSecaoPagina, renderizarStatusPagina, renderizarTopoPagina)

# Tela de designação de cargos acadêmicos
def telaDesignacaoCargos():
    renderizarTopoPagina(
        titulo="Designação de cargos",
        descricao=(
            "Gerencie os reitores dos campi e os coordenadores "
            "responsáveis pelos cursos."
        ),
        categoria="GESTÃO ACADÊMICA",
    )

    if st.session_state.pop("cargo_sucesso", False):
        st.toast(
            "Operação realizada com sucesso!",
            icon=":material/check:",
        )

    if "cache_campus_cargos" not in st.session_state:
        st.session_state.cache_campus_cargos = listarCampus()

    if "cache_cursos_cargos" not in st.session_state:
        st.session_state.cache_cursos_cargos = listarCursos()

    listaCampus = st.session_state.cache_campus_cargos
    listaCursos = st.session_state.cache_cursos_cargos

    abaReitor, abaCoordenador = st.tabs(
        ["Reitores de campus", "Coordenadores de curso"]
    )

    with abaReitor:
        with painelPagina(
            titulo="Reitoria do campus",
            descricao=(
                "Selecione uma unidade para consultar ou alterar "
                "o professor designado como reitor."
            ),
            contexto="CARGO INSTITUCIONAL",
        ):
            renderizarSecaoPagina(
                numero=1,
                titulo="Campus",
                descricao="Unidade em que a designação será realizada.",
            )

            campusSelecionado = st.selectbox(
                "Selecione o campus",
                options=listaCampus,
                format_func=lambda campus: campus.nome,
                index=None,
                placeholder="Escolha um campus...",
                key="sel_campus_reitor",
            )

            if campusSelecionado:
                campus = next(
                    (item for item in listaCampus if item.id == campusSelecionado.id),
                    None,
                )

                if campus:
                    try:
                        reitorAtual = campus.reitor
                    except Exception:
                        reitorAtual = None
                        st.warning(
                            "Não foi possível carregar os dados do " "reitor atual."
                        )

                    if reitorAtual:
                        try:
                            nomeReitor = reitorAtual.pessoa.nome
                        except Exception:
                            nomeReitor = f"Professor ID {reitorAtual.pessoa_id}"

                        renderizarStatusPagina(
                            rotulo="Reitor atual",
                            valor=nomeReitor,
                        )

                    else:
                        renderizarStatusPagina(
                            rotulo="Reitor atual",
                            valor="Nenhum professor designado",
                        )

                    renderizarDivisorPagina()

                    renderizarSecaoPagina(
                        numero=2,
                        titulo="Nova designação",
                        descricao=("Escolha um professor vinculado ao mesmo campus."),
                    )

                    try:
                        professoresCampus = listarProfessoresCampus(campus.id)
                    except Exception as erro:
                        professoresCampus = []
                        st.error("Erro ao buscar professores do campus: " f"{erro}")

                    colProfessor, colDesignar = st.columns(
                        [3, 2],
                        vertical_alignment="bottom",
                    )

                    with colProfessor:
                        novoReitor = st.selectbox(
                            "Professor do campus",
                            options=professoresCampus,
                            format_func=lambda professor: (
                                professor.pessoa.nome
                                if hasattr(professor, "pessoa")
                                else f"ID: {professor.pessoa_id}"
                            ),
                            index=None,
                            placeholder="Escolha um professor...",
                            key="novo_reitor_sel",
                        )

                    with colDesignar:
                        marcarAcoesPagina()

                        designarReitor = st.button(
                            "Designar reitor",
                            icon=":material/badge:",
                            type="primary",
                            width="stretch",
                            disabled=not novoReitor,
                            key="btn_designar_reitor",
                        )

                    if designarReitor:
                        try:
                            definirReitor(
                                campus.id,
                                novoReitor.pessoa_id,
                            )
                            st.session_state.cargo_sucesso = True
                            st.session_state.pop(
                                "cache_campus_cargos",
                                None,
                            )
                            st.rerun()

                        except Exception as erro:
                            st.error(f"Erro ao designar: {erro}")

                    if reitorAtual:
                        destituirReitor = st.button(
                            "Destituir reitor atual",
                            icon=":material/person_remove:",
                            width="stretch",
                            key="btn_destituir_reitor",
                        )

                        if destituirReitor:
                            try:
                                removerReitor(campus.id)
                                st.session_state.cargo_sucesso = True
                                st.session_state.pop(
                                    "cache_campus_cargos",
                                    None,
                                )
                                st.rerun()

                            except Exception as erro:
                                st.error(f"Erro ao destituir: {erro}")

    with abaCoordenador:
        with painelPagina(
            titulo="Coordenação do curso",
            descricao=(
                "Selecione um curso para consultar ou alterar "
                "seu professor coordenador."
            ),
            contexto="CARGO ACADÊMICO",
        ):
            renderizarSecaoPagina(
                numero=1,
                titulo="Curso",
                descricao="Curso em que a designação será realizada.",
            )

            cursoSelecionado = st.selectbox(
                "Selecione o curso",
                options=listaCursos,
                format_func=lambda curso: curso.nome,
                index=None,
                placeholder="Escolha um curso...",
                key="sel_curso_coord",
            )

            if cursoSelecionado:
                curso = next(
                    (item for item in listaCursos if item.id == cursoSelecionado.id),
                    None,
                )

                if curso:
                    try:
                        coordenadorAtual = curso.coordenador
                    except Exception:
                        coordenadorAtual = None
                        st.warning(
                            "Não foi possível carregar os dados do "
                            "coordenador atual."
                        )

                    if coordenadorAtual:
                        try:
                            nomeCoordenador = coordenadorAtual.pessoa.nome
                        except Exception:
                            nomeCoordenador = (
                                "Professor ID " f"{coordenadorAtual.pessoa_id}"
                            )

                        renderizarStatusPagina(
                            rotulo="Coordenador atual",
                            valor=nomeCoordenador,
                        )

                    else:
                        renderizarStatusPagina(
                            rotulo="Coordenador atual",
                            valor="Nenhum professor designado",
                        )

                    renderizarDivisorPagina()

                    renderizarSecaoPagina(
                        numero=2,
                        titulo="Nova designação",
                        descricao=(
                            "Escolha um professor vinculado ao campus " "do curso."
                        ),
                    )

                    try:
                        professoresCampus = listarProfessoresCampus(curso.campus_id)
                    except Exception as erro:
                        professoresCampus = []
                        st.error("Erro ao buscar professores do campus: " f"{erro}")

                    colProfessor, colDesignar = st.columns(
                        [3, 2],
                        vertical_alignment="bottom",
                    )

                    with colProfessor:
                        novoCoordenador = st.selectbox(
                            "Professor do campus",
                            options=professoresCampus,
                            format_func=lambda professor: (
                                professor.pessoa.nome
                                if hasattr(professor, "pessoa")
                                else f"ID: {professor.pessoa_id}"
                            ),
                            index=None,
                            placeholder="Escolha um professor...",
                            key="novo_coord_sel",
                        )

                    with colDesignar:
                        marcarAcoesPagina()

                        designarCoordenador = st.button(
                            "Designar coordenador",
                            icon=":material/supervisor_account:",
                            type="primary",
                            width="stretch",
                            disabled=not novoCoordenador,
                            key="btn_designar_coord",
                        )

                    if designarCoordenador:
                        try:
                            definirCoordenador(
                                curso.id,
                                novoCoordenador.pessoa_id,
                            )
                            st.session_state.cargo_sucesso = True
                            st.session_state.pop(
                                "cache_cursos_cargos",
                                None,
                            )
                            st.rerun()

                        except Exception as erro:
                            st.error(f"Erro ao designar: {erro}")

                    if coordenadorAtual:
                        destituirCoordenador = st.button(
                            "Destituir coordenador atual",
                            icon=":material/person_remove:",
                            width="stretch",
                            key="btn_destituir_coord",
                        )

                        if destituirCoordenador:
                            try:
                                removerCoordenador(curso.id)
                                st.session_state.cargo_sucesso = True
                                st.session_state.pop(
                                    "cache_cursos_cargos",
                                    None,
                                )
                                st.rerun()

                            except Exception as erro:
                                st.error(f"Erro ao destituir: {erro}")
