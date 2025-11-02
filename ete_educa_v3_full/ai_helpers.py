import streamlit as st
import unicodedata
import re
import sympy as sp
# AQUI ESTÁ A MUDANÇA: importamos a nova função de verificação
from ai_helpers import generate_new_question, get_correct_answer_from_sympy

# --- Configurações removidas (já fizemos a limpeza antes) ---

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
        q_data = generate_new_question(materia, topico)
        
        if q_data:
            st.session_state.new_question_data = q_data
            
            # --- O "PROFESSOR CORRETOR" ENTRA EM AÇÃO ---
            if materia == "Matemática":
                with st.spinner("Python (SymPy) está verificando a matemática da IA..."):
                    correta_verificada, status = get_correct_answer_from_sympy(q_data)
                    
                    if correta_verificada:
                        st.session_state.correct_answer_verified = correta_verificada
                    else:
                        st.error(f"Falha na verificação: {status}. A IA pode ter criado opções inválidas. Tente gerar outra.")
                        st.session_state.new_question_data = None
            else:
                # Para Português: a IA já enviou a chave 'correta' no JSON
                correta_verificada = q_data.get("correta")
                if correta_verificada:
                    st.session_state.correct_answer_verified = correta_verificada
                else:
                    st.error("Falha de Geração: A IA não forneceu a resposta correta para a pergunta de Português. Tente gerar novamente.")
                    st.session_state.new_question_data = None


st.divider()

# --- Exibição da Pergunta ---
if st.session_state.new_question_data and st.session_state.correct_answer_verified:
    q_data = st.session_state.new_question_data
    
    st.subheader("Questão Gerada pela IA:")
    st.markdown(q_data.get("pergunta", "Erro ao carregar pergunta."))
    
    opcoes = q_data.get("opcoes", [])
    if opcoes:
        resposta_usuario = st.radio(
            "Escolha sua resposta:", 
            opcoes, 
            index=None,
            key="modo_livre_radio"
        )
        
        if st.button("Revelar Resposta e Explicação"):
            st.session_state.reveal_answer = True

        if st.session_state.reveal_answer:
            # A RESPOSTA CORRETA AGORA VEM DA VERIFICAÇÃO FINAL
            correta = st.session_state.correct_answer_verified
            
            if resposta_usuario == correta:
                st.success(f"🎉 Você acertou! A resposta correta (verificada pelo Python) é: **{correta}**")
                st.balloons()
            else:
                st.error(f"❌ Você marcou: {resposta_usuario}\nA resposta correta (verificada pelo Python) era: **{correta}**")
            
            st.subheader("Explicação do Mestre:")
            st.info(q_data.get("explicacao", "Sem explicação disponível."))
            
            if st.button("Gerar Outra Pergunta"):
                st.session_state.new_question_data = None
                st.session_state.reveal_answer = False
                st.session_state.correct_answer_verified = None
                st.rerun()