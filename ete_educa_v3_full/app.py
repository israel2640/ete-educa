import streamlit as st
import os
# MUDANÇA 1: Imports atualizados
# Trocamos TODAS as funções antigas pelo 'get_progress_manager'
from engine import get_progress_manager

st.set_page_config(page_title="ETE_Educa v4", page_icon="🎓", layout="centered")

# MUDANÇA 2: Usando o Gerente para carregar
# Pega o gerente (que já tem o progresso na memória)
manager = get_progress_manager()
# Pega o dicionário de progresso DELE
progress = manager.get_progress()

# Inicializa o usuário logado no st.session_state (memória)
if "user" not in st.session_state:
    st.session_state.user = None

st.title("🎓 ETE_Educa v4 — Aprender → Treinar → Desafiar")
st.caption("Foco total no edital ETE Integrado.")
st.divider()

# --- 1. SE O ALUNO JÁ ESTÁ LOGADO ---
if st.session_state.user:
    user = st.session_state.user
    
    # MUDANÇA 3: Chamando o método do gerente
    manager.ensure_user(user, "") # Garante que o usuário existe
    
    st.header(f"Olá, {user}! 👋")
    st.success(f"Você está logado como **{user}**. Use o menu ao lado para navegar.")
    
    # --- NOSSO DASHBOARD DE "GAMIFICAÇÃO" (Versão CORRIGIDA) ---
    st.subheader("Seu Progresso Atual")
    
    # (Sua lógica aqui está PERFEITA e não precisa mudar, 
    # pois 'progress' é o dicionário do gerente)
    user_data = progress[user]
    reforco_count = len(user_data.get("reforco", []))
    badges_port = len(user_data.get("portugues", {}).get("badges", []))
    badges_mat = len(user_data.get("matematica", {}).get("badges", []))
    
    nivel_aluno = user_data.get("nivel_atual", "Bronze") # Pega o nível salvo
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🏆 Meu Nível", nivel_aluno) # EXIBE O NÍVEL
    col2.metric("🧠 Itens no Reforço", reforco_count)
    col3.metric("📚 Badges Concluídos", badges_port + badges_mat)

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
                # MUDANÇA 4: Usando o método do Gerente
                success, message = manager.check_user_login(selected_user, password_input)
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
                    # MUDANÇA 5: Usando os métodos do Gerente
                    manager.ensure_user(novo_nome, nova_senha) # Cria o perfil com senha
                    manager.save_progress() # Salva o novo usuário no GitHub
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
                    # MUDANÇA 6: Usando o método do Gerente
                    # (O método 'delete_user' do gerente já salva no GitHub)
                    success, message = manager.delete_user(user_to_delete, password_delete)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)