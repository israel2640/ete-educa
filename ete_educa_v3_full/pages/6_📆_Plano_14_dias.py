import streamlit as st
import unicodedata
from engine import load_progress, save_progress, ensure_user

# ================================
# 🔹 Configuração da página
# ================================
st.set_page_config(page_title="📆 Plano de 14 Dias", page_icon="📆", layout="centered")
st.title("📆 Plano de 14 Dias — Reta Final para a ETE")
st.caption("Seu guia de metas diárias. Siga o plano e marque as tarefas ao completar.")

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
# 🔹 Estrutura base do plano (O NOVO GUIA)
# ================================
# Este plano foi criado com base no Edital (Conteúdo Programático) 
# Ele alterna matérias para evitar zerar uma delas 
plano_base = [
    # Semana 1: Fundações
    "**Português (Fundação):** 📘 Estudar e 🎯 Treinar a lição 'POR_01 - Compreensão de Texto'[cite: 177].",
    "**Matemática (Fundação):** 📘 Estudar e 🎯 Treinar as lições 'MAT_01 - Quatro Operações' [cite: 197] e 'MAT_02 - Frações'[cite: 198].",
    "**Português (Gramática Essencial):** 📘 Estudar e 🎯 Treinar 'POR_08 - Classes Gramaticais' [cite: 193] e 'POR_09 - Conectivos'[cite: 194].",
    "**Matemática (Obrigatório):** 📘 Estudar e 🎯 Treinar 'MAT_11 - Porcentagem' [cite: 206] e 'MAT_10 - Regra de Três'[cite: 205].",
    "**REVISÃO (Dia 1):** 🧠 Ir para a página de 'Reforço' e revisar os tópicos que você errou nos primeiros 4 dias.",
    "**Português (Gramática Chave):** 📘 Estudar e 🎯 Treinar 'POR_10 - Pontuação' [cite: 194] e 'POR_11 - Concordância'[cite: 195].",
    "**Matemática (Álgebra Essencial):** 📘 Estudar e 🎯 Treinar 'MAT_17 - Equações 1º Grau' [cite: 211] e 'MAT_18 - Sistemas Lineares'[cite: 212].",
    
    # Semana 2: Check-up e Tópicos Difíceis
    "**CHECKPOINT (Simulado 1):** ⏱️ Ir para a página 'Desafiar' e fazer um simulado curto (10 questões) de Português.",
    "**CHECKPOINT (Simulado 2):** ⏱️ Ir para a página 'Desafiar' e fazer um simulado curto (10 questões) de Matemática.",
    "**REVISÃO (Dia 2):** 🧠 Ir para a página de 'Reforço'. Seu simulado adicionou novos tópicos aqui. Revise-os!",
    "**Português (Tópico Difícil):** 📘 Estudar e 🎯 Treinar 'POR_12 - Crase'[cite: 195]. Use a 🤖 'Revisão com IA' se tiver dúvidas.",
    "**Matemática (Geometria):** 📘 Estudar e 🎯 Treinar 'MAT_19 - Ângulos' [cite: 213] e 'MAT_21 - Triângulos'[cite: 214].",
    "**REVISÃO FINAL (Prova!):** ⏱️ Ir para a página 'Desafiar' e fazer um simulado completo (20 questões)[cite: 62].",
    "**DESCANSO E REVISÃO LEVE:** 🧠 Zerar a lista de 'Reforço' pela última vez e usar a 🤖 'Revisão com IA' para dúvidas finais."
]

# ================================
# 🔹 Exibir plano interativo
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
        # O texto da tarefa (com markdown)
        st.markdown(f"**Dia {dia}:** {tarefa}")
        
        # --- LÓGICA "INTELIGENTE" DE DICAS CONTEXTUAIS ---
        
        # Dica para 'Estudar' e 'Treinar'
        if "Estudar" in tarefa or "Treinar" in tarefa:
            st.info("💡 **Ação:** Vá para as páginas 📘 Estudar e 🎯 Treinar para completar esta meta.")
        
        # Dica para 'Reforço'
        elif "Reforço" in tarefa:
            if reforco_count == 0:
                st.success("🎉 **Status:** Você não tem nenhum item pendente no reforço. Parabéns!")
            else:
                st.warning(f"👉 **Ação:** Vá para a página 🧠 Reforço. Você tem **{reforco_count}** itens para revisar.")
        
        # Dica para 'Desafiar' (Simulado)
        elif "Desafiar" in tarefa or "Simulado" in tarefa:
            st.info(f"👉 **Ação:** Vá para a página ⏱️ Desafiar. (Você já completou {simulados_feitos} simulados).")
        
        # Dica para 'Revisão com IA'
        elif "Revisão com IA" in tarefa:
            st.info("💡 **Ação:** Vá para a página 🤖 Revisão com IA para tirar suas últimas dúvidas.")
        
        else:
            pass # Não mostra dica para a tarefa de "Descansar"

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
    st.success("🎉 Parabéns! Você completou todo o plano de 14 dias!")
    st.balloons()