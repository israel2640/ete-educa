import streamlit as st
import unicodedata
# MUDANÇA 1: Imports atualizados
from engine import get_progress_manager 

# ================================
# 🔹 Configuração da página
# ================================
st.set_page_config(page_title="Plano 14 Dias - Rota da Aprovação", layout="centered")
st.title("📆 Rota da Aprovação (14 Dias)")
st.caption("Seu guia de estudo diário, completo e guiado, cobrindo 100% do edital.")

# ================================
# 🔹 Carregar dados e verificar usuário
# ================================
# MUDANÇA 2: Usando o Gerente para carregar
manager = get_progress_manager()
progress = manager.get_progress()

# --- BLOCO DE VERIFICAÇÃO DE PERFIL ---
if "user" not in st.session_state or not st.session_state.user:
    st.error("Ops! Você precisa selecionar ou criar um perfil na página principal (🎓 ETE_Educa v4) primeiro.")
    st.warning("Por favor, retorne à página principal para fazer o login.")
    st.stop() 

usuario = st.session_state.user
st.info(f"Aluno(a) logado: **{usuario}**") 

# MUDANÇA 3: Chamando o método do gerente
manager.ensure_user(usuario, "") # Garante que o usuário existe
# --- FIM DO BLOCO ---

# ================================
# 🔹 AVISO IMPORTANTE
# ================================
st.success(
    "**Este é o seu guia completo para a aprovação!**\n\n"
    "Ele cobre **100% dos tópicos** do edital para garantir que você não zere nenhuma matéria. "
    "A carga diária é maior, mas o foco é total na sua aprovação em 14 dias.",
    icon="🎯"
)
st.divider()

# ================================
# 🔹 Carregar dados de progresso do aluno
# ================================
user_progress = progress[usuario]
progresso_plano = user_progress.get("plano_14_dias", {str(dia+1): False for dia in range(14)})
reforco_count = len(user_progress.get("reforco", []))

