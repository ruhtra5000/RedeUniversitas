import streamlit as st
from modulos.academico.academico_service import listarMatriculaId
from modulos.utils.view_utils import formatar_aprovacao, limpar_consulta_matricula
from modulos.utils.view_visual import (CampoBusca, CampoView, SecaoView, renderizarCabecalhoView, renderizarFormularioBusca, renderizarMensagemInicial, renderizarRegistroView)

# Tela de visualização de matrícula
def telaViewMatricula():

    selecionada = st.session_state.pop(
        "matricula_selecionada",
        None,
    )

    if selecionada:
        st.session_state["consulta_matricula_chave"] = selecionada

    matricula = None

    # Função de navegação 
    def voltar():
        from modulos.rotas import (
            listagem_matricula_page,
        )

        st.switch_page(listagem_matricula_page)

    renderizarCabecalhoView(categoria="View", titulo="Consultar matrícula", descricao=("Localize uma matrícula utilizando os IDs " "do aluno e da turma."), ao_voltar=voltar, prefixo_chave="matricula")

    buscar, valores = renderizarFormularioBusca(
        campos=[
            CampoBusca(
                nome="aluno",
                rotulo="ID do aluno",
                placeholder="Ex.: 1",
                proporcao=1,
                chave="consulta_matricula_aluno",
            ),
            CampoBusca(
                nome="turma",
                rotulo="ID da turma",
                placeholder="Ex.: 1",
                proporcao=1,
                chave="consulta_matricula_turma",
            ),
        ],
        prefixo_chave="matricula",
        titulo="Localizar matrícula",
        descricao=("Informe os identificadores do aluno " "e da turma."),
    )

    if buscar:
        st.session_state.pop(
            "consulta_matricula_chave",
            None,
        )

        idAluno = valores["aluno"].strip()
        idTurma = valores["turma"].strip()

        if not idAluno or not idTurma:
            st.warning("Informe os IDs do aluno e da turma.")

        elif not all(valor.isdigit() for valor in [idAluno, idTurma]):
            st.error("Todos os IDs devem conter " "somente números.")

        else:
            matricula = listarMatriculaId(
                int(idAluno),
                int(idTurma),
            )

            if matricula is None:
                st.error("Matrícula não encontrada.")

            else:
                st.session_state["consulta_matricula_chave"] = {
                    "aluno_id": matricula.aluno_id,
                    "turma_id": matricula.turma_id,
                }

    chave = st.session_state.get("consulta_matricula_chave")

    if matricula is None and chave:
        matricula = listarMatriculaId(
            chave["aluno_id"],
            chave["turma_id"],
        )

    if matricula is None:
        if not buscar:
            renderizarMensagemInicial(
                "Informe os dados para consultar " "uma matrícula."
            )

        return

    secoes = [
        SecaoView(
            titulo="Dados do aluno",
            descricao=("Aluno vinculado à matrícula acadêmica."),
            linhas=[
                [
                    CampoView(
                        rotulo="ID",
                        valor=lambda item: (item.aluno_id),
                        proporcao=1,
                    ),
                    CampoView(
                        rotulo="Aluno",
                        valor=lambda item: (item.aluno.pessoa.nome),
                        proporcao=3,
                    ),
                    CampoView(
                        rotulo="Matrícula institucional",
                        valor=lambda item: (item.aluno.matricula),
                        proporcao=2,
                    ),
                ],
            ],
        ),
        SecaoView(
            titulo="Vínculo acadêmico",
            descricao=("Turma, disciplina e situação " "da matrícula."),
            linhas=[
                [
                    CampoView(
                        rotulo="Turma",
                        valor=lambda item: (
                            item.turma.codigo or f"Turma {item.turma_id}"
                        ),
                        proporcao=2,
                    ),
                    CampoView(
                        rotulo="Disciplina",
                        valor=lambda item: (item.disciplina.nome),
                        proporcao=2,
                    ),
                    CampoView(
                        rotulo="Situação",
                        valor=lambda item: (formatar_aprovacao(item.aprovacao)),
                        proporcao=2,
                        tipo="badge",
                    ),
                ],
                [
                    CampoView(
                        rotulo="ID do aluno",
                        valor=lambda item: (item.aluno_id),
                        proporcao=1,
                    ),
                    CampoView(
                        rotulo="ID da turma",
                        valor=lambda item: (item.turma_id),
                        proporcao=1,
                    ),
                ],
            ],
        ),
    ]

    renderizarRegistroView(
        registro=matricula,
        nome=lambda item: (f"Matrícula de " f"{item.aluno.pessoa.nome}"),
        tipo_registro="Matrícula",
        meta=lambda item: (item.disciplina.nome),
        status=lambda item: formatar_aprovacao(item.aprovacao),
        secoes=secoes,
        prefixo_chave="matricula",
        ao_limpar=limpar_consulta_matricula,
    )
