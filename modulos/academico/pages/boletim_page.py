import streamlit as st
import pandas as pd
from modulos.academico.academico_service import listarAlunoId

def telaBoletim():
    st.title(":material/school: Meu Boletim")
    st.caption("Acompanhe o seu desempenho acadêmico, notas e frequências.")

    pessoa_id = st.session_state.get("pessoa_id")
    
    if not pessoa_id:
        st.error("Erro na identificação do usuário. Por favor, refaça o login.")
        return

    # Buscar dados do aluno
    aluno = listarAlunoId(pessoa_id)

    if not aluno:
        st.error("Nenhum vínculo de Aluno encontrado para este usuário.")
        return

    # Informações Rápidas do Aluno
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Média Geral", value=f"{float(aluno.media_geral):.2f}" if aluno.media_geral else "-")
    with col2:
        st.metric(label="Coeficiente de Rendimento", value=f"{float(aluno.coef_rend):.2f}" if aluno.coef_rend else "-")
    with col3:
        st.metric(label="RA (Registro)", value=aluno.matricula)
    
    st.write("---")

    matriculas = aluno.matriculas

    if not matriculas:
        st.info("Você ainda não está matriculado em nenhuma disciplina.", icon=":material/info:")
        return

    # Processar matriculas para exibição
    dados_boletim = []
    
    for matr in matriculas:
        # Determinar status em texto amigável
        status = "Pendente"
        if matr.aprovacao is True: status = "Aprovado"
        elif matr.aprovacao is False: status = "Reprovado"

        # Calcular Aulas Totais da disciplina
        aulas_totais = int(matr.disciplina.carga_horaria * 0.75) if matr.disciplina else 0
        
        # Frequencia Relativa (0 a 1) -> Porcentagem (0 a 100)
        freq_rel_percent = float(matr.frequencia_rel) * 100 if matr.frequencia_rel is not None else 0.0

        dados_boletim.append({
            "Semestre": matr.turma.semestre if hasattr(matr, 'turma') and matr.turma else "-",
            "Disciplina": matr.disciplina.nome if matr.disciplina else "-",
            "Nota 1": float(matr.nota1) if matr.nota1 is not None and matr.nota1 != -1 else None,
            "Nota 2": float(matr.nota2) if matr.nota2 is not None and matr.nota2 != -1 else None,
            "Nota 3": float(matr.nota3) if matr.nota3 is not None and matr.nota3 != -1 else None,
            "Final": float(matr.final) if matr.final is not None and matr.final != -1 else None,
            "Média": float(matr.media) if matr.media is not None and matr.media != -1 else None,
            "Faltas": int(matr.frequencia_abs) if matr.frequencia_abs is not None else 0,
            "Frequência (%)": freq_rel_percent,
            "Situação": status
        })

    df_boletim = pd.DataFrame(dados_boletim)

    # Ordenar por Semestre e Disciplina (assumindo que o formato do semestre permite ordenação, ex: 2026.1)
    df_boletim = df_boletim.sort_values(by=["Semestre", "Disciplina"])

    # Configuração das Colunas no DataFrame
    col_config = {
        "Semestre": st.column_config.TextColumn("Semestre"),
        "Disciplina": st.column_config.TextColumn("Disciplina"),
        "Nota 1": st.column_config.NumberColumn("N1", format="%.1f"),
        "Nota 2": st.column_config.NumberColumn("N2", format="%.1f"),
        "Nota 3": st.column_config.NumberColumn("N3", format="%.1f"),
        "Final": st.column_config.NumberColumn("Final", format="%.1f"),
        "Média": st.column_config.NumberColumn("Média", format="%.1f"),
        "Faltas": st.column_config.NumberColumn("Presenças"), 
        # (Nota interna: no Diário chamamos de Frequencia Absoluta que é o número de presenças contabilizadas. 
        # Mas para o aluno podemos exibir como Presenças ou o valor direto)
        "Frequência (%)": st.column_config.NumberColumn("Frequência", format="%.1f%%"),
        "Situação": st.column_config.TextColumn("Situação")
    }

    # Como você prefere formulários e visualizações em containers sem bordas (flat design),
    # o dataframe ficará solto, utilizando todo o espaço horizontal.
    with st.container():
        st.subheader(":material/list_alt: Histórico de Disciplinas")
        
        st.dataframe(
            df_boletim,
            column_config=col_config,
            use_container_width=True,
            hide_index=True
        )
