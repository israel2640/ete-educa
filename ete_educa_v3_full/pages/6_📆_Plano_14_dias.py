import streamlit as st
import unicodedata
from engine import load_progress, save_progress, ensure_user

# ================================
# 🔹 Configuração da página
# ================================
st.set_page_config(page_title="📆 Plano de 14 Dias", page_icon="📆", layout="centered")
st.title("📆 Plano de 14 Dias — Reta Final para a ETE")

# ================================
# 🔹 Carregar dados e verificar usuário
# ================================
progress = load_progress()

# --- NOVO BLOCO DE VERIFICAÇÃO DE PERFIL ---
if "user" not in st.session_state or not st.session_state.user:
    st.error("Ops! Você precisa selecionar ou criar um perfil na página principal (🎓 ETE_Educa v4) primeiro.")
    st.warning("Por favor, retorne à página principal para fazer o login.")
    st.stop() # Para a execução da página

usuario = st.session_state.user
st.info(f"Aluno(a) logado: **{usuario}**") # Mostra quem está logado
ensure_user(progress, usuario) # Garante que o usuário ainda existe no JSON
# --- FIM DO NOVO BLOCO ---

# --- LÓGICA CORRIGIDA ---
# O plano de 14 dias agora é ÚNICO para o usuário, não mais separado por matéria.
if "plano_14_dias" not in progress[usuario]:
    progress[usuario]["plano_14_dias"] = {str(dia+1): False for dia in range(14)}
    save_progress(progress)

progresso_plano = progress[usuario]["plano_14_dias"]
# --- FIM DA CORREÇÃO LÓGICA ---

# ================================
# 🔹 Estrutura base do plano
# ================================
plano_base = [
    "Revisar mini-aulas básicas (Português)",
    "Treinar lições 1 e 2 (Matemática)",
    "Corrigir erros da lista de reforço",
    "Fazer 3 treinos curtos (Português)",
    "Assistir vídeos ou ler resumos (Matemática)",
    "Revisar Português e Matemática alternadamente",
    "Fazer 1 simulado (50% das questões)",
    "Rever erros e anotar dúvidas",
    "Refazer treinos fracos (Matemática)",
    "Treinar interpretação de texto (Português)",
    "Refazer simulado completo",
    "Analisar tempo de prova",
    "Revisar tudo rapidamente",
    "Descansar e revisar anotações leves"
]

# ================================
# 🔹 Exibir plano interativo
# ================================
st.subheader("📚 Plano de Estudos — Reta Final")
st.caption("Marque os dias conforme for completando. Seu progresso será salvo automaticamente.")

# Itera sobre o plano base e exibe os checkboxes
for dia, tarefa in enumerate(plano_base, start=1):
    dia_str = str(dia)
    concluido = progresso_plano.get(dia_str, False)
    
    novo_estado = st.checkbox(f"Dia {dia}: {tarefa}", value=concluido, key=f"dia_{dia}")
    
    # Salva o novo estado SE ele mudou
    if progresso_plano.get(dia_str) != novo_estado:
        progresso_plano[dia_str] = novo_estado
        save_progress(progress) # Salva a cada clique

# ================================
# 🔹 Barra de progresso
# ================================
concluidos = sum(1 for d in progresso_plano.values() if d)
porcentagem = int((concluidos / 14) * 100)

st.progress(concluidos / 14)
st.info(f"✅ Você completou **{concluidos}/14 dias** ({porcentagem}%) do seu plano de estudos.")

if porcentagem == 100:
    st.success("🎉 Parabéns! Você completou todo o plano de 14 dias! Está pronta(o) para a ETE!")