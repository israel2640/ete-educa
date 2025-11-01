import streamlit as st
import os
# Imports atualizados do engine
from engine import load_progress, save_progress, ensure_user, delete_user, check_user_login

st.set_page_config(page_title="ETE_Educa v4", page_icon="🎓", layout="centered")

# Carrega o progresso UMA VEZ
progress = load_progress()

# Inicializa o usuário logado no st.session_state (memória)
if "user" not in st.session_state:
    st.session_state.user = None

st.title("🎓 ETE_Educa v4 — Aprender → Treinar → Desafiar")
st.caption("Foco total no edital ETE Integrado.")
st.divider()

# --- 1. SE O ALUNO JÁ ESTÁ LOGADO ---
if st.session_state.user:
    user = st.session_state.user
    # Não precisa de senha aqui, pois ele já passou pela verificação
    ensure_user(progress, user, "") # Apenas garante que as chaves de progresso existam
    
    st.header(f"Olá, {user}! 👋")
    st.success(f"Você está logado como **{user}**. Use o menu ao lado para navegar.")
    
    # --- NOSSO DASHBOARD DE "GAMIFICAÇÃO" ---
    st.subheader("Seu Progresso Atual")
    
    user_data = progress[user]
    reforco_count = len(user_data.get("reforco", []))
    badges_port = len(user_data.get("portugues", {}).get("badges", []))
    badges_mat = len(user_data.get("matematica", {}).get("badges", []))
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🧠 Itens no Reforço", reforco_count)
    col2.metric("📚 Badges (Português)", badges_port)
    col3.metric("🧮 Badges (Matemática)", badges_mat)

    if reforco_count > 0:
        st.info("Você tem itens pendentes na página '🧠 Reforço'. Não se esqueça de revisar!")
    
    if st.button("Trocar de Perfil (Sair)"):
        st.session_state.user = None
        st.rerun()

# --- 2. SE NINGUÉM ESTÁ LOGADO (TELA DE LOGIN) ---
else:
    st.header("👩‍🎓 Bem-vindo(a)! Selecione ou crie seu perfil")

    nomes_alunos = list(progress.keys())
    
    # --- Bloco 1: Selecionar Perfil Existente ---
    if nomes_alunos:
        st.subheader("Carregar Perfil")
        with st.form("login_form"):
            selected_user = st.selectbox("Selecione seu perfil:", options=nomes_alunos)
            password_input = st.text_input("Digite sua senha:", type="password")
            login_submitted = st.form_submit_button("✅ Carregar Perfil")
            
            if login_submitted:
                success, message = check_user_login(progress, selected_user, password_input)
                if success:
                    st.session_state.user = selected_user
                    st.rerun()
                else:
                    st.error(message)
    else:
        st.info("Nenhum perfil encontrado. Crie um novo abaixo.")

    st.divider()

    # --- Bloco 2: Criar Novo Perfil ---
    with st.expander("➕ Criar um novo perfil"):
        with st.form("novo_perfil_form"):
            novo_nome = st.text_input("Digite seu nome (Ex: 'Joao'):")
            nova_senha = st.text_input("Digite uma senha:", type="password")
            submitted = st.form_submit_button("Criar e Entrar")
            
            if submitted:
                if not novo_nome or not nova_senha:
                    st.error("Por favor, digite um nome E uma senha.")
                elif novo_nome in progress:
                    st.error("Este nome já existe! Tente outro ou carregue o perfil acima.")
                else:
                    ensure_user(progress, novo_nome, nova_senha) # Cria o perfil com senha
                    save_progress(progress) # Salva
                    st.session_state.user = novo_nome # Define como ativo
                    st.success(f"Perfil para '{novo_nome}' criado com sucesso!")
                    st.balloons()
                    st.rerun() 

    # --- Bloco 3: Deletar Perfil ---
    with st.expander("❌ Deletar um perfil"):
        if nomes_alunos:
            st.warning(f"⚠️ **Atenção!** Isso irá apagar **TODO** o progresso permanentemente.")
            with st.form("delete_form"):
                user_to_delete = st.selectbox(
                    "Selecione o perfil para DELETAR:",
                    options=nomes_alunos,
                    key="delete_select"
                )
                password_delete = st.text_input("Digite a senha deste perfil para confirmar:", type="password")
                delete_submitted = st.form_submit_button(f"🗑️ Deletar perfil '{user_to_delete}'")
                
                if delete_submitted:
                    success, message = delete_user(progress, user_to_delete, password_delete)
                    if success:
                        save_progress(progress)
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)