import streamlit as st
import pandas as pd
from datetime import datetime
from database.entidades.enums.StatusBolsa import StatusBolsa
from modulos.academico.academico_service import listarBolsasGeral, editarBolsa

def telaGestaoBolsas():
    st.title("Gestão de Bolsas")
    st.caption("Consulte e edite as informações das bolsas concedidas aos alunos.")

    if st.session_state.pop("bolsas_salvas", False):
        st.toast("Alterações salvas com sucesso!", icon=":material/check:")

    if "cache_bolsas" not in st.session_state:
        st.session_state.cache_bolsas = listarBolsasGeral()
    
    lista_bolsas = st.session_state.cache_bolsas

    if not lista_bolsas:
        st.info("Nenhuma bolsa cadastrada no sistema.")
        return

    # Mapeamento
    dados_bolsas = []
    for b in lista_bolsas:
        try:
            nome_aluno = b.aluno.pessoa.nome
        except Exception:
            nome_aluno = f"ID: {b.aluno_id}"
            
        dados_bolsas.append({
            "ID Bolsa": b.id,
            "Aluno": nome_aluno,
            "Tipo": b.tipo_bolsa,
            "Desconto (%)": float(b.percentual_desconto * 100),
            "Início": b.data_inicio,
            "Término": b.data_fim,
            "Status": b.status.value
        })

    df_bolsas = pd.DataFrame(dados_bolsas)
    
    # Configurar colunas
    col_config = {
        "ID Bolsa": st.column_config.NumberColumn("ID", disabled=True),
        "Aluno": st.column_config.TextColumn("Aluno", disabled=True),
        "Tipo": st.column_config.TextColumn("Tipo", required=True),
        "Desconto (%)": st.column_config.NumberColumn(
            "Desconto (%)", 
            min_value=1.0, max_value=100.0, step=1.0, required=True
        ),
        "Início": st.column_config.DateColumn("Início", disabled=True),
        "Término": st.column_config.DateColumn("Término", required=True),
        "Status": st.column_config.SelectboxColumn(
            "Status", 
            options=[s.value for s in StatusBolsa], 
            required=True
        )
    }

    st.dataframe(
        df_bolsas,
        column_config=col_config,
        width="stretch",
        hide_index=True
    )

    st.write("---")
    
    with st.container():
        st.subheader("Edição de Bolsa")

        bolsa_selecionada = st.selectbox(
            "Selecione a Bolsa",
            options=lista_bolsas,
            format_func=lambda b: f"Bolsa {b.id} - Aluno: {b.aluno.pessoa.nome if hasattr(b.aluno, 'pessoa') else b.aluno_id} ({b.tipo_bolsa})",
            index=None,
            placeholder="Escolha uma bolsa..."
        )

        if bolsa_selecionada:
            bolsa = next((b for b in lista_bolsas if b.id == bolsa_selecionada.id), None)
            if bolsa:
                with st.form(key="form_edicao_bolsa", border=False):
                    with st.container(horizontal=True):
                        novo_tipo = st.text_input("Tipo de Bolsa *", value=bolsa.tipo_bolsa)
                        novo_perc = st.number_input(
                            "Percentual de Desconto (%) *",
                            min_value=1,
                            max_value=100,
                            step=1,
                            format="%d",
                            value=int(bolsa.percentual_desconto * 100),
                            help="Digite um valor de 1 a 100."
                        )

                    with st.container(horizontal=True):
                        novo_fim = st.date_input("Data de Término *", value=bolsa.data_fim, format="DD/MM/YYYY")
                        
                        # Pegar índice do status atual para o selectbox
                        status_list = list(StatusBolsa)
                        status_index = status_list.index(bolsa.status) if bolsa.status in status_list else 0
                        
                        novo_status = st.selectbox(
                            "Status da Bolsa *",
                            options=status_list,
                            index=status_index,
                            format_func=lambda s: s.value
                        )
                    
                    st.write("")
                    
                    _, centro, _ = st.columns([2, 3, 2])
                    with centro:
                        if st.form_submit_button("Salvar Alterações", type="primary", width="stretch"):
                            try:
                                editarBolsa(
                                    idBolsa=bolsa.id,
                                    tipo_bolsa=novo_tipo.strip(),
                                    percentual_desconto=float(novo_perc) / 100.0,
                                    data_fim=novo_fim,
                                    status=novo_status
                                )
                                st.session_state.bolsas_salvas = True
                                if "cache_bolsas" in st.session_state:
                                    del st.session_state["cache_bolsas"]
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao salvar: {e}")
