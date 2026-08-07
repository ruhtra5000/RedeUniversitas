from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
from modulos.academico.academico_service import listarCampusId, editarCampus

def telaEdicaoCampus():
    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem editar registros.")
        st.stop()

    campus_id = st.session_state.get("edicao_campus_id")
    if not campus_id:
        st.error("Campus não especificado para edição.")
        if st.button("Voltar"):
            from modulos.rotas import view_campus_page
            st.switch_page(view_campus_page)
        st.stop()

    campus = listarCampusId(campus_id)
    if not campus:
        st.error("Campus não encontrado.")
        st.stop()

    if "form_key_edit_campus" not in st.session_state:
        st.session_state.form_key_edit_campus = 0

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button(":material/arrow_back: Voltar", width="stretch"):
            st.session_state["consulta_campus_id"] = campus_id
            from modulos.rotas import view_campus_page
            st.switch_page(view_campus_page)

    st.title(":material/edit: Editar Campus")
    st.caption("Altere os dados do campus.")

    if st.session_state.pop("edicao_realizada", False):
        st.toast("Dados do campus atualizados com sucesso!", icon=":material/check:")

    with st.container():
        with st.container():
            st.subheader("Dados do Campus")
            with st.container(horizontal=True):
                nome = st.text_input(
                    "Nome do Campus *",
                    value=campus.nome,
                    key=f"edit_campus_nome_{st.session_state.form_key_edit_campus}"
                )
                email = st.text_input(
                    "E-mail de Contato *",
                    value=campus.email,
                    key=f"edit_campus_email_{st.session_state.form_key_edit_campus}"
                )

            with st.container(horizontal=True):
                telefone = st.text_input(
                    "Telefone",
                    value=campus.telefone if campus.telefone else "",
                    key=f"edit_campus_telefone_{st.session_state.form_key_edit_campus}"
                )
                st.text_input(
                    "Reitor",
                    value=campus.reitor.pessoa.nome if campus.reitor else "Nenhum reitor designado",
                    disabled=True,
                    help="O reitor é definido através de designação de cargo.",
                    key=f"edit_campus_reitor_{st.session_state.form_key_edit_campus}"
                )

        st.write("")
        _, centro, _ = st.columns([2, 3, 2])

        with centro:
            salvar = st.button(
                "Salvar Alterações",
                width="stretch",
                type="primary",
                key=f"btn_edit_campus_{st.session_state.form_key_edit_campus}"
            )

    if salvar:
        if not nome.strip() or not email.strip():
            st.error("Preencha todos os campos obrigatórios (Nome e E-mail).")
        else:
            try:
                editarCampus(
                    idCampus=campus.id,
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=telefone.strip() if telefone.strip() else None
                )
                st.session_state.form_key_edit_campus += 1 
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(f"{str(e)}")
