import streamlit as st
import pandas as pd
from modulos.academico.academico_service import listarMensalidadesAluno, listarBolsasAluno

def telaFinanceiroAluno():
    st.title(":material/payments: Meu Financeiro")
    st.caption("Acompanhe o histórico de suas mensalidades e bolsas estudantis.")
    
    pessoa_id = st.session_state.get("pessoa_id")
    
    if not pessoa_id:
        st.error("Erro na identificação do usuário. Por favor, refaça o login.")
        return

    # Buscar dados do aluno
    mensalidades = listarMensalidadesAluno(pessoa_id)
    bolsas = listarBolsasAluno(pessoa_id)

    st.write("---")

    # Módulo de Bolsas
    st.subheader(":material/account_balance: Minhas Bolsas")
    
    if not bolsas:
        st.info("Nenhuma bolsa vinculada ao seu histórico acadêmico no momento.", icon=":material/info:")
    else:
        dados_bolsas = []
        for bolsa in bolsas:
            dados_bolsas.append({
                "Tipo": bolsa.tipo_bolsa,
                "Desconto (%)": float(bolsa.percentual_desconto * 100),
                "Início": bolsa.data_inicio,
                "Término": bolsa.data_fim,
                "Status": bolsa.status.value
            })

        df_bolsas = pd.DataFrame(dados_bolsas)
        
        # Ordenar por status (ativas primeiro) e data_inicio
        df_bolsas = df_bolsas.sort_values(by=["Status", "Início"])

        col_config_bolsas = {
            "Tipo": st.column_config.TextColumn("Tipo de Bolsa"),
            "Desconto (%)": st.column_config.NumberColumn("Desconto", format="%.0f%%"),
            "Início": st.column_config.DateColumn("Data Inicial", format="DD/MM/YYYY"),
            "Término": st.column_config.DateColumn("Validade (Término)", format="DD/MM/YYYY"),
            "Status": st.column_config.TextColumn("Situação")
        }

        with st.container():
            st.dataframe(
                df_bolsas,
                column_config=col_config_bolsas,
                use_container_width=True,
                hide_index=True
            )

    st.write("---")

    # Módulo de Mensalidades
    st.subheader(":material/receipt_long: Histórico de Mensalidades")
    
    if not mensalidades:
        st.info("Nenhum registro de mensalidade encontrado.", icon=":material/info:")
    else:
        dados_mensalidades = []
        for m in mensalidades:
            referencia = m.data_inicio.strftime("%m/%Y")
            situacao = "Paga" if m.foi_paga else "Pendente"
            
            dados_mensalidades.append({
                "Referência": referencia,
                "Vencimento": m.data_vencimento,
                "Valor Base (R$)": float(m.valor),
                "Situação": situacao
            })

        df_mensalidades = pd.DataFrame(dados_mensalidades)
        
        # Ordenar por vencimento decrescente (mais recentes primeiro)
        df_mensalidades = df_mensalidades.sort_values(by=["Vencimento"], ascending=False)

        col_config_mensalidades = {
            "Referência": st.column_config.TextColumn("Referência (Mês/Ano)"),
            "Vencimento": st.column_config.DateColumn("Vencimento", format="DD/MM/YYYY"),
            "Valor Base (R$)": st.column_config.NumberColumn("Valor Total", format="R$ %.2f"),
            "Situação": st.column_config.TextColumn("Situação do Pagamento")
        }

        with st.container():
            st.dataframe(
                df_mensalidades,
                column_config=col_config_mensalidades,
                use_container_width=True,
                hide_index=True
            )
