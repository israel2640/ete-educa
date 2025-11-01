import streamlit as st
import os
from engine import QuizEngine 

st.set_page_config(page_title="ETE_Educa v4", page_icon="🎓", layout="centered")
st.title("🎓 ETE_Educa v4 — Aprender → Treinar → Desafiar")
st.caption("Foco total no edital ETE Integrado. IA opcional (OpenAI).")

# --- Sidebar ---
with st.sidebar:
    st.header("👩‍🎓 Perfil do Aluno(a)")
    
    # --- CORREÇÃO AQUI ---
    # O 'key' já salva o valor no session_state. 
    # Não precisamos da função 'on_change' que estava causando o bug de timing.
    if "user_input" not in st.session_state:
        st.session_state.user_input = "aluna1" # Valor padrão

    st.text_input(
        "Nome da aluna(o):", 
        key="user_input" # O valor é salvo diretamente em st.session_state.user_input
    )
    # --- FIM DA CORREÇÃO ---
    
    st.info("Use as páginas abaixo na sequência para aprender melhor 📚")

st.markdown("### 📚 Módulos de Aprendizado")
st.write("1️⃣ **Estudar** — Mini-aulas curtas com IA e questões guiadas")
st.write("2️⃣ **Treinar** — 3 questões por lição (precisa acertar ≥ 2)")
st.write("3️⃣ **Desafiar (Simulado)** — prova-treino estilo ETE")
st.write("4️⃣ **Reforço** — revisa os erros com ajuda da IA")
st.write("5️⃣ **Revisão com IA** — explicações carinhosas e resumos personalizados")
st.write("6️⃣ **Plano (14 dias)** — agenda para revisar tudo antes da prova")

st.success("💡 Dica: estude 20–30 minutos, descanse 5, e volte com foco nos erros!")