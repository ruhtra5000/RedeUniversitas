import streamlit as st
import pandas as pd
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from modulos.financeiro.financeiro_service import (
    listarFinanceiroId, 
    listarContasReceber, 
    listarContasPagar,
    definirDataPagamentoContaReceber,
    definirDataPagamentoContaPagar,
    definirFinanceiroContaReceber,
)

def telaGestaoFinanceira():
    st.title(":material/account_balance: Gestão Financeira")
    st.caption("Controle de fluxo de caixa, mensalidades e pagamentos de compras do campus.")
    
    st.markdown(
        """
        <style>
        input[type=number]::-webkit-inner-spin-button, 
        input[type=number]::-webkit-outer-spin-button { 
            -webkit-appearance: none; 
            margin: 0; 
        }
        input[type=number] {
            -moz-appearance: textfield;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    pessoa_id = st.session_state.get("pessoa_id")
    
    if not pessoa_id:
        st.error("Sessão inválida. Por favor, refaça o login.")
        return

    financeiro = listarFinanceiroId(pessoa_id)

    if not financeiro:
        st.error("Perfil financeiro não encontrado para este usuário.")
        return

    campus = financeiro.campus
    caixa = campus.caixa

    if not caixa:
        st.error(f"Nenhum caixa associado ao campus {campus.nome}. Consulte o Reitor.")
        return

    st.write("---")

    # Carregar Dados Filtrados por Caixa
    todas_receber = [c for c in listarContasReceber() if c.caixa_id == caixa.id]
    todas_pagar = [c for c in listarContasPagar() if c.caixa_id == caixa.id]

    receber_pendentes = [c for c in todas_receber if c.data_pagamento is None]
    receber_pagas = [c for c in todas_receber if c.data_pagamento is not None]

    pagar_pendentes = [c for c in todas_pagar if c.data_pagamento is None]
    pagar_pagas = [c for c in todas_pagar if c.data_pagamento is not None]

    # Métrica: Saldo em Caixa
    col1, col2, col3 = st.columns(3)
    
    val_caixa_str = f"R$ {float(caixa.valor_caixa):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    with col1:
        st.caption(f":material/account_balance_wallet: Saldo em Caixa ({campus.nome})")
        st.subheader(val_caixa_str)
        
    total_receber = sum([c.valor for c in receber_pendentes])
    val_receber_str = f"R$ {float(total_receber):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    with col2:
        st.caption(":material/arrow_downward: Total a Receber (Pendente)")
        st.subheader(f":green[{val_receber_str}]")
        
    total_pagar = sum([c.valor for c in pagar_pendentes])
    val_pagar_str = f"R$ {float(total_pagar):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    with col3:
        st.caption(":material/arrow_upward: Total a Pagar (Pendente)")
        st.subheader(f":red[{val_pagar_str}]")


    st.write("")

    # Abas Principais
    tab_receber, tab_pagar, tab_ajustes = st.tabs([":material/input: Contas a Receber", ":material/output: Contas a Pagar", ":material/tune: Ajustes Manuais"])

    # ====== ABA CONTAS A RECEBER ======
    with tab_receber:
        if st.session_state.pop("baixa_receber_realizada", False):
            st.toast("Pagamento recebido e caixa atualizado!", icon=":material/check:")
            
        opcao_receber = st.radio("Selecione a visão:", [":material/pending_actions: Pendentes", ":material/history: Histórico de Pagamentos"], horizontal=True, key="rad_rec")
        
        if opcao_receber == ":material/pending_actions: Pendentes":
            if not receber_pendentes:
                st.info("Nenhuma conta a receber pendente neste caixa.", icon=":material/info:")
            else:
                # Tabela de visualização
                df_rec = pd.DataFrame([{
                    "ID": c.id,
                    "Aluno": c.mensalidade.aluno.pessoa.nome if hasattr(c, 'mensalidade') and c.mensalidade else "-",
                    "Referência": c.mensalidade.data_inicio.strftime("%m/%Y") if hasattr(c, 'mensalidade') and c.mensalidade else "-",
                    "Vencimento": c.data_vencimento.strftime("%d/%m/%Y"),
                    "Valor": f"R$ {float(c.valor):.2f}"
                } for c in receber_pendentes])
                
                st.dataframe(df_rec, use_container_width=True, hide_index=True)
                
                st.write("")
                with st.container():
                    st.subheader(":material/payments: Registrar Pagamento")
                    with st.form("form_baixa_receber", border=False):
                        col_r1, col_r2 = st.columns(2)
                        with col_r1:
                            conta_rec_selecionada = st.selectbox(
                                "Selecione a Conta a Receber",
                                options=receber_pendentes,
                                format_func=lambda c: f"ID: {c.id} - R$ {float(c.valor):.2f} (Venc: {c.data_vencimento.strftime('%d/%m/%Y')})"
                            )
                        with col_r2:
                            data_pagamento_rec = st.date_input("Data Efetiva do Pagamento", value=date.today(), key="data_rec")
                            
                        submit_rec = st.form_submit_button("Confirmar Baixa", type="primary")
                        
                        if submit_rec:
                            if conta_rec_selecionada:
                                try:
                                    definirDataPagamentoContaReceber(conta_rec_selecionada.id, data_pagamento_rec)
                                    # Atribuir quem efetuou a baixa
                                    definirFinanceiroContaReceber(conta_rec_selecionada.id, financeiro.pessoa_id)
                                    st.session_state["baixa_receber_realizada"] = True
                                    st.rerun()
                                except SQLAlchemyError as e:
                                    st.error(f"Erro de banco de dados: {e}")
                                except Exception as e:
                                    st.error(str(e))
                            else:
                                st.error("Nenhuma conta selecionada.")

        elif opcao_receber == ":material/history: Histórico de Pagamentos":
            if not receber_pagas:
                st.info("Nenhum histórico de conta recebida.", icon=":material/info:")
            else:
                df_rec_pagas = pd.DataFrame([{
                    "ID": c.id,
                    "Aluno": c.mensalidade.aluno.pessoa.nome if hasattr(c, 'mensalidade') and c.mensalidade else "-",
                    "Referência": c.mensalidade.data_inicio.strftime("%m/%Y") if hasattr(c, 'mensalidade') and c.mensalidade else "-",
                    "Vencimento": c.data_vencimento.strftime("%d/%m/%Y"),
                    "Data Pagamento": c.data_pagamento.strftime("%d/%m/%Y"),
                    "Responsável": c.financeiro.pessoa.nome if c.financeiro else "-",
                    "Valor Pago": f"R$ {float(c.valor):.2f}"
                } for c in receber_pagas])
                st.dataframe(df_rec_pagas, use_container_width=True, hide_index=True)


    # ====== ABA CONTAS A PAGAR ======
    with tab_pagar:
        if st.session_state.pop("baixa_pagar_realizada", False):
            st.toast("Pagamento efetuado e caixa atualizado!", icon=":material/check:")

        opcao_pagar = st.radio("Selecione a visão:", [":material/pending_actions: Pendentes", ":material/history: Histórico de Pagamentos"], horizontal=True, key="rad_pag")
        
        if opcao_pagar == ":material/pending_actions: Pendentes":
            if not pagar_pendentes:
                st.info("Nenhuma conta a pagar pendente neste caixa.", icon=":material/info:")
            else:
                df_pag = pd.DataFrame([{
                    "ID": c.id,
                    "Produto": c.compra.produto.nome if hasattr(c, 'compra') and c.compra and c.compra.produto else "-",
                    "Fornecedor": c.compra.fornecedor.nome if hasattr(c, 'compra') and c.compra else "-",
                    "Vencimento": c.data_vencimento.strftime("%d/%m/%Y"),
                    "Valor": f"R$ {float(c.valor):.2f}"
                } for c in pagar_pendentes])
                
                st.dataframe(df_pag, use_container_width=True, hide_index=True)
                
                st.write("")
                with st.container():
                    st.subheader(":material/payments: Registrar Pagamento")
                    with st.form("form_baixa_pagar", border=False):
                        col_p1, col_p2 = st.columns(2)
                        with col_p1:
                            conta_pag_selecionada = st.selectbox(
                                "Selecione a Conta a Pagar",
                                options=pagar_pendentes,
                                format_func=lambda c: f"ID: {c.id} - R$ {float(c.valor):.2f} (Venc: {c.data_vencimento.strftime('%d/%m/%Y')})"
                            )
                        with col_p2:
                            data_pagamento_pag = st.date_input("Data Efetiva do Pagamento", value=date.today(), key="data_pag")
                            
                        submit_pag = st.form_submit_button("Confirmar Baixa", type="primary")
                        
                        if submit_pag:
                            if conta_pag_selecionada:
                                try:
                                    definirDataPagamentoContaPagar(conta_pag_selecionada.id, data_pagamento_pag)
                                    st.session_state["baixa_pagar_realizada"] = True
                                    st.rerun()
                                except SQLAlchemyError as e:
                                    st.error(f"Erro de banco de dados: {e}")
                                except Exception as e:
                                    st.error(str(e))
                            else:
                                st.error("Nenhuma conta selecionada.")
        
        elif opcao_pagar == ":material/history: Histórico de Pagamentos":
            if not pagar_pagas:
                st.info("Nenhum histórico de conta paga.", icon=":material/info:")
            else:
                df_pag_pagas = pd.DataFrame([{
                    "ID": c.id,
                    "Produto": c.compra.produto.nome if hasattr(c, 'compra') and c.compra and c.compra.produto else "-",
                    "Fornecedor": c.compra.fornecedor.nome if hasattr(c, 'compra') and c.compra else "-",
                    "Vencimento": c.data_vencimento.strftime("%d/%m/%Y"),
                    "Data Pagamento": c.data_pagamento.strftime("%d/%m/%Y"),
                    "Valor Pago": f"R$ {float(c.valor):.2f}"
                } for c in pagar_pagas])
                st.dataframe(df_pag_pagas, use_container_width=True, hide_index=True)