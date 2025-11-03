import html
import os
import json
import re
import sympy as sp
import math
import requests
import unicodedata
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from typing import Dict, Any

# =====================================================
# 🔹 Carrega variáveis do arquivo .env automaticamente
# =====================================================
load_dotenv()

@dataclass
class AIConfig:
    api_key_env: str = "OPENAI_API_KEY"

# =====================================================
# 🔹 Inicialização segura do cliente
# =====================================================
def _client() -> OpenAI:
    """Cria e valida o cliente OpenAI."""
    cfg = AIConfig()
    api_key = os.getenv(cfg.api_key_env)

    if not api_key:
        raise RuntimeError(f"Defina {cfg.api_key_env} no arquivo .env.")

    if not api_key.startswith(("sk-", "sk-proj-")):
        raise RuntimeError("Chave OPENAI_API_KEY inválida. Deve começar com 'sk-' ou 'sk-proj-'.")

    try:
        return OpenAI(api_key=api_key)
    except Exception as e:
        raise RuntimeError(f"Erro ao inicializar o cliente OpenAI: {e}")

# =====================================================
# 🔹 Função central de chamada à API
# =====================================================
def _make_api_call(system_prompt: str, user_prompt: str, model: str,
                   temperature: float = 1.0, response_format: Dict[str, str] | None = None) -> str:
    """Executa chamadas à API OpenAI com tratamento de erros."""
    try:
        client = _client()

        call_params = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }

        # Alguns modelos (como gpt-5-mini) não aceitam o parâmetro temperature
        unsupported_temp_models = ["gpt-5-mini", "gpt-5"]
        if model not in unsupported_temp_models:
            call_params["temperature"] = temperature

        if response_format:
            call_params["response_format"] = response_format

        resp = client.chat.completions.create(**call_params)
        return resp.choices[0].message.content.strip()

    except OpenAIError as e:
        return f"❌ Erro ao conectar à OpenAI: {e.message}\nVerifique sua chave e conexão."
    except Exception as e:
        return f"❌ Erro inesperado: {e}"

# =====================================================
# 🔹 Função genérica para gerar JSON
# =====================================================
def _generate_question(system_prompt, user_prompt, response_format):
    json_string = _make_api_call(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model="gpt-5-mini",
        temperature=1,
        response_format=response_format,
    )
    if json_string.startswith("❌"):
        print(f"Erro ao gerar questão: {json_string}")
        return None
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        print(f"String recebida: {json_string}")
        return None

# =====================================================
# 🔹 Geração de questão de MATEMÁTICA
# =====================================================
def generate_math_question(materia: str, topico: str) -> dict | None:
    system = (
        "Você é um assistente de IA especialista em criar questões de matemática para o vestibular da ETE. "
        "Crie uma pergunta de múltipla escolha com 4 alternativas (a, b, c, d) "
        "e inclua a equação SymPy correspondente, que o Python poderá resolver. "
        "Não inclua o campo 'correta'."
    )
    user = f"""
Matéria: {materia}
Tópico: {topico}

Responda apenas com JSON no formato:
{{
  "pergunta": "Resolva: 2x + 4 = 10",
  "opcoes": ["a) 2", "b) 3", "c) 4", "d) 5"],
  "equacao_para_sympy": "Eq(2*x + 4, 10)",
  "variavel_solucao": "x",
  "explicacao": "💡 Vamos resolver passo a passo..."
}}
"""
    return _generate_question(system, user, {"type": "json_object"})

# =====================================================
# 🔹 Geração de questão de PORTUGUÊS
# =====================================================
def generate_portuguese_question(materia: str, topico: str) -> dict | None:
    system = (
        "Você é um criador de questões de português para o vestibular da ETE. "
        "Crie uma questão completa com:\n"
        "1️⃣ Um pequeno texto-base (3 a 5 linhas) coerente e claro.\n"
        "2️⃣ Uma pergunta de interpretação sobre esse texto.\n"
        "3️⃣ Quatro alternativas (a, b, c, d).\n"
        "4️⃣ O campo 'correta' com a alternativa certa.\n"
        "5️⃣ Uma explicação textual mostrando por que essa é a correta.\n"
        "⚠️ Formate tudo como JSON bem estruturado."
    )
    user = f"""
Matéria: {materia}
Tópico: {topico}

Responda apenas com JSON no formato:
{{
  "pergunta": "Qual das alternativas expressa melhor a ideia principal do texto?",
  "opcoes": ["a) ...", "b) ...", "c) ...", "d) ..."],
  "correta": "c) ...",
  "explicacao": "💬 Explique por que esta é a alternativa correta."
}}
"""
    return _generate_question(system, user, {"type": "json_object"})

