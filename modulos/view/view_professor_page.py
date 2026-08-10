import re
import streamlit as st
from modulos.academico.academico_service import listarProfessorCpf, listarProfessorId
from modulos.utils.view_utils import formatar_cpf, limpar_consulta_professor
from modulos.utils.view_visual import (AcaoView, CampoBusca, CampoView, SecaoView, renderizarCabecalhoView, renderizarFormularioBusca, renderizarMensagemInicial, renderizarRegistroView)

# Tela de visualização de professor
def telaViewProfessor():

    if "professor_id" in st.session_state:
        st.session_state["consulta_professor_id"] = st.session_state.pop("professor_id")

    professor = None

    # Função de navegação 
    def voltar():
        from modulos.rotas import (
            listagem_professor_page,
        )

        st.switch_page(listagem_professor_page)

    renderizarCabecalhoView(categoria="View", titulo="Consultar professor", descricao=("Localize um professor utilizando " "o CPF ou o identificador."), ao_voltar=voltar, prefixo_chave="professor")

    buscar, valores = renderizarFormularioBusca(
        campos=[
            CampoBusca(
                nome="cpf",
                rotulo="CPF",
                placeholder="Somente números",
                proporcao=1,
                chave="consulta_professor_cpf",
            ),
            CampoBusca(
                nome="id",
                rotulo="ID",
                placeholder="Ex.: 1",
                proporcao=1,
                chave="consulta_professor_id_digitado",
            ),
        ],
        prefixo_chave="professor",
        titulo="Localizar professor",
        descricao=("Informe somente o CPF ou somente o ID."),
    )

    if buscar:
        st.session_state.pop(
            "consulta_professor_id",
            None,
        )

        cpf = re.sub(r"\D", "", valores["cpf"])
        idProfessor = valores["id"].strip()

        if not cpf and not idProfessor:
            st.warning("Informe um CPF ou um ID.")

        elif cpf and idProfessor:
            st.warning("Informe somente o CPF ou somente o ID.")

        elif cpf:
            if len(cpf) != 11:
                st.error("O CPF deve possuir 11 números.")

            else:
                professor = listarProfessorCpf(cpf)

                if professor is None:
                    st.error("Professor não encontrado.")

                else:
                    st.session_state["consulta_professor_id"] = professor.pessoa_id

        elif not idProfessor.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            professor = listarProfessorId(int(idProfessor))

            if professor is None:
                st.error("Professor não encontrado.")

            else:
                st.session_state["consulta_professor_id"] = professor.pessoa_id

    professorId = st.session_state.get("consulta_professor_id")

    if professor is None and professorId is not None:
        professor = listarProfessorId(professorId)

    if professor is None:
        if not buscar:
            renderizarMensagemInicial(
                "Informe um CPF ou ID para consultar " "um professor."
            )

        return

    # Função para edição de professor
    def editar(registro):
        st.session_state["edicao_professor_id"] = registro.pessoa_id

        from modulos.rotas import (
            editar_professor_page,
        )

        st.switch_page(editar_professor_page)

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
            descricao=("Informações de identificação " "e contato do professor."),
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
            titulo="Vínculo institucional",
            descricao=("Campus ao qual o professor " "está vinculado."),
            linhas=[
                [
                    CampoView(
                        rotulo="ID",
                        valor=lambda item: (item.pessoa_id),
                        proporcao=1.2,
                    ),
                    CampoView(
                        rotulo="Campus",
                        valor=lambda item: (
                            item.campus.nome if item.campus else "Não informado"
                        ),
                        proporcao=4.8,
                        tipo="badge",
                    ),
                ],
            ],
        ),
    ]

    renderizarRegistroView(
        registro=professor,
        nome=lambda item: item.pessoa.nome,
        tipo_registro="Professor",
        meta=lambda item: (item.campus.nome if item.campus else "Campus não informado"),
        status="Registro localizado",
        secoes=secoes,
        prefixo_chave="professor",
        ao_limpar=limpar_consulta_professor,
        acoes=acoes,
    )
