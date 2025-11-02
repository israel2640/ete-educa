import streamlit as st
import sympy as sp
import re
from ai_helpers import generate_new_question, explain_like_coach

st.set_page_config(page_title="Modo Livre — ETE Educa", page_icon="⚡", layout="centered")

st.title("⚡ Modo Livre")
st.caption("Gere questões inéditas com IA — agora com verificação automática de cálculos 🔍")

st.markdown("---")

# ========================================
# 🧭 Escolha de matéria e tópico
# ========================================
materia = st.selectbox(
    "Escolha a matéria:",
    ["Matemática", "Português", "Ciências", "História", "Geografia"]
)
topico = st.text_input("Digite um tópico (ex: potências, substantivos, ecossistemas):")

st.markdown("---")

if st.button("🎲 Gerar Questão com IA"):
    if not topico.strip():
        st.warning("Por favor, insira um tópico para gerar a questão.")
        st.stop()

    with st.spinner("Gerando questão com IA..."):
        q = generate_new_question(materia, topico)

    if not q:
        st.error("❌ Não foi possível gerar a questão. Tente novamente.")
        st.stop()

    st.session_state["questao_atual"] = q
    st.session_state["resposta_certa"] = None
    st.session_state["explicacao_final"] = None

# ========================================
# 📘 Exibir questão gerada
# ========================================
if "questao_atual" in st.session_state:
    q = st.session_state["questao_atual"]

    st.markdown("### 🧠 Questão Gerada pela IA:")
    st.write(q["pergunta"])

    # Mostra as alternativas
    resposta_usuario = st.radio("Escolha sua resposta:", q["opcoes"], key="resposta_usuario")

    # ========================================
    # 🔍 Função para validar o cálculo matemático
    # ========================================
    def corrigir_expressao(expr_text):
        """
        Tenta resolver expressões simples (com ^, *, /, +, -) e retornar o resultado numérico.
        """
        try:
            expr = expr_text.replace("^", "**")
            result = sp.sympify(expr).evalf()
            return float(result)
        except Exception:
            return None

    # ========================================
    # 🧩 Verificação automática da resposta
    # ========================================
    if st.button("Revelar Resposta e Explicação"):
        correta = q["correta"]
        explicacao = q["explicacao"]

        # 🔸 Verifica se há expressão matemática no enunciado
        texto = q["pergunta"]
        possiveis_expr = re.findall(r"[\d\(\)\+\-\*\/\^x\s]+", texto)
        calculado = None

        for trecho in possiveis_expr:
            if any(op in trecho for op in ["^", "*", "+", "-"]):
                calculado = corrigir_expressao(trecho)
                break

        # Corrige se o cálculo automático não bate com a resposta da IA
        if calculado is not None:
            if str(int(calculado)) not in correta and str(round(calculado, 2)) not in correta:
                explicacao += f"\n\n⚠️ Correção automática: o cálculo simbólico indica que o resultado é **{calculado:.2f}**."
                correta += f" (Corrigido pelo sistema)"

        st.session_state["resposta_certa"] = correta
        st.session_state["explicacao_final"] = explicacao

# ========================================
# 🧾 Mostrar feedback e explicação
# ========================================
if st.session_state.get("resposta_certa"):
    correta = st.session_state["resposta_certa"]
    explicacao = st.session_state["explicacao_final"]
    resposta_usuario = st.session_state.get("resposta_usuario", "")

    if resposta_usuario.strip() == correta.strip():
        st.success(f"✅ Você acertou! A resposta correta era: {correta}")
    else:
        st.error(f"❌ Você marcou: {resposta_usuario}\n\nA resposta correta era: {correta}")

    st.markdown("---")
    st.markdown("### 🧑‍🏫 Explicação do Mestre:")

    with st.spinner("Gerando explicação detalhada..."):
        explicacao_ia = explain_like_coach(q["pergunta"], materia)

    st.info(explicacao)
    st.markdown("---")
    st.markdown("### 💬 Explicação da IA (professora):")
    st.write(explicacao_ia)

    st.button("🔁 Gerar Outra Pergunta", on_click=lambda: st.session_state.clear())

# ========================================
# ⚠️ Aviso de segurança
# ========================================
st.markdown("---")
st.caption(
    "⚠️ As questões são criadas pela IA e verificadas automaticamente com cálculos simbólicos. "
    "Mesmo assim, revise sempre o raciocínio — o objetivo é **treinar o pensamento**, não apenas decorar respostas. 🧩"
)
