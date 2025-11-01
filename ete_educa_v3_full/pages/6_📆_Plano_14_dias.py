import streamlit as st
import unicodedata
from engine import load_progress, save_progress, ensure_user

# ================================
# 🔹 Função auxiliar
# ================================
def normalizar_materia(nome: str) -> str:
    """Remove acentos e converte para minúsculas."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', nome.lower())
        if unicodedata.category(c) != 'Mn'
    )

# ================================
# 🔹 Configuração da página
# ================================
st.set_page_config(page_title="📆 Plano de 14 Dias", page_icon="📆", layout="centered")
st.title("📆 Plano de 14 Dias — Reta Final para a ETE")

usuario = st.text_input("Aluno(a):", value="aluna1")
progress = load_progress()
ensure_user(progress, usuario)

materia = st.selectbox("Matéria", ["Português", "Matemática"], index=0)
materia_key = normalizar_materia(materia)

if materia_key not in progress[usuario]:
    progress[usuario][materia_key] = {"badges": [], "treinos_ok": 0, "erros": []}
    save_progress(progress)

progresso_materia = progress[usuario][materia_key]

# ================================
# 🔹 Estrutura base do plano
# ================================
plano_base = [
    "Revisar mini-aulas básicas",
    "Treinar lições 1 e 2",
    "Corrigir erros da lista de reforço",
    "Fazer 3 treinos curtos",
    "Assistir vídeos ou ler resumos",
    "Revisar Português e Matemática alternadamente",
    "Fazer 1 simulado (50% das questões)",
    "Rever erros e anotar dúvidas",
    "Refazer treinos fracos",
    "Treinar redação e interpretação",
    "Refazer simulado completo",
    "Analisar tempo de prova",
    "Revisar tudo rapidamente",
    "Descansar e revisar anotações leves"
]

# ================================
# 🔹 Exibir plano interativo
# ================================
st.subheader(f"📚 Plano de Estudos — {materia}")
st.caption("Marque os dias conforme for completando. Seu progresso será salvo automaticamente.")

if "plano" not in progresso_materia:
    progresso_materia["plano"] = {dia+1: False for dia in range(14)}

for dia, tarefa in enumerate(plano_base, start=1):
    concluido = progresso_materia["plano"].get(str(dia), False)
    novo_estado = st.checkbox(f"Dia {dia}: {tarefa}", value=concluido)
    progresso_materia["plano"][str(dia)] = novo_estado

save_progress(progress)

# ================================
# 🔹 Barra de progresso
# ================================
concluidos = sum(1 for d in progresso_materia["plano"].values() if d)
porcentagem = int((concluidos / 14) * 100)

st.progress(concluidos / 14)
st.info(f"✅ Você completou **{concluidos}/14 dias** ({porcentagem}%) do plano de {materia}.")

if porcentagem == 100:
    st.success("🎉 Parabéns! Você completou todo o plano de 14 dias! Está pronta(o) para a ETE!")
