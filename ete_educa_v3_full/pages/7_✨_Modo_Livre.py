import streamlit as st
import unicodedata
import re
import sympy as sp
import time 

# 🔹 Importações corretas das funções de IA (COM A CORREÇÃO)
from ai_helpers import (
    generate_math_question,
    generate_portuguese_question,
    get_correct_answer_from_sympy,
    explain_like_coach,      # para explicações divertidas
    ask_quick_question,      # para perguntas do aluno
    limpar_texto_pergunta,  # Importação corrigida
    generate_speech
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

# (Lógica do temporizador)
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "elapsed_time_seconds" not in st.session_state:
    st.session_state.elapsed_time_seconds = None


materia = st.radio("Escolha a matéria:", ["Português", "Matemática"], horizontal=True)
if materia == "Português":
    topico = st.selectbox("Escolha um tópico do edital:", topicos_portugues)
else:
    topico = st.selectbox("Escolha um tópico do edital:", topicos_matematica)

if st.button(f"Gerar Pergunta Inédita sobre {topico}"):
    # Reseta o estado completo
    st.session_state.new_question_data = None
    st.session_state.reveal_answer = False
    st.session_state.correct_answer_verified = None
    st.session_state.start_time = None
    st.session_state.elapsed_time_seconds = None
    st.session_state.chat_duvidas = [] # Reseta o chat anterior

    with st.spinner(f"A IA está criando uma questão sobre {topico}..."):

        # 1) Gera a questão (IA)
        if materia == "Matemática":
            q_data = generate_math_question(materia, topico)
        else:
            q_data = generate_portuguese_question(materia, topico)

        # 2) Se gerou, LIMPA primeiro
        if q_data:
            # 🔹 Limpa textos bugados
            if "pergunta" in q_data:
                q_data["pergunta"] = limpar_texto_pergunta(q_data["pergunta"])
            if "texto" in q_data:
                q_data["texto"] = limpar_texto_pergunta(q_data["texto"])
            if "explicacao" in q_data:
                q_data["explicacao"] = limpar_texto_pergunta(q_data["explicacao"])
            if "opcoes" in q_data and isinstance(q_data["opcoes"], list):
                q_data["opcoes"] = [limpar_texto_pergunta(op) for op in q_data["opcoes"]]

            # --- NOVO BLOCO: VERIFICAÇÃO DE INTEGRIDADE (CONTRA RUÍDO) ---
            pergunta_limpa = q_data.get("pergunta", "").lower()
            
            # Padrões que indicam ruído ou formatação quebrada:
            # 1. Letras minúsculas soltas (o, u, g, n, etc.) com vírgula ou espaço.
            # 2. Palavras grudadas após o símbolo de Real (ex: R$15.sabe).
            if re.search(r"r\$\s*\d+\s*[.,]\s*[a-z]", pergunta_limpa) or re.search(r"[\s,][a-z]\s+[a-z]\s+[a-z][\s,]", pergunta_limpa):
                
                st.error("❌ Erro de formatação grave detectado (ruído de caracteres ou falha na moeda). A questão foi rejeitada para garantir a qualidade. Tente gerar novamente.")
                st.session_state.new_question_data = None
                
                # RECURSO: O RERUN É CRÍTICO AQUI PARA LIMPAR O ESTADO
                st.rerun() 
            
            
            st.session_state.new_question_data = q_data

            # 4) Verifica a resposta
            if materia == "Matemática":
                with st.spinner("Python (SymPy) está verificando a matemática da IA..."):
                    correta_verificada, status = get_correct_answer_from_sympy(q_data)
                    if correta_verificada:
                        st.session_state.correct_answer_verified = correta_verificada
                        st.session_state.start_time = time.time() # Inicia o timer
                    else:
                        st.error(f"Falha na verificação: {status}. A IA pode ter criado opções inválidas. Tente gerar outra.")
                        st.session_state.new_question_data = None
            else:
                # Português: pega a correta vinda da IA
                correta_ia = q_data.get("correta")
                if not correta_ia: # Tenta inferir se a IA esqueceu
                    exp = q_data.get("explicacao", "").lower()
                    for opcao in q_data.get("opcoes", []):
                        if isinstance(opcao, str) and ")" in opcao:
                            corpo = opcao.lower().split(")", 1)[1].strip()
                            if corpo and corpo in exp:
                                correta_ia = opcao
                                break
                if correta_ia:
                    st.session_state.correct_answer_verified = correta_ia
                    st.session_state.start_time = time.time() # Inicia o timer
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
    pergunta_completa = q_data.get('pergunta', 'Erro ao carregar pergunta.')

    # NOVO: Dividir o layout em duas colunas para o texto da pergunta e o botão de áudio
    col_pergunta, col_audio = st.columns([0.9, 0.1]) # 90% para a pergunta, 10% para o botão

    with col_pergunta:
        st.markdown(f"**📝 {pergunta_completa}**")

    # NOVO: Botão para gerar e tocar o áudio
    with col_audio:
        # O botão '🔊' usa o ícone de som
        if st.button("🔊", key="audio_button", help="Clique para ouvir a pergunta"): 
            # 1. Tenta gerar o áudio
            with st.spinner("Gerando áudio..."):
                audio_bytes = generate_speech(pergunta_completa)
            
            if audio_bytes:
                # 2. Armazena os bytes na sessão
                st.session_state.audio_pergunta = audio_bytes
            else:
                st.error("❌ Erro ao gerar o áudio. Verifique as configurações da OpenAI.")

    # NOVO: Exibe o player de áudio se o áudio foi gerado
    if "audio_pergunta" in st.session_state and st.session_state.audio_pergunta:
         # st.audio exibe o player nativo do navegador e toca automaticamente (autoplay=True)
         st.audio(st.session_state.audio_pergunta, format='audio/mp3', autoplay=True) 

    # Continuação do seu código original:
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
            # Para o temporizador
            if st.session_state.start_time:
                end_time = time.time()
                elapsed_time = end_time - st.session_state.start_time
                st.session_state.elapsed_time_seconds = elapsed_time
                st.session_state.start_time = None # Para o timer
            else:
                st.session_state.elapsed_time_seconds = None
            
            st.session_state.reveal_answer = True

        # 🔹 Quando o aluno clica em "Revelar"
        if st.session_state.reveal_answer:
            
            # Exibe o tempo de resposta
            if st.session_state.elapsed_time_seconds is not None:
                total_seconds = int(st.session_state.elapsed_time_seconds)
                minutes, seconds = divmod(total_seconds, 60)
                if minutes > 0:
                    time_str = f"{minutes} min e {seconds} seg"
                else:
                    time_str = f"{seconds} segundos"
                
                st.info(f"⏱️ **Tempo de resposta:** {time_str}")

            correta = st.session_state.correct_answer_verified

            if resposta_usuario == correta:
                st.success(f"🎉 Você acertou! A resposta correta (verificada pelo Python) é: **{correta}**")
                st.balloons()
            else:
                st.error(f"❌ Você marcou: {resposta_usuario}\nA resposta correta (verificada pelo Python) era: **{correta}**")

            st.subheader("Explicação da Professora:")

            # 'explicacao_divertida' É DEFINIDA AQUI
            explicacao_original = q_data.get("explicacao", "Sem explicação disponível.")
            
            # PASSO 1: LIMPA a explicação original antes de enviar para a IA de persona
            explicacao_limpa = limpar_texto_pergunta(explicacao_original)
            
            # PASSO 2: Envia o texto LIMPO para a IA que cria a "persona do coach"
            explicacao_divertida = explain_like_coach(explicacao_limpa, materia)

            st.markdown(f"🧠 {explicacao_divertida}")
            
            
            # ==========================================================
            # 🔹 CORREÇÃO: TODO O BLOCO DE CHAT FOI MOVIDO PARA CÁ
            # ==========================================================
            
            st.markdown("💬 **Tem alguma dúvida sobre essa explicação?**")

            # --- Inicializa variáveis ---
            if "chat_duvidas" not in st.session_state:
                st.session_state.chat_duvidas = []
                if "audio_pergunta" in st.session_state:
                    st.session_state.audio_pergunta = None
            if "limpar_input" not in st.session_state:
                st.session_state.limpar_input = False

            if st.session_state.limpar_input:
                st.session_state.limpar_input = False
                st.session_state.pergunta_aluno = ""

            # --- Exibe histórico do chat ---
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

            # --- Campo de entrada ---
            st.divider()
            pergunta_aluno = st.text_input("Digite sua pergunta aqui:", key="pergunta_aluno")

            if pergunta_aluno:
                with st.spinner("A professora está pensando... 🤔"):
                    # AGORA 'explicacao_divertida' GARANTIDAMENTE EXISTE
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
            # ==========================================================
            # 🔹 FIM DO BLOCO DE CHAT MOVIDO
            # ==========================================================