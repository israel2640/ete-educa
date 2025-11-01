import streamlit as st
import unicodedata
from engine import load_lessons, load_progress, save_progress, ensure_user
from ai_helpers import explain_like_coach
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

# --- NOVO BLOCO DE VERIFICAÇÃO DE PERFIL ---
if "user" not in st.session_state or not st.session_state.user:
    st.error("Ops! Você precisa selecionar ou criar um perfil na página principal (🎓 ETE_Educa v4) primeiro.")
    st.warning("Por favor, retorne à página principal para fazer o login.")
    st.stop() # Para a execução da página

user = st.session_state.user
st.info(f"Aluno(a) logado: **{user}**") # Mostra quem está logado


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

        # --- NOVA LÓGICA DE IA ---
        exp_key = f"exp_ia_{lesson['id']}" # Chave única para o expander
        
        if st.checkbox(f"🤖 Pedir à IA para explicar '{lesson['title']}' de outro jeito", key=f"check_ia_{lesson['id']}"):
            with st.spinner("A IA está preparando uma explicação com carinho..."):
                try:
                    # Gera a explicação (ou usa o cache 'st.session_state')
                    if exp_key not in st.session_state:
                        prompt = f"Por favor, me explique este tópico: '{lesson['title']}'. Contexto: {lesson.get('lesson_text', '')}"
                        st.session_state[exp_key] = explain_like_coach(prompt, materia)
                    
                    # Mostra a explicação
                    st.markdown(st.session_state[exp_key])
                except Exception as e:
                    st.error(f"Não foi possível conectar à IA. Verifique seu .env. Erro: {e}")
        # --- FIM DA NOVA LÓGICA ---

        # Mostrar perguntas extras, se houver (agora dentro de um expander)
        with st.expander("Ver perguntas de treino desta lição"):
            for i, q in enumerate(lesson.get("train_questions", []), start=1):
                st.markdown(f"**{i}. {q['q']}**")
                st.info(f"💡 Explicação: {q.get('exp', 'Sem explicação cadastrada.')}")
        
        st.divider()

if temas_para_revisar == 0:
    st.success(f"🎉 Nenhum tema de {materia} pendente na lista de reforço!")

st.caption("Dica: Revise 2 temas por dia até limpar sua lista de reforço 🧩")