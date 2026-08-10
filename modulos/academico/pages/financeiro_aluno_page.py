import pandas as pd
import streamlit as st
from modulos.academico.academico_service import (listarBolsasAluno, listarMensalidadesAluno)
from modulos.utils.academico_visual import (marcarTabelaPagina, painelPagina, renderizarTopoPagina)

# Tela de financeiro do aluno
def telaFinanceiroAluno():
    renderizarTopoPagina(
        titulo="Meu financeiro",
        descricao=(
            "Acompanhe suas mensalidades e os benefícios "
            "acadêmicos vinculados ao seu histórico."
        ),
        categoria="PORTAL DO ALUNO",
    )

    pessoa_id = st.session_state.get("pessoa_id")

    if not pessoa_id:
        st.error("Erro na identificação do usuário. " "Por favor, refaça o login.")
        return

    mensalidades = listarMensalidadesAluno(pessoa_id)
    bolsas = listarBolsasAluno(pessoa_id)

    with painelPagina(
        titulo="Minhas bolsas",
        descricao="Benefícios e descontos vinculados ao seu cadastro.",
        contexto="BENEFÍCIOS",
    ):
        if not bolsas:
            st.info(
                "Nenhuma bolsa está vinculada ao seu histórico acadêmico.",
                icon=":material/info:",
            )

        else:
            dadosBolsas = [
                {
                    "Tipo": bolsa.tipo_bolsa,
                    "Desconto (%)": float(bolsa.percentual_desconto * 100),
                    "Início": bolsa.data_inicio,
                    "Término": bolsa.data_fim,
                    "Status": bolsa.status.value,
                }
                for bolsa in bolsas
            ]

            tabelaBolsas = pd.DataFrame(dadosBolsas).sort_values(
                by=["Status", "Início"]
            )

            configuracaoBolsas = {
                "Tipo": st.column_config.TextColumn("Tipo de bolsa"),
                "Desconto (%)": st.column_config.NumberColumn(
                    "Desconto",
                    format="%.0f%%",
                ),
                "Início": st.column_config.DateColumn(
                    "Data inicial",
                    format="DD/MM/YYYY",
                ),
                "Término": st.column_config.DateColumn(
                    "Validade",
                    format="DD/MM/YYYY",
                ),
                "Status": st.column_config.TextColumn("Situação"),
            }

            marcarTabelaPagina()

            st.dataframe(
                tabelaBolsas,
                column_config=configuracaoBolsas,
                width="stretch",
                hide_index=True,
            )

    with painelPagina(
        titulo="Histórico de mensalidades",
        descricao="Valores, vencimentos e situação dos pagamentos.",
        contexto="PAGAMENTOS",
    ):
        if not mensalidades:
            st.info(
                "Nenhum registro de mensalidade foi encontrado.",
                icon=":material/info:",
            )

        else:
            dadosMensalidades = [
                {
                    "Referência": mensalidade.data_inicio.strftime("%m/%Y"),
                    "Vencimento": mensalidade.data_vencimento,
                    "Valor Base (R$)": float(mensalidade.valor),
                    "Situação": ("Paga" if mensalidade.foi_paga else "Pendente"),
                }
                for mensalidade in mensalidades
            ]

            tabelaMensalidades = pd.DataFrame(dadosMensalidades).sort_values(
                by=["Vencimento"],
                ascending=False,
            )

            configuracaoMensalidades = {
                "Referência": st.column_config.TextColumn("Referência"),
                "Vencimento": st.column_config.DateColumn(
                    "Vencimento",
                    format="DD/MM/YYYY",
                ),
                "Valor Base (R$)": st.column_config.NumberColumn(
                    "Valor total",
                    format="R$ %.2f",
                ),
                "Situação": st.column_config.TextColumn("Situação do pagamento"),
            }

            marcarTabelaPagina()

            st.dataframe(
                tabelaMensalidades,
                column_config=configuracaoMensalidades,
                width="stretch",
                hide_index=True,
            )