# =====================================================
# 🔹 Resolver matemática e verificar resposta correta
# =====================================================
def get_correct_answer_from_sympy(q_data: dict) -> tuple[str | None, str]:
    """
    Resolve a matemática usando SymPy para ENCONTRAR a resposta correta.
    Faz matching robusto: decimal com ponto/vírgula, fração (a/b), número misto (a b/c) e aproximação.
    """
    try:
        equacao_str = q_data.get("equacao_para_sympy")
        variavel_str = q_data.get("variavel_solucao")
        opcoes = q_data.get("opcoes", [])

        if not equacao_str:
            return None, "Erro: A IA não forneceu uma equação para verificar."

        expr = sp.sympify(equacao_str)
        solucao_final = None

        if isinstance(expr, sp.Equality) and variavel_str:
            variavel = sp.symbols(variavel_str)
            solucoes = sp.solve(expr, variavel)
            if solucoes:
                solucao_final = float(solucoes[0])
        elif not variavel_str:
            solucao_final = float(expr.evalf())

        if solucao_final is None:
            return None, f"Erro: SymPy não conseguiu resolver '{equacao_str}'."

        try:
            racional = sp.nsimplify(solucao_final)
        except Exception:
            racional = None

        def extrair_valor(op_text: str) -> float | None:
            txt = op_text.strip().lower()
            txt = re.sub(r"^[a-d]\)\s*", "", txt)

            m_misto = re.match(r"^\s*(\d+)\s+(\d+)\s*/\s*(\d+)\s*$", txt)
            if m_misto:
                a, b, c = map(int, m_misto.groups())
                if c != 0:
                    return a + (b / c)

            m_frac = re.match(r"^\s*(-?\d+)\s*/\s*(\d+)\s*$", txt)
            if m_frac:
                a, b = map(int, m_frac.groups())
                if b != 0:
                    return a / b

            m_dec = re.search(r"-?\d+(?:[.,]\d+)?", txt)
            if m_dec:
                num = m_dec.group(0).replace(",", ".")
                try:
                    return float(num)
                except ValueError:
                    pass

            return None

        for opcao in opcoes:
            val = extrair_valor(opcao)
            if val is not None:
                if math.isclose(val, solucao_final, rel_tol=0.0, abs_tol=0.01):
                    return opcao, "Cálculo verificado pelo Python (aproximação numérica)."
                if round(val, 2) == round(solucao_final, 2):
                    return opcao, "Cálculo verificado pelo Python (duas casas decimais)."

            if racional and isinstance(racional, sp.Rational):
                frac_text = f"{int(racional.p)}/{int(racional.q)}"
                opcao_limpa = re.sub(r"^[a-d]\)\s*", "", opcao.strip()).replace(" ", "")
                if opcao_limpa == frac_text:
                    return opcao, "Cálculo verificado pelo Python (fração exata)."

        return None, (
            f"Erro: Nenhuma opção corresponde à resposta correta ({solucao_final}). "
            "A IA pode ter criado opções inválidas. Tente gerar outra."
        )

    except Exception as e:
        return None, f"Erro fatal no SymPy: {e}"

# =====================================================
# 🔹 Funções de texto (usam modelo mais barato)
# =====================================================
def explain_like_coach(question_text: str, materia: str) -> str:
    """
    Explica de forma leve, divertida e fácil de entender, como uma professora que ensina alunos de 14 anos do 9º ano.
    Usa emojis, frases curtas e exemplos do dia a dia (dinheiro, escola, futebol, celular, amigos).
    """
    system = (
        "Você é uma professora alegre, paciente e criativa que ensina alunos do 9º ano de escolas públicas do Recife. "
        "Explique de um jeito simples, com frases curtas, palavras fáceis e exemplos do dia a dia (como dinheiro, futebol, escola, amigos, celular). "
        "Use emojis e fale como se estivesse conversando com o aluno na sala. "
        "Evite termos difíceis e equações longas. "
        "Mostre o raciocínio com calma e encoraje o aluno no final. "
        "Sempre divida a resposta em três partes:\n\n"
        "💡 O que a questão quer dizer — explique o que o problema está pedindo, em linguagem do aluno.\n"
        "🪄 Como resolver — mostre o passo a passo de forma simples e divertida.\n"
        "🎯 Dica esperta — termine com uma dica prática ou truque fácil de lembrar depois.\n\n"
        "Evite fórmulas complicadas. Prefira comparações, exemplos e expressões do cotidiano. "
        "O tom deve ser empático, leve e positivo, como uma professora que acredita no potencial do aluno."
    )

    user = f"""
Matéria: {materia}
Questão:
{question_text}

Explique no estilo de professora divertida, com linguagem popular e exemplos práticos.
"""
    return _make_api_call(system_prompt=system, user_prompt=user, model="gpt-5-mini", temperature=1)

