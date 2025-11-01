import streamlit as st
from engine import QuizEngine, load_progress, save_progress, set_studied, ensure_user
from ai_helpers import explain_like_coach
# CORREÇÃO: Importar 'questoes' da pasta 'data'
from data.questoes import questoes_portugues, questoes_matematica

# =====================================================
# 🔹 Configuração da página
# =====================================================
st.set_page_config(page_title="📘 Estudar — ETE Educa", page_icon="📘", layout="centered")
st.title("📘 Estudar — Mini Aulas Interativas")
st.caption("Aprenda os principais temas do edital da ETE com explicações da IA 🤖")

# =====================================================
# 🔹 Carregar dados de progresso e usuário
# =====================================================
progress = load_progress()

# --- NOVO BLOCO DE VERIFICAÇÃO DE PERFIL ---
if "user" not in st.session_state or not st.session_state.user:
    st.error("Ops! Você precisa selecionar ou criar um perfil na página principal (🎓 ETE_Educa v4) primeiro.")
    st.warning("Por favor, retorne à página principal para fazer o login.")
    st.stop() # Para a execução da página

user = st.session_state.user
st.info(f"Aluno(a) logado: **{user}**") # Mostra quem está logado


ensure_user(progress, user)

# =====================================================
# 🔹 Escolha da matéria
# =====================================================
materia = st.radio("Escolha a matéria:", ["Português", "Matemática"])
if materia == "Português":
    questoes = questoes_portugues
    materia_key = "portugues"
else:
    questoes = questoes_matematica
    materia_key = "matematica"

engine = QuizEngine(questoes)

# =====================================================
# 🔹 Inicialização de estado (COM A CORREÇÃO)
# =====================================================
# Reinicia o progresso se a matéria mudar
if "materia_anterior" not in st.session_state or st.session_state.materia_anterior != materia:
    st.session_state.fase = "aula"
    
    # --- CORREÇÃO AQUI ---
    # Verifica o progresso salvo para saber qual é a lição atual
    # Pega os 'badges' (lições feitas) que estão salvos no GitHub
    badges_estudados = progress[user].get(materia_key, {}).get("badges", [])
    
    # Pega os IDs de todas as lições desta matéria
    ids_licoes_materia = [q["id"] for q in questoes]
    
    # Conta quantos badges desta matéria o usuário já tem
    licoes_ja_feitas = [badge for badge in badges_estudados if badge in ids_licoes_materia]
    
    # Define a questão atual como o número de lições já feitas
    # Se ela fez 2 lições, a contagem é 2, e ela começará na lição de índice 2 (a 3ª lição)
    st.session_state.questao_atual = len(licoes_ja_feitas)
    # --- FIM DA CORREÇÃO ---

    st.session_state.feedback = ""
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.materia_anterior = materia

# =====================================================
# 🔹 LÓGICA DE SELEÇÃO DE LIÇÃO (A GRANDE MUDANÇA)
# =====================================================
st.divider()

# Pega o progresso atual para marcar o status (✅ ou 📖)
studied_badges = set(progress[user].get(materia_key, {}).get("badges", []))
total_licoes = len(questoes)
licoes_feitas = len([badge for badge in studied_badges if badge in [q["id"] for q in questoes]])

# Formata o título da lição para o selectbox
def format_lesson_title(lesson):
    status = "✅ Feito" if lesson['id'] in studied_badges else "📖 Estudar"
    return f"{status} — {lesson['id']} - {lesson['title']}"

# O menu suspenso para escolher a lição
selected_lesson = st.selectbox(
    "Escolha uma lição para estudar ou revisar:",
    options=questoes,
    format_func=format_lesson_title,
    index=min(st.session_state.questao_atual, total_licoes - 1) # Começa na próxima lição a ser feita
)

# Se o usuário mudar a lição no selectbox, reinicia o estado
if "selected_lesson_id" not in st.session_state or st.session_state.selected_lesson_id != selected_lesson["id"]:
    st.session_state.fase = "aula"
    st.session_state.feedback = ""
    st.session_state.selected_lesson_id = selected_lesson["id"]

# A 'questao' agora é a lição selecionada
questao = selected_lesson
engine.atual = questoes.index(selected_lesson) # Atualiza o engine

