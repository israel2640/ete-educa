import streamlit as st
import unicodedata
# MUDANÇA 1: Imports atualizados
from engine import (
    load_lessons, get_progress_manager, shuffled_options
)

# ====== Configuração ======
st.set_page_config(page_title="Treinar — ETE Educa", layout="centered")
st.header("🎯 Treinar — Uma pergunta de cada vez")

# ====== Função auxiliar padronizada ======
def normalizar_materia(nome: str) -> str:
    """Remove acentos e padroniza para minúsculas."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', nome.lower())
        if unicodedata.category(c) != 'Mn'
    )

# ==================================
# 🔹 FUNÇÃO DE CALLBACK (A NOVA LÓGICA)
# ==================================
def check_answer():
    """Chamada IMEDIATAMENTE quando um botão de rádio é clicado."""
    # (Sua lógica de callback está perfeita e não precisa de NENHUMA MUDANÇA)
    radio_key = st.session_state.last_radio_key
    user_answer = st.session_state[radio_key]
    
    gabarito = st.session_state.current_gabarito
    explicacao = st.session_state.current_explicacao
    
    if user_answer.strip() == gabarito.strip():
        st.session_state.treino_feedback = f"✅ Correto! {explicacao}"
        st.session_state.treino_corrects += 1
    else:
        st.session_state.treino_feedback = f"❌ Errado! A resposta era '{gabarito}'.\n\n{explicacao}"
    
    st.session_state.treino_answered = True

# ====== Carregar dados ======
lessons = load_lessons()

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
manager.ensure_user(user, "") # Garante que o usuário ainda existe no JSON
# --- FIM DO NOVO BLOCO ---

materia = st.selectbox("Matéria", ["Português", "Matemática"], index=0)
materia_key = normalizar_materia(materia)

subs = [l for l in lessons if l.get("subject", "").lower() == materia_key]
# (A lógica abaixo está perfeita, usa o 'progress' que pegamos do gerente)
studied = set(progress[user].get(materia_key, {}).get("badges", []))
ordered = [l for l in subs if l["id"] in studied] + [l for l in subs if l["id"] not in studied]

if not ordered:
    st.warning(f"Nenhuma lição disponível para {materia}. Vá ao modo 'Estudar' primeiro.")
    st.stop()

# ==================================
# 🔹 Seleção e Verificação da Lição
# ==================================
lesson = st.selectbox("Lição", ordered, format_func=lambda x: f"{'✅ ' if x['id'] in studied else '🔒 '}{x['id']} — {x['title']}")

if lesson["id"] not in studied:
    st.warning("📘 Estude esta lição primeiro (na página 'Estudar') para liberar o treino.")
    disable_train = True
else:
    st.success("✅ Lição estudada! Você pode treinar.")
    disable_train = False

train_questions = lesson.get("train_questions", [])
total_questions = len(train_questions)

if total_questions == 0 and disable_train == False:
    st.error("❌ Nenhuma questão cadastrada para esta lição.")
    st.stop()

# ==================================
# 🔹 Lógica de Estado do Treino
# ==================================
# (Sua lógica de estado está perfeita e não precisa de mudança)
if "current_lesson_id" not in st.session_state or st.session_state.current_lesson_id != lesson["id"]:
    st.session_state.current_lesson_id = lesson["id"]
    st.session_state.treino_q_index = 0
    st.session_state.treino_corrects = 0
    st.session_state.treino_feedback = ""
    st.session_state.treino_answered = False
    st.session_state.treino_finished = False

st.divider()

# ==================================
# 🔹 Loop de Treino (Uma pergunta por vez)
# ==================================
# (Toda a sua lógica de quiz (callbacks, etc.) está perfeita e não precisa de mudança)
if not disable_train and not st.session_state.treino_finished:
    
    q_index = st.session_state.treino_q_index
    q_data = train_questions[q_index]
    
    st.subheader(f"Pergunta {q_index + 1} de {total_questions}")
    st.markdown(f"**{q_data['q']}**")
    
    st.session_state.current_gabarito = q_data["ans"]
    st.session_state.current_explicacao = q_data.get("exp", "Sem explicação.")
    radio_key = f"radio_q_{lesson['id']}_{q_index}"
    st.session_state.last_radio_key = radio_key
    
    st.radio(
        "Escolha:", 
        shuffled_options(q_data["opts"]), 
        key=radio_key, 
        index=None,
        on_change=check_answer, 
        disabled=st.session_state.treino_answered
    )
    
    if st.session_state.treino_answered:
        feedback = st.session_state.treino_feedback
        if "✅" in feedback:
            st.success(feedback)
        else:
            st.error(feedback)
            
        if q_index < total_questions - 1:
            if st.button("Próxima Questão ➡️"):
                st.session_state.treino_q_index += 1
                st.session_state.treino_answered = False
                st.session_state.treino_feedback = ""
                st.rerun()
        else:
            if st.button("Ver Resultado Final 🏁"):
                st.session_state.treino_finished = True
                st.rerun()

# ==================================
# 🔹 Tela de Resultado Final
# ==================================
if st.session_state.treino_finished:
    st.header(f"Resultado do Treino: {lesson['title']}")
    corrects = st.session_state.treino_corrects
    total = total_questions
    st.subheader(f"Você acertou {corrects} de {total} questões!")
    
    min_acertos = max(1, int(total * 0.7)) # Pelo menos 1 acerto ou 70%

    if corrects >= min_acertos:
        # MUDANÇA 3: Usando os métodos do Gerente
        manager.set_train_ok(user, materia_key, lesson["id"])
        st.success("🏆 Treino aprovado!")
        st.balloons()
    else:
        # MUDANÇA 3: Usando os métodos do Gerente
        manager.add_reforco(user, lesson["id"]) # Adiciona ao 'reforco'
        st.warning("⚠️ Treino não aprovado. Este tema foi adicionado ao modo 'Reforço' para revisão.")
    
    # MUDANÇA 3: Salvando com o Gerente
    manager.save_progress() # Salva o resultado no GitHub
    
    if st.button("Treinar outra lição"):
        st.session_state.treino_finished = False
        st.session_state.treino_q_index = 0
        st.session_state.treino_corrects = 0
        st.session_state.treino_feedback = ""
        st.session_state.treino_answered = False
        st.rerun()


# ==================================
# 🔹 Indicador de Progresso (Rodapé)
# ==================================
# (Sua lógica aqui está perfeita e não precisa de mudança)
if materia_key not in progress[user]:
    progress[user][materia_key] = {"treinos_ok": 0}

total_treinos_concluidos = progress[user][materia_key].get("treinos_ok", 0)
total_licoes_materia = len(subs) if subs else 1 # Evita divisão por zero

st.divider()
st.markdown(f"🏆 **Treinos concluídos em {materia}:** {total_treinos_concluidos} / {total_licoes_materia}")
st.progress(min(total_treinos_concluidos / total_licoes_materia, 1.0))