import pandas as pd
import streamlit as st
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from modulos.cadastros.mensalidade import criarMensalidades
from modulos.financeiro.financeiro_service import (definirDataPagamentoContaPagar, definirDataPagamentoContaReceber, definirFinanceiroContaReceber, listarContasPagar, listarContasReceber, listarFinanceiroId)
from modulos.utils.financeiro_visual import (aplicarEstiloGestaoFinanceira, marcarMetricasPagina, marcarTabelaPagina, painelPagina, renderizarDivisorPagina, renderizarSecaoPagina, renderizarTopoPagina)

# Função para formatar valores monetários no padrão brasileiro
def formatarMoeda(valor):
    return (
        f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

# Função para renderizar a tabela de contas a receber
def renderizarTabelaReceber(contas, historico=False):
    if historico:
        dados = [
            {
                "ID": conta.id,
                "Aluno": (
                    conta.mensalidade.aluno.pessoa.nome
                    if hasattr(conta, "mensalidade") and conta.mensalidade
                    else "-"
                ),
                "Referência": (
                    conta.mensalidade.data_inicio.strftime("%m/%Y")
                    if hasattr(conta, "mensalidade") and conta.mensalidade
                    else "-"
                ),
                "Vencimento": conta.data_vencimento,
                "Data do pagamento": conta.data_pagamento,
                "Responsável": (
                    conta.financeiro.pessoa.nome if conta.financeiro else "-"
                ),
                "Valor pago": float(conta.valor),
            }
            for conta in contas
        ]

        configuracao = {
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Aluno": st.column_config.TextColumn("Aluno", width="medium"),
            "Referência": st.column_config.TextColumn("Referência", width="small"),
            "Vencimento": st.column_config.DateColumn(
                "Vencimento", format="DD/MM/YYYY"
            ),
            "Data do pagamento": st.column_config.DateColumn(
                "Pagamento",
                format="DD/MM/YYYY",
            ),
            "Responsável": st.column_config.TextColumn("Responsável", width="medium"),
            "Valor pago": st.column_config.NumberColumn(
                "Valor pago",
                format="R$ %.2f",
            ),
        }
    else:
        dados = [
            {
                "ID": conta.id,
                "Aluno": (
                    conta.mensalidade.aluno.pessoa.nome
                    if hasattr(conta, "mensalidade") and conta.mensalidade
                    else "-"
                ),
                "Referência": (
                    conta.mensalidade.data_inicio.strftime("%m/%Y")
                    if hasattr(conta, "mensalidade") and conta.mensalidade
                    else "-"
                ),
                "Vencimento": conta.data_vencimento,
                "Valor": float(conta.valor),
            }
            for conta in contas
        ]

        configuracao = {
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Aluno": st.column_config.TextColumn("Aluno", width="large"),
            "Referência": st.column_config.TextColumn("Referência", width="small"),
            "Vencimento": st.column_config.DateColumn(
                "Vencimento", format="DD/MM/YYYY"
            ),
            "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
        }

    marcarTabelaPagina()
    st.dataframe(
        pd.DataFrame(dados),
        column_config=configuracao,
        width="stretch",
        hide_index=True,
    )

# Função para renderizar a tabela de contas a pagar
def renderizarTabelaPagar(contas, historico=False):
    if historico:
        dados = [
            {
                "ID": conta.id,
                "Produto": (
                    conta.compra.produto.nome
                    if hasattr(conta, "compra")
                    and conta.compra
                    and conta.compra.produto
                    else "-"
                ),
                "Fornecedor": (
                    conta.compra.fornecedor.nome
                    if hasattr(conta, "compra") and conta.compra
                    else "-"
                ),
                "Vencimento": conta.data_vencimento,
                "Data do pagamento": conta.data_pagamento,
                "Valor pago": float(conta.valor),
            }
            for conta in contas
        ]

        configuracao = {
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Produto": st.column_config.TextColumn("Produto", width="large"),
            "Fornecedor": st.column_config.TextColumn("Fornecedor", width="medium"),
            "Vencimento": st.column_config.DateColumn(
                "Vencimento", format="DD/MM/YYYY"
            ),
            "Data do pagamento": st.column_config.DateColumn(
                "Pagamento",
                format="DD/MM/YYYY",
            ),
            "Valor pago": st.column_config.NumberColumn(
                "Valor pago",
                format="R$ %.2f",
            ),
        }
    else:
        dados = [
            {
                "ID": conta.id,
                "Produto": (
                    conta.compra.produto.nome
                    if hasattr(conta, "compra")
                    and conta.compra
                    and conta.compra.produto
                    else "-"
                ),
                "Fornecedor": (
                    conta.compra.fornecedor.nome
                    if hasattr(conta, "compra") and conta.compra
                    else "-"
                ),
                "Vencimento": conta.data_vencimento,
                "Valor": float(conta.valor),
            }
            for conta in contas
        ]

        configuracao = {
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Produto": st.column_config.TextColumn("Produto", width="large"),
            "Fornecedor": st.column_config.TextColumn("Fornecedor", width="medium"),
            "Vencimento": st.column_config.DateColumn(
                "Vencimento", format="DD/MM/YYYY"
            ),
            "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
        }

    marcarTabelaPagina()
    st.dataframe(
        pd.DataFrame(dados),
        column_config=configuracao,
        width="stretch",
        hide_index=True,
    )

# Função principal para renderizar a tela de gestão financeira
def telaGestaoFinanceira():
    aplicarEstiloGestaoFinanceira()

    renderizarTopoPagina(
        titulo="Gestão financeira",
        descricao=(
            "Acompanhe o fluxo de caixa, contas pendentes e pagamentos "
            "vinculados ao campus."
        ),
        categoria="GESTÃO FINANCEIRA",
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

    st.html(f"""
        <div class="gf-campus-context">
            <span class="gf-campus-dot"></span>
            Caixa em operação · {campus.nome}
        </div>
        """)

    todas_receber = [
        conta for conta in listarContasReceber() if conta.caixa_id == caixa.id
    ]
    todas_pagar = [conta for conta in listarContasPagar() if conta.caixa_id == caixa.id]

    receber_pendentes = [
        conta for conta in todas_receber if conta.data_pagamento is None
    ]
    receber_pagas = [
        conta for conta in todas_receber if conta.data_pagamento is not None
    ]

    pagar_pendentes = [conta for conta in todas_pagar if conta.data_pagamento is None]
    pagar_pagas = [conta for conta in todas_pagar if conta.data_pagamento is not None]

    total_receber = sum(conta.valor for conta in receber_pendentes)
    total_pagar = sum(conta.valor for conta in pagar_pendentes)

    with painelPagina(
        titulo="Visão geral do caixa",
        descricao=(
            "Resumo financeiro das movimentações pendentes e do saldo "
            "disponível no campus."
        ),
        contexto="RESUMO FINANCEIRO",
    ):
        colSaldo, colReceber, colPagar = st.columns(3)

        with colSaldo:
            marcarMetricasPagina()
            st.metric(
                "Saldo em caixa",
                formatarMoeda(caixa.valor_caixa),
            )

        with colReceber:
            st.metric(
                "Total a receber",
                formatarMoeda(total_receber),
                delta=f"{len(receber_pendentes)} pendente(s)",
                delta_color="off",
            )

        with colPagar:
            st.metric(
                "Total a pagar",
                formatarMoeda(total_pagar),
                delta=f"{len(pagar_pendentes)} pendente(s)",
                delta_color="off",
            )

    tabReceber, tabPagar, tabAjustes = st.tabs(
        [
            ":material/arrow_downward: Contas a receber",
            ":material/arrow_upward: Contas a pagar",
            ":material/tune: Ajustes manuais",
        ]
    )

    with tabReceber:
        if st.session_state.pop("baixa_receber_realizada", False):
            st.toast(
                "Pagamento recebido e caixa atualizado!",
                icon=":material/check:",
            )

        with painelPagina(
            titulo="Contas a receber",
            descricao=(
                "Acompanhe mensalidades pendentes e consulte os pagamentos "
                "já registrados."
            ),
            contexto="ENTRADAS",
        ):
            opcaoReceber = st.segmented_control(
                "Visualização",
                options=["Pendentes", "Histórico"],
                default="Pendentes",
                key="seg_rec",
                width="stretch",
            )

            renderizarDivisorPagina()

            if opcaoReceber == "Pendentes":
                renderizarSecaoPagina(
                    numero=1,
                    titulo="Pendências de recebimento",
                    descricao="Valores aguardando confirmação de pagamento.",
                )

                if not receber_pendentes:
                    st.info(
                        "Nenhuma conta a receber pendente neste caixa.",
                        icon=":material/check_circle:",
                    )
                else:
                    renderizarTabelaReceber(receber_pendentes)

                    renderizarDivisorPagina()
                    renderizarSecaoPagina(
                        numero=2,
                        titulo="Registrar recebimento",
                        descricao=(
                            "Selecione uma conta e informe a data efetiva "
                            "do pagamento."
                        ),
                    )

                    with st.form("form_baixa_receber", border=False):
                        colConta, colData = st.columns([3, 2])

                        with colConta:
                            conta_rec_selecionada = st.selectbox(
                                "Conta a receber",
                                options=receber_pendentes,
                                format_func=lambda conta: (
                                    f"#{conta.id} · {formatarMoeda(conta.valor)} · "
                                    f"Venc. {conta.data_vencimento.strftime('%d/%m/%Y')}"
                                ),
                            )

                        with colData:
                            data_pagamento_rec = st.date_input(
                                "Data do pagamento",
                                value=date.today(),
                                key="data_rec",
                            )

                        _, colunaBotao = st.columns([3.5, 2])

                        with colunaBotao:
                            submit_rec = st.form_submit_button(
                                "Confirmar recebimento",
                                type="primary",
                                icon=":material/check:",
                                width="stretch",
                            )

                    if submit_rec:
                        if conta_rec_selecionada:
                            try:
                                definirDataPagamentoContaReceber(
                                    conta_rec_selecionada.id,
                                    data_pagamento_rec,
                                )
                                definirFinanceiroContaReceber(
                                    conta_rec_selecionada.id,
                                    financeiro.pessoa_id,
                                )
                                st.session_state["baixa_receber_realizada"] = True
                                st.rerun()
                            except SQLAlchemyError as erro:
                                st.error(f"Erro de banco de dados: {erro}")
                            except Exception as erro:
                                st.error(str(erro))
                        else:
                            st.error("Nenhuma conta selecionada.")

            elif opcaoReceber == "Histórico":
                renderizarSecaoPagina(
                    numero=1,
                    titulo="Histórico de recebimentos",
                    descricao="Pagamentos já confirmados e creditados no caixa.",
                )

                if not receber_pagas:
                    st.info(
                        "Nenhum histórico de conta recebida.",
                        icon=":material/info:",
                    )
                else:
                    renderizarTabelaReceber(receber_pagas, historico=True)

    with tabPagar:
        if st.session_state.pop("baixa_pagar_realizada", False):
            st.toast(
                "Pagamento efetuado e caixa atualizado!",
                icon=":material/check:",
            )

        with painelPagina(
            titulo="Contas a pagar",
            descricao=(
                "Controle as despesas pendentes do campus e consulte os "
                "pagamentos concluídos."
            ),
            contexto="SAÍDAS",
        ):
            opcaoPagar = st.segmented_control(
                "Visualização",
                options=["Pendentes", "Histórico"],
                default="Pendentes",
                key="seg_pag",
                width="stretch",
            )

            renderizarDivisorPagina()

            if opcaoPagar == "Pendentes":
                renderizarSecaoPagina(
                    numero=1,
                    titulo="Pendências de pagamento",
                    descricao="Compras e compromissos aguardando quitação.",
                )

                if not pagar_pendentes:
                    st.info(
                        "Nenhuma conta a pagar pendente neste caixa.",
                        icon=":material/check_circle:",
                    )
                else:
                    renderizarTabelaPagar(pagar_pendentes)

                    renderizarDivisorPagina()
                    renderizarSecaoPagina(
                        numero=2,
                        titulo="Registrar pagamento",
                        descricao=(
                            "Selecione uma conta e informe a data em que "
                            "o pagamento foi realizado."
                        ),
                    )

                    with st.form("form_baixa_pagar", border=False):
                        colConta, colData, colAcao = st.columns(
                            [3.3, 2.1, 1.8],
                            vertical_alignment="bottom",
                        )

                        with colConta:
                            conta_pag_selecionada = st.selectbox(
                                "Conta a pagar",
                                options=pagar_pendentes,
                                format_func=lambda conta: (
                                    f"#{conta.id} · {formatarMoeda(conta.valor)} · "
                                    f"Venc. {conta.data_vencimento.strftime('%d/%m/%Y')}"
                                ),
                            )

                        with colData:
                            data_pagamento_pag = st.date_input(
                                "Data do pagamento",
                                value=date.today(),
                                format="DD/MM/YYYY",
                                key="data_pag",
                            )

                        with colAcao:
                            submit_pag = st.form_submit_button(
                                "Confirmar",
                                type="secondary",
                                icon=":material/check:",
                                width="stretch",
                            )

                    if submit_pag:
                        if conta_pag_selecionada:
                            try:
                                definirDataPagamentoContaPagar(
                                    conta_pag_selecionada.id,
                                    data_pagamento_pag,
                                )
                                st.session_state["baixa_pagar_realizada"] = True
                                st.rerun()
                            except SQLAlchemyError as erro:
                                st.error(f"Erro de banco de dados: {erro}")
                            except Exception as erro:
                                st.error(str(erro))
                        else:
                            st.error("Nenhuma conta selecionada.")

            elif opcaoPagar == "Histórico":
                renderizarSecaoPagina(
                    numero=1,
                    titulo="Histórico de pagamentos",
                    descricao="Despesas já quitadas e registradas no caixa.",
                )

                if not pagar_pagas:
                    st.info(
                        "Nenhum histórico de conta paga.",
                        icon=":material/info:",
                    )
                else:
                    renderizarTabelaPagar(pagar_pagas, historico=True)

    with tabAjustes:
        with painelPagina(
            titulo="Ajustes manuais",
            descricao=(
                "Ações administrativas que afetam a rotina financeira do sistema."
            ),
            contexto="ADMINISTRAÇÃO",
        ):
            renderizarSecaoPagina(
                numero=1,
                titulo="Gerar mensalidades",
                descricao=(
                    "Gere manualmente as mensalidades de todos os alunos quando "
                    "for necessário antecipar ou repetir a rotina automática."
                ),
            )

            st.info(
                "A geração já ocorre automaticamente no dia 1 de cada mês. "
                "Use esta ação somente quando necessário.",
                icon=":material/info:",
            )

            _, colunaAcao = st.columns([3.5, 2])

            with colunaAcao:
                gerarMensalidades = st.button(
                    "Gerar mensalidades agora",
                    type="primary",
                    icon=":material/autorenew:",
                    width="stretch",
                    key="btn_gerar_mensalidades_manual",
                )

            if gerarMensalidades:
                with st.spinner("Gerando mensalidades..."):
                    try:
                        criarMensalidades()
                        st.success("Mensalidades geradas com sucesso!")
                        import time

                        time.sleep(1.5)
                        st.rerun()
                    except Exception as erro:
                        st.error(f"Erro ao gerar mensalidades: {erro}")