# ================================
# 🔹 Estrutura base do plano (O NOVO GUIA COMPLETO E GUIADO)
# ================================
plano_guiado_completo = [
    # --- SEMANA 1: FUNDAÇÕES E ALTO IMPACTO ---
    {
        "dia": 1, "titulo": "Fundação (Port/Mat)", "tarefa": "POR_01, MAT_01, MAT_02",
        "guia": [
            "**Passo 1:** Vá para 📘 **Estudar** e complete as 3 lições: 'POR_01 (Texto)', 'MAT_01 (Operações)' e 'MAT_02 (Frações)'.",
            "**Passo 2:** Vá para 🎯 **Treinar** e seja aprovado(a) nos treinos dessas 3 lições.",
            "**Passo 3:** Vá para ✨ **Modo Livre** e pratique 5 questões de 'Frações'."
        ]
    },
    {
        "dia": 2, "titulo": "Tópicos Obrigatórios (Mat)", "tarefa": "MAT_10, MAT_11",
        "guia": [
            "**Passo 1:** Vá para 📘 **Estudar** e complete as 2 lições: 'MAT_10 (Regra de Três)' e 'MAT_11 (Porcentagem)'.",
            "**Passo 2:** Vá para 🎯 **Treinar** e seja aprovado(a) nos treinos de ambas.",
            "**Passo 3:** Vá para ✨ **Modo Livre**, selecione 'Matemática' e pratique 5 questões de 'Porcentagem' e 5 de 'Regra de Três'."
        ]
    },
    {
        "dia": 3, "titulo": "Gramática Essencial (Port)", "tarefa": "POR_08, POR_09, POR_10",
        "guia": [
            "**Passo 1:** Vá para 📘 **Estudar** e complete as 3 lições: 'POR_08 (Classes)', 'POR_09 (Conectivos)' e 'POR_10 (Pontuação)'.",
            "**Passo 2:** Vá para 🎯 **Treinar** e seja aprovado(a) nos treinos de todas elas.",
            "**Passo 3:** Vá para ✨ **Modo Livre** e pratique 5 questões de 'Pontuação'."
        ]
    },
    {
        "dia": 4, "titulo": "Álgebra Essencial (Mat)", "tarefa": "MAT_17, MAT_18",
        "guia": [
            "**Passo 1:** Vá para 📘 **Estudar** e complete as 2 lições: 'MAT_17 (Equação 1º Grau)' e 'MAT_18 (Sistemas Lineares)'.",
            "**Passo 2:** Vá para 🎯 **Treinar** e seja aprovado(a) nos treinos de ambas.",
            "**Passo 3:** Vá para ✨ **Modo Livre** e pratique 5 questões de 'Equações 1º Grau'."
        ]
    },
    {
        "dia": 5, "titulo": "Gramática Chave (Port)", "tarefa": "POR_11, POR_12",
        "guia": [
            "**Passo 1:** Vá para 📘 **Estudar** e complete as 2 lições: 'POR_11 (Concordância)' e 'POR_12 (Crase)'.",
            "**Passo 2:** Vá para 🎯 **Treinar** e seja aprovado(a) nos treinos de ambas.",
            "**Passo 3:** Vá para ✨ **Modo Livre** e pratique 5 questões de 'Crase'."
        ]
    },
    {
        "dia": 6, "titulo": "Geometria Básica (Mat)", "tarefa": "MAT_19, MAT_20, MAT_21",
        "guia": [
            "**Passo 1:** Vá para 📘 **Estudar** e complete as 3 lições: 'MAT_19 (Ângulos)', 'MAT_20 (Polígonos)' e 'MAT_21 (Triângulos)'.",
            "**Passo 2:** Vá para 🎯 **Treinar** e seja aprovado(a) nos treinos de todas elas.",
            "**Passo 3:** Vá para ✨ **Modo Livre** e pratique 5 questões de 'Ângulos' ou 'Triângulos'."
        ]
    },
    {
        "dia": 7, "titulo": "REVISÃO (Dia 1) + Simulado", "tarefa": "Zerar o reforço e fazer 1 simulado.",
        "guia": [
            f"**Passo 1:** Vá para a página 🧠 **Reforço**. Você tem **{reforco_count}** itens. Revise e marque-os como concluídos lá.",
            "**Passo 2:** Vá para a página ⏱️ **Desafiar** e faça 1 simulado (10 questões) da matéria que tiver MAIS dificuldade.",
            "**Passo 3:** Descanse!"
        ]
    },
    
    # --- SEMANA 2: TÓPICOS INTERMEDIÁRIOS E FINAIS ---
    {
        "dia": 8, "titulo": "Tópicos Textuais (Port)", "tarefa": "POR_02, POR_03, POR_04",
        "guia": [
            "**Passo 1:** Vá para 📘 **Estudar** e complete as 3 lições: 'POR_02 (Textualidade)', 'POR_03 (Gêneros)' e 'POR_04 (Semântica)'.",
            "**Passo 2:** Vá para 🎯 **Treinar** e seja aprovado(a) nos treinos de todas elas."
        ]
    },
    {
        "dia": 9, "titulo": "Números e Medidas (Mat)", "tarefa": "MAT_03, MAT_04, MAT_05, MAT_07",
        "guia": [
            "**Passo 1:** Vá para 📘 **Estudar** e complete as 4 lições: 'MAT_03 (Decimais)', 'MAT_04 (Potência)', 'MAT_05 (Raiz Exata)' e 'MAT_07 (Medidas)'.",
            "**Passo 2:** Vá para 🎯 **Treinar** e seja aprovado(a) nos treinos de todas elas."
        ]
    },
    {
        "dia": 10, "titulo": "Tópicos Estilísticos (Port)", "tarefa": "POR_05, POR_06, POR_07",
        "guia": [
            "**Passo 1:** Vá para 📘 **Estudar** e complete as 3 lições: 'POR_05 (Figuras)', 'POR_06 (Variações)' e 'POR_07 (Palavras)'.",
            "**Passo 2:** Vá para 🎯 **Treinar** e seja aprovado(a) nos treinos de todas elas."
        ]
    },
    {
        "dia": 11, "titulo": "Álgebra Intermediária (Mat)", "tarefa": "MAT_13, MAT_14, MAT_15, MAT_16",
        "guia": [
            "**Passo 1:** Vá para 📘 **Estudar** e complete as 4 lições: 'MAT_13 (Polinômios)', 'MAT_14 (Notáveis)', 'MAT_15 (Fatoração)' e 'MAT_16 (Radiciação)'.",
            "**Passo 2:** Vá para 🎯 **Treinar** e seja aprovado(a) nos treinos de todas elas."
        ]
    },
    {
        "dia": 12, "titulo": "Matemática Avançada (Mat)", "tarefa": "MAT_06, MAT_08, MAT_12, MAT_24, MAT_25",
        "guia": [
            "**Passo 1:** Vá para 📘 **Estudar** e complete as 5 lições: 'MAT_06 (Expressões)', 'MAT_08 (Razão)', 'MAT_12 (Médias)', 'MAT_24 (Raiz Aproximada)' e 'MAT_25 (Outras Médias)'.",
            "**Passo 2:** Vá para 🎯 **Treinar** e seja aprovado(a) nos treinos de todas elas.",
            "**Passo 3:** Use a 🤖 **Revisão com IA** para tirar dúvidas sobre 'Média Harmônica' (MAT_25)."
        ]
    },
    {
        "dia": 13, "titulo": "Geometria Avançada (Mat)", "tarefa": "MAT_09, MAT_22, MAT_23",
        "guia": [
            "**Passo 1:** Vá para 📘 **Estudar** e complete as 3 lições: 'MAT_09 (Divisão Proporcional)', 'MAT_22 (Semelhança)' e 'MAT_23 (Cevianas)'.",
            "**Passo 2:** Vá para 🎯 **Treinar** e seja aprovado(a) nos treinos de todas elas."
        ]
    },
    {
        "dia": 14, "titulo": "SIMULADO FINAL E REVISÃO", "tarefa": "Simulado Completo (20q) + Zerar Reforço.",
        "guia": [
            "**Passo 1:** Vá para ⏱️ **Desafiar** e faça 1 simulado de 20 questões (10 de cada matéria, se possível, ou 1 de 20).",
            f"**Passo 2:** Vá para 🧠 **Reforço**. Zere sua lista! Você tem **{reforco_count}** itens.",
            "**Passo 3:** Descanse. Você cobriu 100% do edital. Boa prova!"
        ]
    }
]


