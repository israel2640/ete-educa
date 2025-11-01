import streamlit as st
import unicodedata
from ai_helpers import generate_new_question

st.set_page_config(page_title="✨ Modo Livre — ETE Educa", page_icon="✨", layout="centered")
st.title("✨ Modo Livre — Prática Infinita")
st.caption("A IA vai gerar perguntas inéditas para você no estilo da prova!")

# --- Listas de Tópicos do Edital ---
# (Baseado no edital que você forneceu)

topicos_portugues = [
    "Compreensão de Texto (Ideias Principais)",
    "Textualidade (Coesão e Coerência)",
    "Gêneros Textuais e Sequências",
    "Semântica (Sentido das Palavras)",
    "Figuras de Linguagem (Conotação/Denotação)",
    "Norma Padrão e Variedades Linguísticas",
    "Estrutura e Formação das Palavras",
    "Classes Gramaticais",
    "Conectivos (Coordenação e Subordinação)",
    "Pontuação",
    "Concordância e Regência",
    "Crase"
]

topicos_matematica = [
    "Problemas com as Quatro Operações",
    "Operações com Frações",
    "Operações com Números Decimais",
    "Potenciação",
    "Raiz Quadrada Exata",
    "Expressões com Números Reais (PEMDAS)",
    "Sistemas de Medidas",
    "Razão e Proporção",
    "Divisão Proporcional",
    "Regra de Três Simples",
    "Regra de Três Composta",
    "Porcentagem",
    "Médias",
    "Polinômios (Valor Numérico e Operações)",
    "Produtos Notáveis",
    "Fatoração",
    "Radiciação (Simplificação de Raízes)",
    "Equações Algébricas do 1º Grau",
    "Sistemas Lineares do 1º Grau",
    "Ângulos",
    "Polígonos (Soma dos Ângulos)",
    "Triângulos (Classificação e Lei Angular)",
    "Semelhança de Triângulos (Teorema de Tales)",
    "Cevianas (Mediana, Bissetriz, Altura)"
]

# --- Interface do Modo Livre ---

# Inicializa o estado
if "new_question_data" not in st.session_state:
    st.session_state.new_question_data = None
if "reveal_answer" not in st.session_state:
    st.session_state.reveal_answer = False

# Seleção de Matéria e Tópico
materia = st.radio("Escolha a matéria:", ["Português", "Matemática"], horizontal=True)
if materia == "Português":
    topico = st.selectbox("Escolha um tópico do edital:", topicos_portugues)
else:
    topico = st.selectbox("Escolha um tópico do edital:", topicos_matematica)

# Botão de Gerar
if st.button(f"Gerar Pergunta Inédita sobre {topico}"):
    st.session_state.new_question_data = None # Limpa a questão anterior
    st.session_state.reveal_answer = False # Esconde a resposta
    with st.spinner(f"A IA está criando uma questão sobre {topico}..."):
        try:
            st.session_state.new_question_data = generate_new_question(materia, topico)
        except Exception as e:
            st.error(f"Não foi possível conectar à IA. Verifique seu .env. Erro: {e}")

st.divider()

# --- Exibição da Pergunta ---
if st.session_state.new_question_data:
    q_data = st.session_state.new_question_data
    
    st.subheader("Questão Gerada pela IA:")
    st.markdown(q_data.get("pergunta", "Erro ao carregar pergunta."))
    
    # Exibe as opções de rádio
    opcoes = q_data.get("opcoes", [])
    if opcoes:
        resposta_usuario = st.radio(
            "Escolha sua resposta:", 
            opcoes, 
            index=None, # Deixa em branco por padrão
            key="modo_livre_radio"
        )
        
        # Botão para revelar
        if st.button("Revelar Resposta e Explicação"):
            st.session_state.reveal_answer = True

        # Lógica de revelação
        if st.session_state.reveal_answer:
            correta = q_data.get("correta", "")
            
            if resposta_usuario == correta:
                st.success(f"🎉 Você acertou! A resposta correta é: **{correta}**")
                st.balloons()
            else:
                st.error(f"❌ Você marcou: {resposta_usuario}\nA resposta correta era: **{correta}**")
            
            st.subheader("Explicação do Mestre:")
            st.info(q_data.get("explicacao", "Sem explicação disponível."))
            
            if st.button("Gerar Outra Pergunta"):
                st.session_state.new_question_data = None
                st.session_state.reveal_answer = False
                st.rerun()