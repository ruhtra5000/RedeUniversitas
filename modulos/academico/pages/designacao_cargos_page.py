import streamlit as st
from modulos.academico.academico_service import (
    listarCampus, listarCursos, listarProfessoresCampus,
    definirReitor, removerReitor, definirCoordenador, removerCoordenador
)

def telaDesignacaoCargos():
    st.title("Designação de Cargos")
    st.caption("Faça a designação ou destituição de Reitores de Campus e Coordenadores de Curso.")

    if st.session_state.pop("cargo_sucesso", False):
        st.toast("Operação realizada com sucesso!", icon=":material/check:")

    if "cache_campus_cargos" not in st.session_state:
        st.session_state.cache_campus_cargos = listarCampus()
    if "cache_cursos_cargos" not in st.session_state:
        st.session_state.cache_cursos_cargos = listarCursos()

    lista_campus = st.session_state.cache_campus_cargos
    lista_cursos = st.session_state.cache_cursos_cargos

    aba_reitor, aba_coordenador = st.tabs(["Reitores de Campus", "Coordenadores de Curso"])

    with aba_reitor:
        with st.container(border=True):
            campus_selecionado = st.selectbox(
                "Selecione o Campus",
                options=lista_campus,
                format_func=lambda c: c.nome,
                index=None,
                placeholder="Escolha um campus...",
                key="sel_campus_reitor"
            )

            if campus_selecionado:
                campus_real = next((c for c in lista_campus if c.id == campus_selecionado.id), None)
                
                if campus_real:
                    # Verifica reitor atual
                    try:
                        reitor_atual = campus_real.reitor
                    except Exception:
                        reitor_atual = None
                        st.warning("Não foi possível carregar as informações do reitor atual devido à falta de carregamento no banco.")

                    if reitor_atual:
                        try:
                            nome_reitor = reitor_atual.pessoa.nome
                        except Exception:
                            nome_reitor = f"ID do Professor: {reitor_atual.pessoa_id}"
                        st.info(f"**Reitor Atual:** {nome_reitor}")
                    else:
                        st.warning("Este Campus atualmente não possui um Reitor designado.")

                    st.write("---")
                    st.write("#### Atualizar Cargo")
                    
                    try:
                        professores_campus = listarProfessoresCampus(campus_real.id)
                    except Exception as e:
                        professores_campus = []
                        st.error(f"Erro ao buscar professores do campus: {e}")

                    col1, col2 = st.columns([3, 2], vertical_alignment="bottom")
                    with col1:
                        novo_reitor = st.selectbox(
                            "Selecione um Professor do Campus para Designar",
                            options=professores_campus,
                            format_func=lambda p: p.pessoa.nome if hasattr(p, 'pessoa') else f"ID: {p.pessoa_id}",
                            index=None,
                            placeholder="Escolha um professor...",
                            key="novo_reitor_sel"
                        )
                    
                    with col2:
                        if st.button("Designar Novo Reitor", type="primary", width="stretch", disabled=not novo_reitor):
                            try:
                                definirReitor(campus_real.id, novo_reitor.pessoa_id)
                                st.session_state.cargo_sucesso = True
                                if "cache_campus_cargos" in st.session_state: del st.session_state["cache_campus_cargos"]
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao designar: {e}")
                    
                    if reitor_atual:
                        st.write("")
                        if st.button("Destituir Reitor Atual", type="secondary"):
                            try:
                                removerReitor(campus_real.id)
                                st.session_state.cargo_sucesso = True
                                if "cache_campus_cargos" in st.session_state: del st.session_state["cache_campus_cargos"]
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao destituir: {e}")

    with aba_coordenador:
        with st.container(border=True):
            curso_selecionado = st.selectbox(
                "Selecione o Curso",
                options=lista_cursos,
                format_func=lambda c: f"{c.nome}",
                index=None,
                placeholder="Escolha um curso...",
                key="sel_curso_coord"
            )

            if curso_selecionado:
                curso_real = next((c for c in lista_cursos if c.id == curso_selecionado.id), None)
                
                if curso_real:
                    try:
                        coord_atual = curso_real.coordenador
                    except Exception:
                        coord_atual = None
                        st.warning("Não foi possível carregar as informações do coordenador atual devido à falta de carregamento no banco.")

                    if coord_atual:
                        try:
                            nome_coord = coord_atual.pessoa.nome
                        except Exception:
                            nome_coord = f"ID do Professor: {coord_atual.pessoa_id}"
                        st.info(f"**Coordenador Atual:** {nome_coord}")
                    else:
                        st.warning("Este Curso atualmente não possui um Coordenador designado.")

                    st.write("---")
                    st.write("#### Atualizar Cargo")
                    
                    try:
                        professores_curso_campus = listarProfessoresCampus(curso_real.campus_id)
                    except Exception as e:
                        professores_curso_campus = []
                        st.error(f"Erro ao buscar professores do campus: {e}")

                    col1, col2 = st.columns([3, 2], vertical_alignment="bottom")
                    with col1:
                        novo_coord = st.selectbox(
                            "Selecione um Professor do Campus para Designar",
                            options=professores_curso_campus,
                            format_func=lambda p: p.pessoa.nome if hasattr(p, 'pessoa') else f"ID: {p.pessoa_id}",
                            index=None,
                            placeholder="Escolha um professor...",
                            key="novo_coord_sel"
                        )
                    
                    with col2:
                        if st.button("Designar Novo Coordenador", type="primary", width="stretch", disabled=not novo_coord, key="btn_designar_coord"):
                            try:
                                definirCoordenador(curso_real.id, novo_coord.pessoa_id)
                                st.session_state.cargo_sucesso = True
                                if "cache_cursos_cargos" in st.session_state: del st.session_state["cache_cursos_cargos"]
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao designar: {e}")
                    
                    if coord_atual:
                        st.write("")
                        if st.button("Destituir Coordenador Atual", type="secondary", key="btn_destituir_coord"):
                            try:
                                removerCoordenador(curso_real.id)
                                st.session_state.cargo_sucesso = True
                                if "cache_cursos_cargos" in st.session_state: del st.session_state["cache_cursos_cargos"]
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao destituir: {e}")
