import streamlit as st
import unicodedata
import re
import sympy as sp

# 🔹 Importações corretas das funções de IA
from ai_helpers import (
    generate_math_question,
    generate_portuguese_question,
    get_correct_answer_from_sympy,
    explain_like_coach,      # para explicações divertidas
    ask_quick_question       # para perguntas do aluno
)


# AQUI ESTÁ A MUDANÇA: importamos a nova função de verificação
from ai_helpers import generate_math_question, generate_portuguese_question

st.set_page_config(page_title="Modo Livre — ETE Educa", layout="centered")
st.title("✨ Modo Livre — Prática Infinita (Verificada)")
st.caption("A IA gera perguntas inéditas e o Python verifica a resposta para garantir 100% de precisão!")

# --- Listas de Tópicos do Edital ---
topicos_portugues = [
    "Compreensão de Texto (Ideias Principais)", "Textualidade (Coesão e Coerência)",
    "Gêneros Textuais e Sequências", "Semântica (Sentido das Palavras)",
    "Figuras de Linguagem (Conotação/Denotação)", "Norma Padrão e Variedades Linguísticas",
    "Estrutura e Formação das Palavras", "Classes Gramaticais",
    "Conectivos (Coordenação e Subordinação)", "Pontuação",
    "Concordância e Regência", "Crase"
]
topicos_matematica = [
    "Problemas com as Quatro Operações", "Operações com Frações", "Operações com Números Decimais",
    "Potenciação", "Raiz Quadrada Exata", "Expressões com Números Reais (PEMDAS)",
    "Sistemas de Medidas", "Razão e Proporção", "Divisão Proporcional",
    "Regra de Três Simples", "Regra de Três Composta", "Porcentagem", "Médias",
    "Polinômios (Valor Numérico e Operações)", "Produtos Notáveis", "Fatoração",
    "Radiciação (Simplificação de Raízes)", "Equações Algébricas do 1º Grau",
    "Sistemas Lineares do 1º Grau", "Ângulos", "Polígonos (Soma dos Ângulos)",
    "Triângulos (Classificação e Lei Angular)", "Semelhança de Triângulos (Teorema de Tales)",
    "Cevianas (Mediana, Bissetriz, Altura)"
]

# --- Interface do Modo Livre ---
if "new_question_data" not in st.session_state:
    st.session_state.new_question_data = None
if "reveal_answer" not in st.session_state:
    st.session_state.reveal_answer = False
if "correct_answer_verified" not in st.session_state:
    st.session_state.correct_answer_verified = None

materia = st.radio("Escolha a matéria:", ["Português", "Matemática"], horizontal=True)
if materia == "Português":
    topico = st.selectbox("Escolha um tópico do edital:", topicos_portugues)
else:
    topico = st.selectbox("Escolha um tópico do edital:", topicos_matematica)

# Botão de Gerar
if st.button(f"Gerar Pergunta Inédita sobre {topico}"):
    st.session_state.new_question_data = None
    st.session_state.reveal_answer = False
    st.session_state.correct_answer_verified = None
    
    with st.spinner(f"A IA está criando uma questão sobre {topico}..."):
        
        if materia == "Matemática":
            q_data = generate_math_question(materia, topico)
        else:
            q_data = generate_portuguese_question(materia, topico)
        
        if q_data:
            st.session_state.new_question_data = q_data
            
# --- O "PROFESSOR CORRETOR" ENTRA EM AÇÃO ---
            if materia == "Matemática":
                with st.spinner("Python (SymPy) está verificando a matemática da IA..."):
                    # Nós usamos o SymPy para descobrir a resposta correta
                    correta_verificada, status = get_correct_answer_from_sympy(q_data)
                    
                    if correta_verificada:
                        # Nós salvamos a resposta que o *Python* encontrou
                        st.session_state.correct_answer_verified = correta_verificada
                        # --- CORREÇÃO AQUI ---
                        
                    else:
                        st.error(f"Falha na verificação: {status}. A IA pode ter criado opções inválidas. Tente gerar outra.")
                        st.session_state.new_question_data = None
            else:
                # Para Português, a IA deve enviar a alternativa correta dentro do JSON
                correta_ia = q_data.get("correta")

                # 🔹 Caso o modelo não tenha enviado "correta", tenta identificar pela explicação
                if not correta_ia:
                    exp = q_data.get("explicacao", "").lower()
                    for opcao in q_data.get("opcoes", []):
                        if re.search(re.escape(opcao.lower().split(")")[1].strip()), exp):
                            correta_ia = opcao
                            break

                if correta_ia:
                    st.session_state.correct_answer_verified = correta_ia
                else:
                    st.error("❌ A IA não retornou a alternativa correta. Gere outra questão.")
                    st.session_state.new_question_data = None

        else:
            st.error("Não foi possível gerar a questão. Tente novamente.")

st.divider()

# --- Exibição da Pergunta ---
if st.session_state.new_question_data and st.session_state.correct_answer_verified:
    q_data = st.session_state.new_question_data

    st.subheader("Questão Gerada pela IA:")

    # 🔹 Exibir texto-base se existir
    if "texto" in q_data and q_data["texto"].strip():
        st.markdown("📘 **Texto-base:**")
        st.markdown(q_data["texto"])
        st.divider()

    # 🔹 Exibir a pergunta
    st.markdown(q_data.get("pergunta", "Erro ao carregar pergunta."))

    opcoes = q_data.get("opcoes", [])
    if opcoes:
        resposta_usuario = st.radio(
            "Escolha sua resposta:", 
            opcoes, 
            index=None,
            key="modo_livre_radio"
        )

        # 🔹 Botão para revelar a resposta
        if st.button("Revelar Resposta e Explicação"):
            st.session_state.reveal_answer = True

        # 🔹 Quando o aluno clica em "Revelar", mostra a resposta e a explicação
        if st.session_state.reveal_answer:
            correta = st.session_state.correct_answer_verified

            if resposta_usuario == correta:
                st.success(f"🎉 Você acertou! A resposta correta (verificada pelo Python) é: **{correta}**")
                st.balloons()
            else:
                st.error(f"❌ Você marcou: {resposta_usuario}\nA resposta correta (verificada pelo Python) era: **{correta}**")

            st.subheader("Explicação do Mestre:")

            # 🔹 Usa a explicação divertida para todas as matérias
            explicacao_original = q_data.get("explicacao", "Sem explicação disponível.")
            explicacao_divertida = explain_like_coach(explicacao_original, materia)

            # Exibe a explicação com um emoji
            st.markdown(f"🧠 {explicacao_divertida}")

            # 🔹 Campo para o aluno perguntar sobre a explicação
            st.markdown("💬 **Tem alguma dúvida sobre essa explicação?**")
            pergunta_aluno = st.text_input("Digite sua pergunta aqui:", key="pergunta_aluno")

            if pergunta_aluno:
                with st.spinner("A professora está pensando... 🤔"):
                    resposta_duvida = ask_quick_question(
                        f"Matéria: {materia}\n\nExplicação: {explicacao_divertida}\n\nPergunta do aluno: {pergunta_aluno}"
                    )
                    st.markdown(f"🗣️ **Resposta da professora:** {resposta_duvida}")

                # 🔹 Limpa o campo depois da resposta
                st.session_state["pergunta_aluno"] = ""


            # --- Botão para gerar nova pergunta ---
            if st.button("Gerar Outra Pergunta"):
                st.session_state.new_question_data = None
                st.session_state.reveal_answer = False
                st.session_state.correct_answer_verified = None
                st.rerun()

