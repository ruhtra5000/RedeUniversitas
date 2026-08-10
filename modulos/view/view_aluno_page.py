import re
import streamlit as st
from modulos.academico.academico_service import listarAlunoCpf, listarAlunoId
from modulos.utils.view_utils import formatar_cpf, limpar_consulta_aluno
from modulos.utils.view_visual import (AcaoView, CampoBusca, CampoView, SecaoView, renderizarCabecalhoView, renderizarFormularioBusca, renderizarMensagemInicial, renderizarRegistroView)

# Tela de visualização de aluno
def telaViewAluno():

    if "aluno_id" in st.session_state:
        st.session_state["consulta_aluno_id"] = st.session_state.pop("aluno_id")

    aluno = None

    # Função de navegação 
    def voltar():
        from modulos.rotas import listagem_aluno_page

        st.switch_page(listagem_aluno_page)

    renderizarCabecalhoView(categoria="View", titulo="Consultar aluno", descricao=("Localize um aluno utilizando o CPF " "ou o identificador."), ao_voltar=voltar, prefixo_chave="aluno")

    buscar, valores = renderizarFormularioBusca(
        campos=[
            CampoBusca(
                nome="cpf",
                rotulo="CPF",
                placeholder="Somente números",
                proporcao=1,
                chave="consulta_cpf",
            ),
            CampoBusca(
                nome="id",
                rotulo="ID",
                placeholder="Ex.: 1",
                proporcao=1,
                chave="consulta_id",
            ),
        ],
        prefixo_chave="aluno",
        titulo="Localizar aluno",
        descricao=("Informe somente o CPF ou somente o ID."),
    )

    if buscar:
        st.session_state.pop("consulta_aluno_id", None)

        cpf = re.sub(r"\D", "", valores["cpf"])
        idAluno = valores["id"].strip()

        if not cpf and not idAluno:
            st.warning("Informe um CPF ou um ID.")

        elif cpf and idAluno:
            st.warning("Informe somente o CPF ou somente o ID.")

        elif cpf:
            if len(cpf) != 11:
                st.error("O CPF deve possuir 11 números.")

            else:
                aluno = listarAlunoCpf(cpf)

                if aluno is None:
                    st.error("Aluno não encontrado.")

                else:
                    st.session_state["consulta_aluno_id"] = aluno.pessoa_id

        elif not idAluno.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            aluno = listarAlunoId(int(idAluno))

            if aluno is None:
                st.error("Aluno não encontrado.")

            else:
                st.session_state["consulta_aluno_id"] = aluno.pessoa_id

    alunoId = st.session_state.get("consulta_aluno_id")

    if aluno is None and alunoId is not None:
        aluno = listarAlunoId(alunoId)

    if aluno is None:
        if not buscar:
            renderizarMensagemInicial(
                "Informe um CPF ou ID para consultar " "um aluno."
            )

        return

    # Função para edição de aluno
    def editar(registro):
        st.session_state["edicao_aluno_id"] = registro.pessoa_id

        from modulos.rotas import editar_aluno_page

        st.switch_page(editar_aluno_page)

    acoes = []

    if "ADMIN" in st.session_state.get("roles", []):
        acoes.append(
            AcaoView(
                rotulo="Editar",
                icone=":material/edit:",
                tipo="secondary",
                chave="editar",
                ao_clicar=editar,
            )
        )

    secoes = [
        SecaoView(
            titulo="Dados pessoais",
            descricao=("Informações de identificação " "e contato do aluno."),
            linhas=[
                [
                    CampoView(
                        rotulo="Nome",
                        valor=lambda item: (item.pessoa.nome),
                        proporcao=3.5,
                    ),
                    CampoView(
                        rotulo="CPF",
                        valor=lambda item: formatar_cpf(item.pessoa.cpf),
                        proporcao=2.5,
                    ),
                ],
                [
                    CampoView(
                        rotulo="E-mail",
                        valor=lambda item: (item.pessoa.email),
                        proporcao=3.5,
                        tipo="email",
                    ),
                    CampoView(
                        rotulo="Telefone",
                        valor=lambda item: (item.pessoa.telefone or "Não informado"),
                        proporcao=2.5,
                    ),
                ],
            ],
        ),
        SecaoView(
            titulo="Dados acadêmicos",
            descricao=("Informações de matrícula, curso " "e desempenho acadêmico."),
            linhas=[
                [
                    CampoView(
                        rotulo="ID",
                        valor=lambda item: (item.pessoa_id),
                        proporcao=1,
                    ),
                    CampoView(
                        rotulo="Matrícula",
                        valor=lambda item: (item.matricula),
                        proporcao=2,
                    ),
                    CampoView(
                        rotulo="Campus",
                        valor=lambda item: (
                            item.campus.nome if item.campus else "Não informado"
                        ),
                        proporcao=3,
                        tipo="badge",
                    ),
                ],
                [
                    CampoView(
                        rotulo="Curso",
                        valor=lambda item: (
                            item.curso.nome if item.curso else "Não informado"
                        ),
                        proporcao=3,
                    ),
                    CampoView(
                        rotulo="Média geral",
                        valor=lambda item: (f"{item.media_geral or 0:.2f}"),
                        proporcao=1.5,
                        tipo="destaque",
                    ),
                    CampoView(
                        rotulo="Coef. rendimento",
                        valor=lambda item: (f"{item.coef_rend or 0:.2f}"),
                        proporcao=1.5,
                        tipo="destaque",
                    ),
                ],
            ],
        ),
    ]

    renderizarRegistroView(
        registro=aluno,
        nome=lambda item: item.pessoa.nome,
        tipo_registro="Aluno",
        meta=lambda item: (item.curso.nome if item.curso else "Curso não informado"),
        status="Registro localizado",
        secoes=secoes,
        prefixo_chave="aluno",
        ao_limpar=limpar_consulta_aluno,
        acoes=acoes,
    )
