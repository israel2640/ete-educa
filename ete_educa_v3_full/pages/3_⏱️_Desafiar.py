import streamlit as st
import random, base64, time
import unicodedata # <--- Importar
from data.simulado_loader import gerar_prova 
from engine import load_progress, save_progress, ensure_user 

# ====== Configuração ======
st.set_page_config(page_title="⏱️ Desafiar — ETE Educa", page_icon="⏱️", layout="centered")
st.title("⏱️ Desafiar — Simulado Inteligente")
st.write("Responda ao simulado completo com base nas provas oficiais da ETE (2022–2024) e veja seu desempenho!")

# ====== Estado global ======
if "fase" not in st.session_state:
    st.session_state.fase = "inicio"
    st.session_state.questoes = []
    st.session_state.q_atual = 0
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.feedback = "" # NOVO: Para guardar o feedback

progress = load_progress()
usuario = st.text_input("Nome da aluna(o):", value="aluna1")
ensure_user(progress, usuario)

# ====== CORREÇÃO: Função auxiliar padronizada ======
def normalizar_materia(nome: str) -> str:
    """Remove acentos e padroniza para minúsculas."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', nome.lower())
        if unicodedata.category(c) != 'Mn'
    )
# --- FIM DA CORREÇÃO ---

# ====== Fase 1: Seleção ======
if st.session_state.fase == "inicio":
    materia = st.radio("Escolha a matéria:", ["Português", "Matemática"])
    n_questoes = st.slider("Número de questões no simulado:", 5, 20, 10)

    if st.button("🎯 Iniciar Simulado"):
        st.session_state.questoes = gerar_prova(materia, n_questoes)
        if not st.session_state.questoes:
            st.error("Não há questões suficientes em 'data/provas_db.py' para gerar o simulado. Adicione mais questões.")
        else:
            st.session_state.q_atual = 0
            st.session_state.acertos = 0
            st.session_state.erros = 0
            st.session_state.feedback = ""
            st.session_state.materia = materia
            st.session_state.fase = "questao"
            st.rerun()

# ====== Fase 2: Questões ======
elif st.session_state.fase == "questao":
    if st.session_state.q_atual < len(st.session_state.questoes):
        q = st.session_state.questoes[st.session_state.q_atual]
        st.subheader(f"Questão {st.session_state.q_atual + 1}/{len(st.session_state.questoes)} — {q['tema']}")
        st.markdown(q["pergunta"])
        
        # Garante que alternativas existam
        if "alternativas" not in q or not q["alternativas"]:
            st.error("Erro: Questão sem alternativas cadastradas.")
            st.session_state.q_atual += 1 # Pula questão
        else:
            resposta = st.radio("Escolha sua resposta:", q["alternativas"], key=f"resp_{st.session_state.q_atual}", index=None)

            # --- LÓGICA DE RESPOSTA MODIFICADA ---
            if st.button("Responder"):
                if resposta == q["correta"]:
                    st.session_state.acertos += 1
                    st.session_state.feedback = "✅ Correto!"
                else:
                    st.session_state.erros += 1
                    st.session_state.feedback = (
                        f"❌ Errado! A resposta correta é **{q['correta']}**.\n\n"
                        f"**Explicação:** {q.get('explicacao', 'Leia novamente este tema no modo Estudar.')}"
                    )
                
                st.session_state.fase = "feedback_simulado" # Muda para a nova fase
                st.rerun() # Recarrega para mostrar o feedback
    else:
        st.session_state.fase = "resultado"
        st.rerun()

# --- NOVA FASE DE FEEDBACK ---
elif st.session_state.fase == "feedback_simulado":
    st.subheader(f"Questão {st.session_state.q_atual + 1}/{len(st.session_state.questoes)}")
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)
    
    if st.button("Próxima Questão ➡️"):
        st.session_state.q_atual += 1
        st.session_state.fase = "questao"
        st.session_state.feedback = "" # Limpa o feedback
        st.rerun()


# ====== Fase 3: Resultado ======
elif st.session_state.fase == "resultado":
    total = st.session_state.acertos + st.session_state.erros
    st.header("📊 Resultado do Simulado")
    
    if total == 0:
        st.warning("Nenhuma questão foi respondida.")
        st.session_state.fase = "inicio"
        st.button("Voltar")
        
    else:
        st.write(f"✅ Acertos: {st.session_state.acertos}")
        st.write(f"❌ Erros: {st.session_state.erros}")
        perc = st.session_state.acertos / total

        if perc >= 0.9:
            nivel = "🥇 Ouro"
        elif perc >= 0.7:
            nivel = "🥈 Prata"
        else:
            nivel = "🥉 Bronze"

        st.progress(perc)
        st.markdown(f"**Desempenho:** {nivel} ({perc*100:.1f}%)")

        if perc >= 0.7:
            st.success("🎉 Excelente! Você atingiu o nível mínimo para a ETE!")
            st.balloons()
        else:
            st.warning("📘 Continue estudando as lições e refaça o simulado para subir de nível.")

        # --- ESTA É A CORREÇÃO DEFINITIVA ---
        materia_key = normalizar_materia(st.session_state.materia)
        # --- FIM DA CORREÇÃO ---
        
        if usuario not in progress:
             ensure_user(progress, usuario) # Garante que existe
             
        progress[usuario][materia_key]["simulados"] = progress[usuario][materia_key].get("simulados", 0) + 1
        save_progress(progress)

        if st.button("🔁 Refazer Simulado"):
            st.session_state.fase = "inicio"
            st.rerun()