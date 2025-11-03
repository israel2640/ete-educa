import streamlit as st
import unicodedata
import re
import sympy as sp
from ai_helpers import limpar_texto_pergunta

# 🔹 Importações corretas das funções de IA
from ai_helpers import (
    generate_math_question,
    generate_portuguese_question,
    get_correct_answer_from_sympy,
    explain_like_coach,      # para explicações divertidas
    ask_quick_question,      # para perguntas do aluno
    buscar_videos_youtube    # para recomendações de vídeos
)

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

if st.button(f"Gerar Pergunta Inédita sobre {topico}"):
    st.session_state.new_question_data = None
    st.session_state.reveal_answer = False
    st.session_state.correct_answer_verified = None

    with st.spinner(f"A IA está criando uma questão sobre {topico}..."):

        # 1) Gera a questão (IA)
        if materia == "Matemática":
            q_data = generate_math_question(materia, topico)
        else:
            q_data = generate_portuguese_question(materia, topico)

        # 2) Se gerou, LIMPA primeiro (antes de salvar e antes de verificar)
        if q_data:
            # 🔹 Limpa textos bugados vindos da IA (antes de salvar no session_state)
            if "pergunta" in q_data:
                q_data["pergunta"] = limpar_texto_pergunta(q_data["pergunta"])
            if "texto" in q_data:
                q_data["texto"] = limpar_texto_pergunta(q_data["texto"])
            if "explicacao" in q_data:
                q_data["explicacao"] = limpar_texto_pergunta(q_data["explicacao"])
            if "opcoes" in q_data and isinstance(q_data["opcoes"], list):
                q_data["opcoes"] = [limpar_texto_pergunta(op) for op in q_data["opcoes"]]

            # Depois de limpar, salva
            st.session_state.new_question_data = q_data


            # 4) Verifica a resposta (apenas Matemática)
            if materia == "Matemática":
                with st.spinner("Python (SymPy) está verificando a matemática da IA..."):
                    correta_verificada, status = get_correct_answer_from_sympy(q_data)
                    if correta_verificada:
                        st.session_state.correct_answer_verified = correta_verificada
                    else:
                        st.error(f"Falha na verificação: {status}. A IA pode ter criado opções inválidas. Tente gerar outra.")
                        st.session_state.new_question_data = None
            else:
                # Português: pega a correta vinda da IA (ou tenta inferir)
                correta_ia = q_data.get("correta")
                if not correta_ia:
                    exp = q_data.get("explicacao", "").lower()
                    for opcao in q_data.get("opcoes", []):
                        if isinstance(opcao, str) and ")" in opcao:
                            corpo = opcao.lower().split(")", 1)[1].strip()
                            if corpo and corpo in exp:
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
    st.markdown(f"**📝 {q_data.get('pergunta', 'Erro ao carregar pergunta.')}**")


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
            # 🔹 Recomendar vídeos do YouTube com base no tópico e matéria
            from ai_helpers import buscar_videos_youtube

            with st.spinner("Buscando vídeos explicativos no YouTube... 🎥"):
                recomendacoes = buscar_videos_youtube(topico, materia)

            if recomendacoes:
                st.markdown("🎬 **Quer reforçar o conteúdo? Assista também:**")

                for v in recomendacoes:
                    titulo = v.get("titulo", "Vídeo educativo")
                    link = v.get("link", "")

                    if link:
                        st.markdown(
                            f"<a href='{link}' target='_blank' style='text-decoration:none; color:#00B4FF;'>▶️ {titulo}</a>",
                            unsafe_allow_html=True
                        )



            # 🔹 Campo para o aluno perguntar sobre a explicação
    st.markdown("💬 **Tem alguma dúvida sobre essa explicação?**")

    # --- Inicializa variáveis ---
    if "chat_duvidas" not in st.session_state:
        st.session_state.chat_duvidas = []
    if "limpar_input" not in st.session_state:
        st.session_state.limpar_input = False

    # --- Se a flag estiver ativa, limpa o input ---
    if st.session_state.limpar_input:
        st.session_state.limpar_input = False
        st.session_state.pergunta_aluno = ""

    # --- Exibe histórico do chat antes do input ---
    if st.session_state.chat_duvidas:
        st.markdown("🧠 **Chat com a Professora IA**")
        st.markdown("""
        <style>
            .chat-container {
                display: flex;
                flex-direction: column;
                gap: 12px;
                margin-top: 10px;
            }
            .mensagem-aluno {
                align-self: flex-end;
                background: linear-gradient(135deg, #0078D7, #00B4FF);
                color: white;
                padding: 10px 14px;
                border-radius: 18px 18px 0px 18px;
                max-width: 70%;
                box-shadow: 0px 2px 5px rgba(0,0,0,0.15);
            }
            .mensagem-professora {
                align-self: flex-start;
                background: #FFFBEA;
                color: #333;
                padding: 10px 14px;
                border-radius: 18px 18px 18px 0px;
                max-width: 80%;
                border: 1px solid #FFE58A;
                box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for msg in st.session_state.chat_duvidas:
            st.markdown(f"""
            <div class='mensagem-aluno'><b>👦 Você:</b> {msg["pergunta"]}</div>
            <div class='mensagem-professora'><b>👩‍🏫 Professora:</b> {msg["resposta"]}</div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Campo de entrada AGORA fica embaixo ---
    st.divider()
    pergunta_aluno = st.text_input("Digite sua pergunta aqui:", key="pergunta_aluno")

    if pergunta_aluno:
        with st.spinner("A professora está pensando... 🤔"):
            resposta_duvida = ask_quick_question(
                f"Matéria: {materia}\n\nExplicação: {explicacao_divertida}\n\nPergunta do aluno: {pergunta_aluno}"
            )

        st.session_state.chat_duvidas.append({
            "pergunta": pergunta_aluno,
            "resposta": resposta_duvida
        })

        st.session_state.limpar_input = True
        st.rerun()

    # --- Botão de limpar conversa ---
    if st.session_state.chat_duvidas:
        st.divider()
        if st.button("🧹 Limpar conversa"):
            st.session_state.chat_duvidas = []
            st.session_state.limpar_input = True
            st.rerun()

    st.caption("💬 O chat fica salvo enquanto você estiver nesta sessão 👩‍🏫")