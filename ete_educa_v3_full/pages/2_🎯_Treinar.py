import streamlit as st
import unicodedata
from engine import (
    load_lessons, load_progress, save_progress, ensure_user,
    set_train_ok, shuffled_options, add_reforco, set_studied
)

# ====== Configuração ======
st.set_page_config(page_title="🎯 Treinar — ETE Educa", page_icon="🎯", layout="centered")
st.header("🎯 Treinar — 3 perguntas por lição")

# ====== CORREÇÃO: Função auxiliar padronizada ======
def normalizar_materia(nome: str) -> str:
    """Remove acentos e padroniza para minúsculas."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', nome.lower())
        if unicodedata.category(c) != 'Mn'
    )
# --- FIM DA CORREÇÃO ---

# ====== Carregar dados ======
lessons = load_lessons()
progress = load_progress()
user = st.text_input("Aluno(a)", value="aluna1")
ensure_user(progress, user)

materia = st.selectbox("Matéria", ["Português", "Matemática"], index=0)
materia_key = normalizar_materia(materia)

subs = [l for l in lessons if l.get("subject", "").lower() == materia_key]

# ====== Ordenar lições ======
# 'badges' agora contém todas as lições que foram 'estudadas'
studied = set(progress[user].get(materia_key, {}).get("badges", []))
ordered = [l for l in subs if l["id"] in studied] + [l for l in subs if l["id"] not in studied]

if not ordered:
    st.warning(f"Nenhuma lição disponível para {materia}. Vá ao modo 'Estudar' primeiro.")
    st.stop()

lesson = st.selectbox("Lição", ordered, format_func=lambda x: f"{'✅ ' if x['id'] in studied else '🔒 '}{x['id']} — {x['title']}")

# ====== Verificação de estudo ======
if lesson["id"] not in studied:
    st.warning("📘 Estude esta lição primeiro (na página 'Estudar') para liberar o treino.")
    disable_train = True
else:
    st.success("✅ Lição estudada! Você pode treinar.")
    disable_train = False

# ====== Execução do treino ======
corrects = 0
train_questions = lesson.get("train_questions", [])
total = len(train_questions)

if total == 0:
    st.error("❌ Nenhuma questão cadastrada para esta lição.")
    st.stop()

respostas_usuario = {}

# Usar um formulário para evitar que os botões "Confirmar" recarreguem a página
with st.form("treino_form"):
    for i, q in enumerate(train_questions, start=1):
        st.markdown(f"**{i}. {q['q']}**")
        opts = shuffled_options(q["opts"])
        
        key = f"t_{lesson['id']}_{i}"
        ch = st.radio("Escolha:", opts, key=key, disabled=disable_train, index=None)
        respostas_usuario[key] = (ch, q["ans"], q.get("exp", "Sem explicação."))

    submitted = st.form_submit_button("Finalizar treino", disabled=disable_train)

# ====== Finalização (Fora do formulário) ======
if submitted:
    corrects = 0
    # Processar respostas
    for key, (resposta_aluna, gabarito, explicacao) in respostas_usuario.items():
        if resposta_aluna == gabarito:
            st.success(f"✅ Questão '{key}' correta! {explicacao}")
            corrects += 1
        else:
            st.error(f"❌ Questão '{key}' incorreta. A resposta era '{gabarito}'.")
            st.info(explicacao)
            
    st.divider()
    
    # Mínimo de 2 acertos ou 70%
    min_acertos = max(2, int(total * 0.7)) 

    if corrects >= min_acertos:
        set_train_ok(progress, user, materia_key, lesson["id"])
        st.success(f"🏆 Treino aprovado! ({corrects}/{total})")
        st.balloons()
    else:
        add_reforco(progress, user, lesson["id"])
        st.warning(f"⚠️ Treino não aprovado. ({corrects}/{total}) Este tema foi adicionado ao modo 'Reforço' para revisão.")
    
    save_progress(progress)

# ====== Indicador de progresso ======
if materia_key not in progress[user]:
    progress[user][materia_key] = {"treinos_ok": 0}

total_treinos_concluidos = progress[user][materia_key].get("treinos_ok", 0)
total_licoes_materia = len(subs) if subs else 1 # Evita divisão por zero

st.divider()
st.markdown(f"🏆 **Treinos concluídos em {materia}:** {total_treinos_concluidos} / {total_licoes_materia}")
st.progress(min(total_treinos_concluidos / total_licoes_materia, 1.0))