# =====================================================
# 🔹 Controle de fluxo de estudo (Modo Aula/Questão/Feedback)
# =====================================================
titulo = questao.get("title") or questao.get("tema", "Tema não informado")
texto_aula = questao.get("lesson_text") or questao.get("texto", "Sem conteúdo disponível.")
exemplo = questao.get("example") or questao.get("exemplo", "Sem exemplo disponível.")

# --- Etapa 1: Mini Aula ---
if st.session_state.fase == "aula":
    st.subheader(f"📖 Mini Aula — {titulo}")
    st.write(texto_aula)
    st.info("💡 Exemplo: " + exemplo)

    # Explicação com IA (usando ai_helpers)
    if st.checkbox("Gerar explicação da IA "):
        with st.spinner("A IA está explicando com carinho..."):
            try:
                explicacao = explain_like_coach(
                    f"Explique o tema '{titulo}' para uma aluna de 14 anos se preparando para a prova da ETE.",
                    materia
                )
                st.markdown(explicacao)
            except Exception as e:
                st.error(f"Não foi possível conectar à IA. Verifique seu .env. Erro: {e}")

    if st.button("👉 Entendi, pode perguntar!"):
        st.session_state.fase = "questao"
        st.rerun()

# --- Etapa 2: Pergunta de Treino ---
elif st.session_state.fase == "questao":
    st.subheader(f"🎯 Questão de Treino — {titulo}")
    
    if not questao.get("train_questions"):
        st.error("Erro: Esta lição não tem 'train_questions' cadastradas.")
        if st.button("Voltar para a aula"):
            st.session_state.fase = "aula"
            st.rerun()
    else:
        q = questao["train_questions"][0] 
        
        if "opts" not in q:
             st.error("Erro: Pergunta de treino mal formatada (sem 'opts').")
             if st.button("Voltar para a aula"):
                st.session_state.fase = "aula"
                st.rerun()
        else:
            resposta = st.radio("Escolha sua resposta:", q["opts"], key=f"q_{questao['id']}", index=None)
            
            if st.button("Responder"):
                acertou, feedback = engine.responder(resposta)
                st.session_state.feedback = feedback # Salva o feedback
                
                # Salva o progresso (badge) no GitHub
                set_studied(progress, user, materia_key, questao["id"])
                save_progress(progress)
                
                st.session_state.fase = "feedback"
                st.rerun()

# --- Etapa 3: Feedback ---
elif st.session_state.fase == "feedback":
    st.subheader("📘 Revisão")
    st.markdown(st.session_state.feedback) # Mostra o feedback salvo
    
    if st.button("Voltar para a lista de lições"):
        st.session_state.fase = "aula"
        # Não precisa mais de 'questao_atual + 1', o selectbox cuida disso
        st.rerun()

# =====================================================
# 🔹 Rodapé de progresso
# =====================================================
st.divider()
if total_licoes > 0:
    progresso_percentual = (licoes_feitas / total_licoes)
else:
    progresso_percentual = 0

st.markdown(f"**Progresso em {materia}:** {licoes_feitas}/{total_licoes} lições estudadas.")
st.progress(min(progresso_percentual, 1.0))

# Lógica para "Recomeçar"
if licoes_feitas == total_licoes and total_licoes > 0:
    st.success(f"🎉 Parabéns! Você completou todas as lições de {materia}!")
    if st.button(f"Recomeçar {materia}?"):
        # Se recomeçar, limpa o progresso DESSA MATÉRIA
        badges_atuais = progress[user][materia_key].get("badges", [])
        ids_desta_materia = [q["id"] for q in questoes]
        
        # Remove apenas os badges desta matéria
        progress[user][materia_key]["badges"] = [b for b in badges_atuais if b not in ids_desta_materia]
        
        # Zera também os treinos
        progress[user][materia_key]["treinos_ok"] = 0
        
        # Limpa o 'reforco' desta matéria
        reforco_atual = progress[user].get("reforco", [])
        progress[user]["reforco"] = [r for r in reforco_atual if r not in ids_desta_materia]
        
        save_progress(progress)
        st.session_state.fase = "aula"
        st.rerun()