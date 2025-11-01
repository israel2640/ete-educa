import streamlit as st
import unicodedata
from engine import load_lessons, load_progress, save_progress, ensure_user

# ==========================
# 🔹 Configuração da página
# ==========================
st.set_page_config(page_title="🧠 Reforço — ETE Educa", page_icon="🧠", layout="centered")
st.header("🧠 Reforço — Revise o que errou e domine o conteúdo!")

# ====== Função auxiliar padronizada ======
def normalizar_materia(nome: str) -> str:
    """Remove acentos e padroniza para minúsculas."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', nome.lower())
        if unicodedata.category(c) != 'Mn'
    )

# ==========================
# 🔹 Carregar dados
# ==========================
lessons = load_lessons()
progress = load_progress()

# --- CORREÇÃO AQUI ---
# Pega o nome do usuário do 'user_input' da página principal
if "user_input" not in st.session_state:
    st.session_state.user_input = "aluna1" 
user = st.session_state.user_input # Lê a chave correta
st.info(f"Aluna: **{user}**") 
# --- FIM DA CORREÇÃO ---

ensure_user(progress, user)

materia = st.selectbox("Matéria", ["Português", "Matemática"], index=0)
materia_key = normalizar_materia(materia)

# ==========================
# 🔹 Carregar lista de reforço
# ==========================
lista_reforco_ids = progress[user].get("reforco", [])

if not lista_reforco_ids:
    st.success("🎉 Nenhum tema pendente! Você está indo muito bem!")
    st.stop()

# ==========================
# 🔹 Mostrar lições de reforço
# ==========================
st.info("Revise as lições que você errou durante os treinos. Depois, volte a praticar!")

temas_para_revisar = 0
for lesson in lessons:
    # Mostrar apenas as lições da matéria selecionada que estão na lista de reforço
    if lesson["id"] in lista_reforco_ids and lesson.get("subject", "").lower() == materia_key:
        temas_para_revisar += 1
        st.subheader(f"📘 {lesson['title']}")
        st.markdown(lesson.get("lesson_text", "Resumo não disponível."))
        st.info(f"💡 Exemplo: {lesson.get('example', 'Sem exemplo.')}")

        # Mostrar perguntas extras, se houver
        for i, q in enumerate(lesson.get("train_questions", []), start=1):
            st.markdown(f"**{i}. {q['q']}**")
            st.info(f"💡 Explicação: {q.get('exp', 'Sem explicação cadastrada.')}")
        st.divider()

if temas_para_revisar == 0:
    st.success(f"🎉 Nenhum tema de {materia} pendente na lista de reforço!")

st.caption("Dica: Revise 2 temas por dia até limpar sua lista de reforço 🧩")