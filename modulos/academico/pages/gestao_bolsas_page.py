import pandas as pd
import streamlit as st
from database.entidades.enums.StatusBolsa import StatusBolsa
from modulos.academico.academico_service import (editarBolsa, listarBolsasGeral)
from modulos.utils.academico_visual import (marcarAcoesPagina, marcarTabelaPagina, painelPagina, renderizarDivisorPagina, renderizarSecaoPagina, renderizarTopoPagina)

# Tela de gestão de bolsas
def telaGestaoBolsas():
    renderizarTopoPagina(
        titulo="Gestão de bolsas",
        descricao=(
            "Consulte os benefícios concedidos e atualize suas "
            "condições de vigência."
        ),
        categoria="GESTÃO ACADÊMICA",
    )

    if st.session_state.pop("bolsas_salvas", False):
        st.toast(
            "Alterações salvas com sucesso!",
            icon=":material/check:",
        )

    if "cache_bolsas" not in st.session_state:
        st.session_state.cache_bolsas = listarBolsasGeral()

    listaBolsas = st.session_state.cache_bolsas

    if not listaBolsas:
        st.info("Nenhuma bolsa está cadastrada no sistema.")
        return

    dadosBolsas = []

    for bolsa in listaBolsas:
        try:
            nomeAluno = bolsa.aluno.pessoa.nome
        except Exception:
            nomeAluno = f"Aluno ID {bolsa.aluno_id}"

        dadosBolsas.append(
            {
                "ID Bolsa": bolsa.id,
                "Aluno": nomeAluno,
                "Tipo": bolsa.tipo_bolsa,
                "Desconto (%)": float(bolsa.percentual_desconto * 100),
                "Início": bolsa.data_inicio,
                "Término": bolsa.data_fim,
                "Status": bolsa.status.value,
            }
        )

    tabelaBolsas = pd.DataFrame(dadosBolsas)

    configuracaoColunas = {
        "ID Bolsa": st.column_config.NumberColumn(
            "ID",
            disabled=True,
        ),
        "Aluno": st.column_config.TextColumn(
            "Aluno",
            disabled=True,
        ),
        "Tipo": st.column_config.TextColumn("Tipo"),
        "Desconto (%)": st.column_config.NumberColumn(
            "Desconto",
            format="%.0f%%",
        ),
        "Início": st.column_config.DateColumn(
            "Início",
            format="DD/MM/YYYY",
        ),
        "Término": st.column_config.DateColumn(
            "Término",
            format="DD/MM/YYYY",
        ),
        "Status": st.column_config.TextColumn("Status"),
    }

    with painelPagina(
        titulo="Bolsas concedidas",
        descricao="Visão geral dos benefícios registrados no sistema.",
        contexto=f"{len(listaBolsas)} REGISTROS",
    ):
        marcarTabelaPagina()

        st.dataframe(
            tabelaBolsas,
            column_config=configuracaoColunas,
            width="stretch",
            hide_index=True,
        )

    with painelPagina(
        titulo="Editar bolsa",
        descricao=(
            "Selecione um benefício para alterar seu tipo, desconto, "
            "término ou status."
        ),
        contexto="EDIÇÃO",
    ):
        bolsaSelecionada = st.selectbox(
            "Selecione a bolsa",
            options=listaBolsas,
            format_func=lambda bolsa: (
                f"Bolsa {bolsa.id} — " f"{bolsa.aluno.pessoa.nome} | {bolsa.tipo_bolsa}"
            ),
            index=None,
            placeholder="Escolha uma bolsa...",
            key="gestao_bolsa_selecionada",
        )

        if bolsaSelecionada:
            bolsa = next(
                (item for item in listaBolsas if item.id == bolsaSelecionada.id),
                None,
            )

            if bolsa:
                renderizarDivisorPagina()

                renderizarSecaoPagina(
                    numero=1,
                    titulo="Condições do benefício",
                    descricao="Dados permitidos para edição.",
                )

                colTipo, colPercentual = st.columns(2)

                with colTipo:
                    novoTipo = st.text_input(
                        "Tipo de bolsa *",
                        value=bolsa.tipo_bolsa,
                        key=f"gestao_bolsa_tipo_{bolsa.id}",
                    )

                with colPercentual:
                    novoPercentual = st.number_input(
                        "Percentual de desconto (%) *",
                        min_value=1,
                        max_value=100,
                        step=1,
                        format="%d",
                        value=int(bolsa.percentual_desconto * 100),
                        key=f"gestao_bolsa_percentual_{bolsa.id}",
                    )

                colTermino, colStatus = st.columns(2)

                with colTermino:
                    novoTermino = st.date_input(
                        "Data de término *",
                        value=bolsa.data_fim,
                        format="DD/MM/YYYY",
                        key=f"gestao_bolsa_termino_{bolsa.id}",
                    )

                with colStatus:
                    listaStatus = list(StatusBolsa)
                    indiceStatus = (
                        listaStatus.index(bolsa.status)
                        if bolsa.status in listaStatus
                        else 0
                    )

                    novoStatus = st.selectbox(
                        "Status da bolsa *",
                        options=listaStatus,
                        index=indiceStatus,
                        format_func=lambda status: status.value,
                        key=f"gestao_bolsa_status_{bolsa.id}",
                    )

                marcarAcoesPagina()
                _, colunaSalvar, _ = st.columns([2, 3, 2])

                with colunaSalvar:
                    salvar = st.button(
                        "Salvar alterações",
                        icon=":material/save:",
                        type="primary",
                        width="stretch",
                        key=f"gestao_bolsa_salvar_{bolsa.id}",
                    )

                if salvar:
                    if not novoTipo.strip():
                        st.error("Informe o tipo da bolsa.")

                    else:
                        try:
                            editarBolsa(
                                idBolsa=bolsa.id,
                                tipo_bolsa=novoTipo.strip(),
                                percentual_desconto=(float(novoPercentual) / 100.0),
                                data_fim=novoTermino,
                                status=novoStatus,
                            )

                            st.session_state.bolsas_salvas = True
                            st.session_state.pop("cache_bolsas", None)
                            st.rerun()

                        except Exception as erro:
                            st.error(f"Erro ao salvar: {erro}")
