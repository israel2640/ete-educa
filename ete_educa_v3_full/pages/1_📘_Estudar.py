import streamlit as st
from engine import QuizEngine, load_progress, save_progress, set_studied, ensure_user
from ai_helpers import explain_like_coach
# CORREÇÃO: Importar 'questoes' da pasta 'data'
from data.questoes import questoes_portugues, questoes_matematica

# =====================================================
# 🔹 Configuração da página
# =====================================================
st.set_page_config(page_title="📘 Estudar — ETE Educa", page_icon="📘", layout="centered")
st.title("📘 Estudar — Mini Aulas Interativas")
st.caption("Aprenda os principais temas do edital da ETE com explicações da IA 🤖")

# =====================================================
# 🔹 Carregar dados de progresso e usuário
# =====================================================
progress = load_progress()
# O usuário é pego da tela principal
user = st.session_state.get("user", "aluna1") 
ensure_user(progress, user)

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
# 🔹 Inicialização de estado
# =====================================================
# Reinicia o progresso se a matéria mudar
if "materia_anterior" not in st.session_state or st.session_state.materia_anterior != materia:
    st.session_state.fase = "aula"
    st.session_state.questao_atual = 0
    st.session_state.feedback = ""
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.materia_anterior = materia

# =====================================================
# 🔹 Controle de fluxo de estudo
# =====================================================
if st.session_state.questao_atual >= len(questoes):
    st.success("🎉 Parabéns! Você completou todas as lições disponíveis!")
    st.balloons()
    st.session_state.fase = "final"
    if st.button("Recomeçar?"):
        st.session_state.questao_atual = 0
        st.session_state.fase = "aula"
        st.rerun()

else:
    # Ajusta o 'atual' do engine para bater com o 'atual' do app
    engine.atual = st.session_state.questao_atual
    
    questao = questoes[st.session_state.questao_atual]

    # Compatibilidade de campos (title ou tema)
    titulo = questao.get("title") or questao.get("tema", "Tema não informado")
    texto_aula = questao.get("lesson_text") or questao.get("texto", "Sem conteúdo disponível.")
    exemplo = questao.get("example") or questao.get("exemplo", "Sem exemplo disponível.")

    # =====================================================
    # 🧠 Etapa 1 — Mini Aula com IA
    # =====================================================
    if st.session_state.fase == "aula":
        st.subheader(f"📖 Mini Aula — {titulo}")
        st.write(texto_aula)
        st.info("💡 Exemplo: " + exemplo)

        # Explicação com IA (usando ai_helpers)
        if st.checkbox("Gerar explicação da IA (requer chave .env)"):
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
            st.rerun() # Usar rerun para atualizar a página

    # =====================================================
    # 🎯 Etapa 2 — Pergunta de Treino
    # =====================================================
    elif st.session_state.fase == "questao":
        st.subheader(f"🎯 Questão de Treino — {titulo}")
        
        # Garante que há 'train_questions'
        if not questao.get("train_questions"):
            st.error("Erro: Esta lição não tem 'train_questions' cadastradas.")
            st.session_state.fase = "feedback" # Pula para o feedback
        else:
            q = questao["train_questions"][0] # Pega a primeira questão de treino
            
            # Garante que 'opts' existe
            if "opts" not in q:
                 st.error("Erro: Pergunta de treino mal formatada (sem 'opts').")
                 st.session_state.fase = "feedback"
            else:
                resposta = st.radio("Escolha sua resposta:", q["opts"], key=f"q_{st.session_state.questao_atual}", index=None)
                
                if st.button("Responder"):
                    acertou, feedback = engine.responder(resposta)
                    st.session_state.feedback = feedback
                    if acertou:
                        st.session_state.acertos += 1
                    else:
                        st.session_state.erros += 1
                    
                    # *** CORREÇÃO CRÍTICA ***
                    # Marca a lição como 'estudada' para liberar o treino
                    set_studied(progress, user, materia_key, questao["id"])
                    save_progress(progress)
                    # *** FIM DA CORREÇÃO ***
                    
                    st.session_state.fase = "feedback"
                    st.rerun()

    # =====================================================
    # 📘 Etapa 3 — Feedback da IA
    # =====================================================
    elif st.session_state.fase == "feedback":
        st.subheader("📘 Revisão")
        st.markdown(st.session_state.feedback)
        
        if st.button("Próxima lição ➡️"):
            st.session_state.questao_atual += 1
            st.session_state.fase = "aula"
            st.session_state.feedback = "" # Limpa o feedback
            st.rerun()

# =====================================================
# 🔹 Rodapé de progresso (COM A CORREÇÃO)
# =====================================================
st.divider()
total_licoes = len(questoes)
if total_licoes > 0:
    # --- ESTA É A LINHA CORRIGIDA ---
    progresso_percentual = (st.session_state.questao_atual / total_licoes)
else:
    progresso_percentual = 0

st.markdown(f"**Progresso:** {st.session_state.questao_atual}/{total_licoes} lições estudadas.")
# Adicionamos min(..., 1.0) por segurança, para nunca passar de 1.0
st.progress(min(progresso_percentual, 1.0))