def ask_quick_question(pergunta: str) -> str:
    """Responde perguntas rápidas e didáticas."""
    system = (
        "Você é um professor tira-dúvidas da ETE. "
        "Explique de forma simples, direta e com exemplos. "
        "Se for um conceito, dê uma frase explicando e um exemplo."
    )
    user = f"Dúvida da aluna: {pergunta}"
    return _make_api_call(system_prompt=system, user_prompt=user, model="gpt-5-mini", temperature=1)
import html

def limpar_texto_pergunta(texto: str) -> str:
    """
    Corrige textos bugados vindos da IA:
    - Adiciona espaço depois de valores monetários (R6,00de → R$ 6,00 de)
    - Decodifica HTML
    - Remove tags e símbolos estranhos
    """

    if not texto:
        return texto

    # 1️⃣ Decodifica HTML (&eacute;, &ccedil;, etc.)
    texto = html.unescape(texto)

    # 2️⃣ Garante que o símbolo de moeda esteja correto
    texto = texto.replace("R$", "R$ ")
    texto = re.sub(r"R\s*(\d)", r"R$ \1", texto)  # R6 → R$ 6
    texto = re.sub(r"R\$\s*,", "R$ 0,", texto)     # R$,00 → R$ 0,00 (casos raros)

    # 3️⃣ Corrige números grudados em palavras
    texto = re.sub(r"(\d)([A-Za-z])", r"\1 \2", texto)  # 24cada → 24 cada
    texto = re.sub(r"([A-Za-z])(\d)", r"\1 \2", texto)  # Rde2 → R de 2
    texto = re.sub(r"(\d,\d{2})([A-Za-z])", r"\1 \2", texto)  # 6,00de → 6,00 de

    # 4️⃣ Remove tags ou caracteres estranhos
    texto = re.sub(r"<[^>]+>", "", texto)
    texto = re.sub(r"[_*~#><]", "", texto)

    # 5️⃣ Corrige pontuação e espaços
    texto = re.sub(r"\s+", " ", texto).strip()
    texto = re.sub(r"\s+([.,!?])", r"\1", texto)

    # 6️⃣ Corrige padrões conhecidos
    texto = texto.replace("R2", "R$ 2").replace("R3", "R$ 3").replace("R4", "R$ 4")
    texto = texto.replace("R5", "R$ 5").replace("R6", "R$ 6").replace("R7", "R$ 7")
    texto = texto.replace("R8", "R$ 8").replace("R9", "R$ 9").replace("R1", "R$ 1")

    return texto

def buscar_videos_youtube(topico, materia):
    """
    Busca vídeos educativos no YouTube via SerpAPI (Google Search).
    Retorna até 3 resultados relevantes e seguros.
    """
    api_key = os.getenv("SERP_API_KEY")
    if not api_key:
        print("⚠️ SERP_API_KEY não configurada no .env")
        return []

    url = "https://serpapi.com/search"
    pesquisas = [
        f"aula {materia} {topico} explicação 9º ano site:youtube.com",
        f"aula {topico} {materia} site:youtube.com"
    ]

    recomendacoes = []

    try:
        for termo in pesquisas:
            params = {"engine": "google", "q": termo, "num": 5, "api_key": api_key}
            r = requests.get(url, params=params)
            data = r.json()

            for item in data.get("organic_results", []):
                link = item.get("link", "")
                if "youtube.com/watch" in link:
                    recomendacoes.append({
                        "titulo": item.get("title", "Vídeo educativo"),
                        "link": link
                    })
            if recomendacoes:
                break

        # 🔹 Garante máximo de 3 vídeos únicos
        recomendacoes = recomendacoes[:3]

        if not recomendacoes:
            recomendacoes = [
                {"titulo": "Matemática Básica — Professor Ferretto", "link": "https://www.youtube.com/watch?v=dz_1kzq0I3Y"},
                {"titulo": "Interpretação de Texto — Professor Noslen", "link": "https://www.youtube.com/watch?v=XsN0e_xPyNI"}
            ]

        return recomendacoes

    except Exception as e:
        print(f"Erro ao buscar vídeos: {e}")
        return []