import streamlit as st
from ai_helpers import explain_like_coach, ask_quick_question

# ==========================
# 🔹 Configuração da página
# ==========================
st.set_page_config(page_title="🤖 Revisão com IA — ETE Educa", page_icon="🤖", layout="centered")
st.title("🤖 Revisão com IA")
st.caption("Use a IA para explicar questões difíceis ou tirar dúvidas rápidas!")

# --- Criação das Abas ---
tab1, tab2 = st.tabs(["Explicar Questão da Prova", "Dúvida Rápida (Dicionário)"])

# ==========================
# 🔹 ABA 1: Explicar Questão
# ==========================
with tab1:
    st.subheader("Explicar Questão da Prova")
    st.info("Cole aqui uma questão completa (com as alternativas) que você errou ou não entendeu.")
    
    materia = st.radio("Matéria da Questão:", ["Português", "Matemática"], key="tab1_materia")
    question_text = st.text_area("Cole a questão aqui:", height=200, key="tab1_text")
    
    if st.button("Me explique, Professora! 👩‍🏫", key="tab1_button"):
        if not question_text:
            st.error("Por favor, cole a questão que você não entendeu.")
        else:
            with st.spinner("A IA está analisando a questão..."):
                try:
                    explicacao = explain_like_coach(question_text, materia)
                    st.markdown(explicacao)
                except Exception as e:
                    st.error(f"Não foi possível conectar à IA. Verifique seu .env. Erro: {e}")

# ==========================
# 🔹 ABA 2: Dúvida Rápida (Dicionário)
# ==========================
with tab2:
    st.subheader("Dúvida Rápida (Dicionário)")
    st.info("Não sabe o que uma palavra significa? Ou tem uma dúvida rápida de matemática? Pergunte aqui!")
    
    pergunta = st.text_input("Qual é a sua dúvida?", placeholder="Ex: O que significa 'perdulários'?", key="tab2_text")
    
    if st.button("Me responda, por favor! 💡", key="tab2_button"):
        if not pergunta:
            st.error("Por favor, digite sua dúvida.")
        else:
            with st.spinner("A IA está buscando a resposta..."):
                try:
                    resposta = ask_quick_question(pergunta)
                    st.markdown(resposta)
                except Exception as e:
                    st.error(f"Não foi possível conectar à IA. Verifique seu .env. Erro: {e}")