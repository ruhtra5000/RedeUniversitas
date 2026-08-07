import streamlit as st
import time
from sqlalchemy.exc import SQLAlchemyError

from modulos.academico.academico_service import listarAlunoId, listarTurmasDisponiveisAluno
from modulos.cadastros.matricula import criarMatricula
from database.entidades.Matricula import Matricula

@st.dialog("Confirmação de Segurança")
def modal_confirmacao(aluno, turmas_selecionadas):
    st.warning("Tem certeza que deseja efetivar a matrícula nas seguintes turmas/disciplinas?")
    
    for t in turmas_selecionadas:
        st.write(f"• **{t.disciplina.nome}** (Turma {t.codigo})")
        
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Confirmar", type="primary", use_container_width=True):
            sucesso = True
            with st.spinner("Efetivando matrículas..."):
                for t in turmas_selecionadas:
                    try:
                        nova_matricula = Matricula(
                            aluno_id=aluno.pessoa_id,
                            turma_id=t.id,
                            disciplina_id=t.disciplina_id
                        )
                        criarMatricula(nova_matricula, aluno, t.disciplina)
                    except Exception as e:
                        st.error(f"Erro ao matricular na turma {t.codigo}: {e}")
                        sucesso = False
                        
            if sucesso:
                st.success("Matrícula(s) efetivada(s) com sucesso!")
                time.sleep(1.5)
                st.rerun()

    with col2:
        if st.button("Cancelar", use_container_width=True):
            st.rerun()

def telaRenovarMatricula():
    st.title(":material/school: Renovar Matrícula")
    st.caption("Efetue a sua matrícula nas disciplinas disponíveis para o seu curso.")
    
    roles = st.session_state.get("roles", [])
    if "ALUNO" not in roles:
        st.error("Acesso negado. Apenas alunos podem acessar esta página.")
        return
        
    pessoa_id = st.session_state.get("pessoa_id")
    if not pessoa_id:
        st.error("Sessão inválida. Por favor, refaça o login.")
        return
        
    try:
        aluno = listarAlunoId(pessoa_id)
    except Exception as e:
        st.error(f"Erro ao carregar dados do aluno: {e}")
        return

    st.write("---")

    # Input disabled do Aluno
    st.text_input("Aluno", value=aluno.pessoa.nome, disabled=True)
    st.text_input("Curso", value=aluno.curso.nome, disabled=True)
    
    # 1 e 2. Listar e filtrar turmas válidas diretamente via backend
    turmas_validas = listarTurmasDisponiveisAluno(pessoa_id)
            
    if not turmas_validas:
        st.info("Não há turmas disponíveis para matrícula no momento. Ou você já concluiu todas as disciplinas possíveis, ou faltam pré-requisitos.")
        return
        
    st.subheader("Seleção de Disciplinas")
    
    # Select de turmas
    turmas_selecionadas = st.multiselect(
        "Turmas Disponíveis",
        options=turmas_validas,
        format_func=lambda t: f"{t.disciplina.nome} (Turma: {t.codigo} - Semestre: {t.semestre})"
    )
    
    if st.button("Confirmar Inscrição", type="primary", disabled=len(turmas_selecionadas) == 0):
        modal_confirmacao(aluno, turmas_selecionadas)
