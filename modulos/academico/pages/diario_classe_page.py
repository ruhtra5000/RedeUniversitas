import streamlit as st
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError
from modulos.academico.academico_service import (
    listarProfessores, listarTurmasGeral,
    lancarNota1, lancarNota2, lancarNota3, lancarNotaFinal,
    cadastrarPresenca, fecharTurma
)

def telaDiarioClasse():
    st.title("Diário de Classe")
    st.caption("Faça o lançamento de notas, faltas e o fechamento do semestre para as suas turmas.")

    if st.session_state.pop("diario_salvo", False):
        st.toast("Lançamentos salvos com sucesso!", icon=":material/check:")
        
    if st.session_state.pop("turma_fechada", False):
        st.toast("Turma consolidada com sucesso!", icon=":material/check:")
        
    if "form_key_diario" not in st.session_state:
        st.session_state.form_key_diario = 0

    # --- PROVISÓRIO ---
    # Até implementarmos o sistema de login, o usuário seleciona quem ele é
    if "cache_professores" not in st.session_state:
        st.session_state.cache_professores = listarProfessores()
    if "cache_turmas" not in st.session_state:
        st.session_state.cache_turmas = listarTurmasGeral()

    lista_professores = st.session_state.cache_professores
    lista_turmas_geral = st.session_state.cache_turmas

    with st.container(border=True):
        st.subheader("Filtro de Turma")
        with st.container(horizontal=True):
            professor_selecionado = st.selectbox(
                "Professor (Simulação de Login)",
                options=lista_professores if lista_professores else [],
                format_func=lambda p: p.pessoa.nome,
                index=None,
                placeholder="Identifique-se como professor...",
                key="diario_prof"
            )
            
            if professor_selecionado:
                turmas_filtradas = [t for t in lista_turmas_geral if t.professor_id == professor_selecionado.pessoa_id]
            else:
                turmas_filtradas = []

            turma_selecionada = st.selectbox(
                "Turma",
                options=turmas_filtradas,
                format_func=lambda t: f"{t.semestre} | {t.codigo} - {t.disciplina.nome}",
                index=None,
                placeholder="Selecione sua turma..." if professor_selecionado else "Selecione o Professor primeiro",
                disabled=not professor_selecionado,
                key="diario_turma"
            )

    st.write("")

    if turma_selecionada:
        # Busca a turma atualizada pelo ID (evita que o selectbox retenha um objeto antigo na memória)
        turma = next((t for t in lista_turmas_geral if t.id == turma_selecionada.id), None)
        if not turma:
            return
        
        matriculas = turma.matriculas

        if not matriculas:
            st.info("Nenhum aluno matriculado nesta turma ainda.")
        else:
            st.subheader(f"Lançamentos para {turma_selecionada.disciplina.nome}")
            
            # Montar a estrutura de dados para o data_editor
            original_data = []
            for matr in matriculas:
                # Determinar o status textual
                status = "Pendente"
                if matr.aprovacao is True: status = "Aprovado"
                elif matr.aprovacao is False: status = "Reprovado"
                
                aulas_totais = int(turma_selecionada.disciplina.carga_horaria * 0.75)

                original_data.append({
                    "ID Aluno": matr.aluno_id,
                    "Nome": matr.aluno.pessoa.nome,
                    "Nota 1": float(matr.nota1) if matr.nota1 is not None and matr.nota1 != -1 else None,
                    "Nota 2": float(matr.nota2) if matr.nota2 is not None and matr.nota2 != -1 else None,
                    "Nota 3": float(matr.nota3) if matr.nota3 is not None and matr.nota3 != -1 else None,
                    "Final": float(matr.final) if matr.final is not None and matr.final != -1 else None,
                    "Média": float(matr.media) if matr.media is not None and matr.media != -1 else None,
                    "Presenças": int(matr.frequencia_abs) if matr.frequencia_abs is not None else 0,
                    "Total Aulas": aulas_totais,
                    "Frequência %": f"{(matr.frequencia_rel * 100):.1f}%" if matr.frequencia_rel is not None else "0.0%",
                    "Situação": status,
                    "Adicionar Presenças": 0
                })

            st.caption("Dica: Você pode preencher as notas e presenças diretamente na tabela como se fosse no Excel.")
            
            # Exibe o editor de dados
            edited_data = st.data_editor(
                original_data,
                disabled=["ID Aluno", "Nome", "Média", "Presenças", "Total Aulas", "Frequência %", "Situação"],
                hide_index=True,
                width="stretch",
                column_config={
                    "ID Aluno": None, # Oculta a coluna
                    "Nota 1": st.column_config.NumberColumn(min_value=0.0, max_value=10.0, step=0.1, format="%.1f"),
                    "Nota 2": st.column_config.NumberColumn(min_value=0.0, max_value=10.0, step=0.1, format="%.1f"),
                    "Nota 3": st.column_config.NumberColumn(min_value=0.0, max_value=10.0, step=0.1, format="%.1f"),
                    "Final": st.column_config.NumberColumn(min_value=0.0, max_value=10.0, step=0.1, format="%.1f"),
                    "Média": st.column_config.NumberColumn(format="%.1f"),
                    "Adicionar Presenças": st.column_config.NumberColumn(min_value=0, max_value=100, step=1)
                },
                key=f"editor_turma_{turma_selecionada.id}_{st.session_state.form_key_diario}"
            )
            
            st.write("")
            c1, c2, c3 = st.columns([1, 1, 1])
            
            with c1:
                salvar = st.button("💾 Salvar Lançamentos", type="primary", width="stretch")
            
            with c3:
                fechar = st.button("🔒 Consolidar Turma", width="stretch", help="Calcula a situação final de todos os alunos e fecha a turma.")

            if salvar:
                try:
                    for orig, edit in zip(original_data, edited_data):
                        id_aluno = orig["ID Aluno"]
                        
                        if edit["Nota 1"] != orig["Nota 1"] and edit["Nota 1"] is not None:
                            lancarNota1(id_aluno, turma_selecionada.id, Decimal(str(edit["Nota 1"])))
                            
                        if edit["Nota 2"] != orig["Nota 2"] and edit["Nota 2"] is not None:
                            lancarNota2(id_aluno, turma_selecionada.id, Decimal(str(edit["Nota 2"])))
                            
                        if edit["Nota 3"] != orig["Nota 3"] and edit["Nota 3"] is not None:
                            lancarNota3(id_aluno, turma_selecionada.id, Decimal(str(edit["Nota 3"])))
                            
                        if edit["Final"] != orig["Final"] and edit["Final"] is not None:
                            lancarNotaFinal(id_aluno, turma_selecionada.id, Decimal(str(edit["Final"])))
                            
                        if edit.get("Adicionar Presenças", 0) > 0:
                            cadastrarPresenca(id_aluno, turma_selecionada.id, int(edit["Adicionar Presenças"]))
                    
                    st.session_state["diario_salvo"] = True
                    if "cache_turmas" in st.session_state:
                        del st.session_state["cache_turmas"]
                    st.session_state.form_key_diario += 1
                    st.rerun()

                except SQLAlchemyError as e:
                    st.error(f"Erro no banco de dados: {e}")
                except Exception as e:
                    st.error(f"Ocorreu um erro ao salvar: {e}")

            if fechar:
                try:
                    fecharTurma(turma_selecionada.id)
                    st.session_state["turma_fechada"] = True
                    if "cache_turmas" in st.session_state:
                        del st.session_state["cache_turmas"]
                    st.session_state.form_key_diario += 1
                    st.rerun()
                except SQLAlchemyError as e:
                    st.error(f"Erro no banco de dados: {e}")
                except Exception as e:
                    st.error(f"Ocorreu um erro ao consolidar a turma: {e}")
