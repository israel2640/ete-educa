import streamlit as st
import unicodedata
# (Imports permanecem os mesmos)
from engine import (
    load_lessons, get_progress_manager, shuffled_options
)

# ====== Configuração ======
st.set_page_config(page_title="Treinar — ETE Educa", layout="centered")
st.header("🎯 Treinar — Sua Lista de Tarefas") # Título atualizado

# ====== Função auxiliar padronizada ======
def normalizar_materia(nome: str) -> str:
    """Remove acentos e padroniza para minúsculas."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', nome.lower())
        if unicodedata.category(c) != 'Mn'
    )

# ==================================
# 🔹 FUNÇÃO DE CALLBACK (Sem mudança)
# ==================================
def check_answer():
    """Chamada IMEDIATAMENTE quando um botão de rádio é clicado."""
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
manager = get_progress_manager()
progress = manager.get_progress()

# --- BLOCO DE VERIFICAÇÃO DE PERFIL (Sem mudança) ---
if "user" not in st.session_state or not st.session_state.user:
    st.error("Ops! Você precisa selecionar ou criar um perfil na página principal (🎓 ETE_Educa v4) primeiro.")
    st.warning("Por favor, retorne à página principal para fazer o login.")
    st.stop() 

user = st.session_state.user
st.info(f"Aluno(a) logado: **{user}**") 
manager.ensure_user(user, "") 
# --- FIM DO BLOCO ---

materia = st.selectbox("Matéria", ["Português", "Matemática"], index=0)
materia_key = normalizar_materia(materia)

subs = [l for l in lessons if l.get("subject", "").lower() == materia_key]

# ==================================
# 🔹 LÓGICA DA "LISTA DE TAREFAS" (A GRANDE MELHORIA)
# ==================================
# 1. Pega os 'badges' (O que foi Estudado)
studied = set(progress[user].get(materia_key, {}).get("badges", []))
# 2. Pega os 'treinos_ok_list' (O que foi Treinado e Aprovado)
trained = set(progress[user].get(materia_key, {}).get("treinos_ok_list", []))

# 3. Gera as listas de prioridade
licoes_para_fazer = [l for l in subs if l["id"] in studied and l["id"] not in trained]
licoes_concluidas = [l for l in subs if l["id"] in trained]
licoes_bloqueadas = [l for l in subs if l["id"] not in studied]

# 4. Junta tudo na ordem certa
ordered = licoes_para_fazer + licoes_concluidas + licoes_bloqueadas

if not ordered:
    st.warning(f"Nenhuma lição disponível para {materia}. Vá ao modo 'Estudar' primeiro.")
    st.stop()

# 5. Nova função para formatar o título no selectbox
def format_lesson_title(lesson):
    lesson_id = lesson['id']
    if lesson_id in trained:
        status = "🏆 Treino OK"
    elif lesson_id in studied:
        status = "🎯 Para Treinar" # ESTE É O FOCO!
    else:
        status = "🔒 Bloqueada"
    return f"{status} — {lesson['id']} - {lesson['title']}"

# ==================================
# 🔹 Seleção e Verificação da Lição
# ==================================
lesson = st.selectbox(
    "Escolha uma lição (Tarefas 🎯 aparecem primeiro):", 
    ordered, 
    format_func=format_lesson_title
)

# A lógica de bloqueio agora é APENAS se não foi estudada
if lesson["id"] not in studied:
    st.warning("📘 Você precisa 'Estudar' esta lição primeiro (na página 'Estudar') para liberar o treino.")
    disable_train = True
else:
    # Verifica se já foi treinado (para dar um aviso de revisão)
    if lesson["id"] in trained:
        st.info("🏆 Você já foi aprovado neste treino, mas pode refazê-lo para revisar!")
    else:
        st.success("✅ Lição estudada! Este é o seu próximo treino. Boa sorte!")
    disable_train = False

train_questions = lesson.get("train_questions", [])
total_questions = len(train_questions)

if total_questions == 0 and disable_train == False:
    st.error("❌ Nenhuma questão cadastrada para esta lição.")
    st.stop()

# ==================================
# 🔹 Lógica de Estado do Treino (Sem mudança)
# ==================================
if "current_lesson_id" not in st.session_state or st.session_state.current_lesson_id != lesson["id"]:
    st.session_state.current_lesson_id = lesson["id"]
    st.session_state.treino_q_index = 0
    st.session_state.treino_corrects = 0
    st.session_state.treino_feedback = ""
    st.session_state.treino_answered = False
    st.session_state.treino_finished = False

st.divider()

# ==================================
# 🔹 Loop de Treino (Sem mudança)
# ==================================
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
    
    min_acertos = max(1, int(total * 0.7)) 

    if corrects >= min_acertos:
        # (Chamada do manager continua igual)
        manager.set_train_ok(user, materia_key, lesson["id"])
        st.success("🏆 Treino aprovado!")
        st.balloons()
    else:
        # (Chamada do manager continua igual)
        manager.add_reforco(user, lesson["id"]) 
        st.warning("⚠️ Treino não aprovado. Este tema foi adicionado ao modo 'Reforço' para revisão.")
    
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
# MUDANÇA AQUI: Lê o 'len' (tamanho) da nova lista
total_treinos_concluidos = len(progress[user][materia_key].get("treinos_ok_list", []))
total_licoes_materia = len(subs) if subs else 1 

st.divider()
st.markdown(f"🏆 **Treinos concluídos em {materia}:** {total_treinos_concluidos} / {total_licoes_materia}")
st.progress(min(total_treinos_concluidos / total_licoes_materia, 1.0))