# ================================
# 🔹 Exibir plano interativo (NOVO LAYOUT)
# ================================
st.subheader("🚀 Seu Guia Diário (100% do Edital)")
st.caption("Marque a meta do dia ao completar o guia passo a passo.")

if "plano_14_dias" not in user_progress:
     user_progress["plano_14_dias"] = progresso_plano
     # MUDANÇA 4: Salvando com o Gerente
     manager.save_progress() 

# Itera sobre o plano base e exibe os checkboxes
for item in plano_guiado_completo:
    dia_str = str(item["dia"])
    concluido = progresso_plano.get(dia_str, False)
    
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        # O checkbox para marcar a tarefa
        novo_estado = st.checkbox("", value=concluido, key=f"dia_{item['dia']}", label_visibility="collapsed")
    
    with col2:
        # O texto da tarefa (com markdown)
        st.markdown(f"**Dia {item['dia']}: {item['titulo']}**")
        st.caption(f"Lições do dia: {item['tarefa']}")
        
        # --- O GUIA PRESCRITIVO (DENTRO DE UM EXPANDER) ---
        with st.expander("Ver o Guia Passo a Passo 🚀"):
            for passo in item["guia"]:
                # Atualiza dinamicamente o contador de reforço no texto do guia
                passo_atualizado = passo.replace(f"{reforco_count}", f"**{reforco_count}**")
                st.markdown(f"&nbsp;&nbsp;&nbsp;• {passo_atualizado}")
        
    # Salva o novo estado SE ele mudou
    if progresso_plano.get(dia_str) != novo_estado:
        progresso_plano[dia_str] = novo_estado
        # MUDANÇA 5: Salvando com o Gerente
        manager.save_progress() # Salva a cada clique
    
    st.divider()

# ================================
# 🔹 Barra de progresso
# ================================
concluidos = sum(1 for d in progresso_plano.values() if d)
porcentagem = int((concluidos / 14) * 100)

st.progress(concluidos / 14)
st.info(f"✅ Você completou **{concluidos}/14 dias** ({porcentagem}%) do seu plano de estudos focado.")

if porcentagem == 100:
    st.success("🎉 Parabéns! Você completou todo o plano de 14 dias!")
    st.balloons()