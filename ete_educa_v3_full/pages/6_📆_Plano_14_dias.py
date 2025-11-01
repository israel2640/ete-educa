import streamlit as st
import unicodedata
from engine import load_progress, save_progress, ensure_user

# ================================
# 🔹 Configuração da página
# ================================
st.set_page_config(page_title="📆 Plano de 14 Dias", page_icon="📆", layout="centered")
st.title("📆 Plano de 14 Dias — Reta Final para a ETE")
st.caption("Seu guia de metas diárias. Marque os dias conforme for completando.")

# ================================
# 🔹 Carregar dados e verificar usuário
# ================================
progress = load_progress()

# --- BLOCO DE VERIFICAÇÃO DE PERFIL ---
if "user" not in st.session_state or not st.session_state.user:
    st.error("Ops! Você precisa selecionar ou criar um perfil na página principal (🎓 ETE_Educa v4) primeiro.")
    st.warning("Por favor, retorne à página principal para fazer o login.")
    st.stop() 

usuario = st.session_state.user
st.info(f"Aluno(a) logado: **{usuario}**") 
ensure_user(progress, usuario, "") # Garante que o usuário existe
# --- FIM DO BLOCO ---

# ================================
# 🔹 Carregar dados de progresso do aluno
# ================================
user_progress = progress[usuario]
# Carrega o plano salvo (ex: {"1": true, "2": false, ...})
progresso_plano = user_progress.get("plano_14_dias", {str(dia+1): False for dia in range(14)})

# Carrega o número de itens no reforço
reforco_count = len(user_progress.get("reforco", []))
# Carrega o número de simulados feitos
simulados_feitos = user_progress.get("portugues", {}).get("simulados", 0) + user_progress.get("matematica", {}).get("simulados", 0)


# ================================
# 🔹 Estrutura base do plano (A lista de tarefas)
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
# 🔹 Exibir plano interativo (A NOVA LÓGICA)
# ================================
st.subheader("📚 Seu Plano de Estudos")

# Garante que o progresso do plano seja salvo no formato correto
if "plano_14_dias" not in user_progress:
     user_progress["plano_14_dias"] = progresso_plano
     save_progress(progress)

# Itera sobre o plano base e exibe os checkboxes
for dia, tarefa in enumerate(plano_base, start=1):
    dia_str = str(dia)
    concluido = progresso_plano.get(dia_str, False)
    
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        # O checkbox para marcar a tarefa
        novo_estado = st.checkbox("", value=concluido, key=f"dia_{dia}", label_visibility="collapsed")
    
    with col2:
        # O texto da tarefa
        st.markdown(f"**Dia {dia}: {tarefa}**")
        
        # --- AQUI ESTÁ A LÓGICA "INTELIGENTE" ---
        
        # Dica para tarefas de Estudo/Treino
        if "mini-aulas" in tarefa or "Treinar lições" in tarefa or "treinos curtos" in tarefa:
            st.info("💡 Vá para as páginas 📘 Estudar e 🎯 Treinar para completar esta meta.")
        
        # Dica para a tarefa de Reforço
        elif "Corrigir erros" in tarefa:
            if reforco_count == 0:
                st.success("🎉 Você não tem nenhum item pendente no reforço. Parabéns!")
            else:
                st.warning(f"👉 Você tem **{reforco_count}** itens na sua lista! Vá para a página 🧠 Reforço para revisar.")
        
        # Dica para a tarefa de Simulado
        elif "simulado" in tarefa:
            st.info(f"👉 Vá para a página ⏱️ Desafiar. Você já completou {simulados_feitos} simulados.")

    # Salva o novo estado SE ele mudou
    if progresso_plano.get(dia_str) != novo_estado:
        progresso_plano[dia_str] = novo_estado
        save_progress(progress) # Salva a cada clique
    
    st.divider()

# ================================
# 🔹 Barra de progresso
# ================================
concluidos = sum(1 for d in progresso_plano.values() if d)
porcentagem = int((concluidos / 14) * 100)

st.progress(concluidos / 14)
st.info(f"✅ Você completou **{concluidos}/14 dias** ({porcentagem}%) do seu plano de estudos.")

if porcentagem == 100:
    st.success("🎉 Parabéns! Você completou todo o plano de 14 dias! Está pronta(o) para a ETE!")