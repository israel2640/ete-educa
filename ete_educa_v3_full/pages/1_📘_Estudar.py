import streamlit as st
# MUDANÇA 1: Imports atualizados
from engine import QuizEngine, get_progress_manager 
from ai_helpers import explain_like_coach
# CORREÇÃO: Importar 'questoes' da pasta 'data'
from data.questoes import questoes_portugues, questoes_matematica

# =====================================================
# 🔹 Configuração da página
# =====================================================
st.set_page_config(page_title="Estudar — ETE Educa", layout="centered")
st.title("📘 Estudar — Mini Aulas Interativas")
st.caption("Aprenda os principais temas do edital da ETE com explicações da IA 🤖")

# =====================================================
# 🔹 Carregar dados de progresso e usuário
# =====================================================
# MUDANÇA 2: Usando o Gerente para carregar
manager = get_progress_manager()
progress = manager.get_progress()

# --- NOVO BLOCO DE VERIFICAÇÃO DE PERFIL ---
if "user" not in st.session_state or not st.session_state.user:
    st.error("Ops! Você precisa selecionar ou criar um perfil na página principal (🎓 ETE_Educa v4) primeiro.")
    st.warning("Por favor, retorne à página principal para fazer o login.")
    st.stop() # Para a execução da página

user = st.session_state.user
st.info(f"Aluno(a) logado: **{user}**") # Mostra quem está logado

# MUDANÇA 2 (continuação): Chamando o método do gerente
manager.ensure_user(user, "")

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
    # (Sua lógica aqui está PERFEITA e não precisa mudar, 
    # pois 'progress' é o dicionário do gerente)
    badges_estudados = progress[user].get(materia_key, {}).get("badges", [])
    ids_licoes_materia = [q["id"] for q in questoes]
    licoes_ja_feitas = [badge for badge in badges_estudados if badge in ids_licoes_materia]
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

# (Sua lógica aqui está PERFEITA e não precisa mudar)
studied_badges = set(progress[user].get(materia_key, {}).get("badges", []))
total_licoes = len(questoes)
licoes_feitas = len([badge for badge in studied_badges if badge in [q["id"] for q in questoes]])

def format_lesson_title(lesson):
    status = "✅ Feito" if lesson['id'] in studied_badges else "📖 Estudar"
    return f"{status} — {lesson['id']} - {lesson['title']}"

selected_lesson = st.selectbox(
    "Escolha uma lição para estudar ou revisar:",
    options=questoes,
    format_func=format_lesson_title,
    index=min(st.session_state.questao_atual, total_licoes - 1)
)

if "selected_lesson_id" not in st.session_state or st.session_state.selected_lesson_id != selected_lesson["id"]:
    st.session_state.fase = "aula"
    st.session_state.feedback = ""
    st.session_state.selected_lesson_id = selected_lesson["id"]

questao = selected_lesson
engine.atual = questoes.index(selected_lesson)

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
            st.markdown(f"**{q['q']}**")
            resposta = st.radio("Escolha sua resposta:", q["opts"], key=f"q_{questao['id']}", index=None)
            
            if st.button("Responder"):
                acertou, feedback = engine.responder(resposta)
                st.session_state.feedback = feedback # Salva o feedback
                
                # MUDANÇA 3: Salvando com o Gerente
                manager.set_studied(user, materia_key, questao["id"])
                manager.save_progress()
                
                st.session_state.fase = "feedback"
                st.rerun()

# --- Etapa 3: Feedback ---
elif st.session_state.fase == "feedback":
    st.subheader("📘 Revisão")
    st.markdown(st.session_state.feedback) # Mostra o feedback salvo
    
    if st.button("Voltar para a lista de lições"):
        st.session_state.fase = "aula"
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
        
        # (Sua lógica aqui está PERFEITA e não precisa mudar)
        badges_atuais = progress[user][materia_key].get("badges", [])
        ids_desta_materia = [q["id"] for q in questoes]
        progress[user][materia_key]["badges"] = [b for b in badges_atuais if b not in ids_desta_materia]
        progress[user][materia_key]["treinos_ok"] = 0
        reforco_atual = progress[user].get("reforco", [])
        progress[user]["reforco"] = [r for r in reforco_atual if r not in ids_desta_materia]
        
        # MUDANÇA 4: Salvando com o Gerente
        manager.save_progress()
        st.session_state.fase = "aula"
        st.rerun()