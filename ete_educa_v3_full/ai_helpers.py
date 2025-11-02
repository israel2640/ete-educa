import os
import json
import re
import sympy as sp
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from typing import Dict

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
def _make_api_call(system_prompt: str, user_prompt: str, model: str, temperature: float,
                   response_format: Dict[str, str] | None = None) -> str:
    """Executa chamadas à API OpenAI com tratamento de erros."""
    try:
        client = _client()

        call_params = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }

        if response_format:
            call_params["response_format"] = response_format

        resp = client.chat.completions.create(**call_params)
        return resp.choices[0].message.content.strip()

    except OpenAIError as e:
        return f"❌ Erro ao conectar à OpenAI: {e.message}\nVerifique sua chave e conexão."
    except Exception as e:
        return f"❌ Erro inesperado: {e}"

# =====================================================
# 🔹 Função de verificação automática de cálculo
# =====================================================
def validar_resposta_auto(q: dict):
    """Valida se a resposta numérica faz sentido comparando com o enunciado."""
    try:
        texto = q.get("pergunta", "").lower()
        correta = q.get("correta", "").lower()
        if "x" in texto and "=" in texto:
            x = sp.Symbol('x')
            # Tenta capturar uma equação simples
            partes = texto.replace("^", "**").split("=")
            if len(partes) == 2:
                eq = sp.Eq(sp.sympify(partes[0]), sp.sympify(partes[1]))
                sol = sp.solve(eq, x)
                if sol:
                    valor_x = float(sol[0])
                    # Se a resposta não contém o valor calculado, adiciona observação
                    if str(int(valor_x)) not in correta and str(round(valor_x, 2)) not in correta:
                        q["explicacao"] += f"\n\n⚠️ Verificação automática: " \
                                           f"a IA indicou '{correta}', mas x ≈ {valor_x:.2f}."
    except Exception:
        pass
    return q

# =====================================================
# 🔹 Explicação da IA (modo professora)
# =====================================================
def explain_like_coach(question_text: str, materia: str) -> str:
    """Gera explicações educativas e carinhosas para aluna de 14 anos estudando para a ETE."""
    system = (
        "Você é uma professora particular paciente e carinhosa para uma aluna de 14 anos "
        "que está estudando para o vestibular da ETE (Pernambuco). "
        "Explique de forma simples e com exemplos do dia a dia. "
        "Sempre divida a explicação em 3 blocos:\n"
        "1️⃣ O Pulo do Gato\n2️⃣ Passo a Passo\n3️⃣ Por que as outras estão erradas\n"
        "Finalize com uma dica divertida de memorização."
    )

    user = f"""
Matéria: {materia}

Questão:
{question_text}

Explique seguindo os 3 blocos e finalize com 1 dica curta de memorização.
"""
    return _make_api_call(
        system_prompt=system,
        user_prompt=user,
        model="gpt-5-mini",
        temperature=0.5
    )

# =====================================================
# 🔹 Geração de nova questão com correção automática
# =====================================================
def generate_new_question(materia: str, topico: str) -> dict | None:
    """
    Gera uma nova questão de múltipla escolha no estilo da ETE.
    Aplica validação automática para detectar incoerências matemáticas.
    """
    system = (
        "Você é um assistente de IA especialista em criar questões para o vestibular da ETE. "
        "Crie perguntas no formato de múltipla escolha (4 alternativas: a, b, c, d), "
        "com o mesmo nível das provas anteriores. "
        "\n\nREGRAS:\n"
        "1. PRECISÃO MATEMÁTICA É PRIORIDADE MÁXIMA.\n"
        "2. Resolva o cálculo passo a passo ANTES de escrever o JSON.\n"
        "3. Valide o resultado final antes de gerar a alternativa correta.\n"
        "4. Garanta que a resposta e a explicação estejam coerentes."
    )

    user = f"""
Gere uma (1) nova questão de múltipla escolha sobre o tópico abaixo.

Matéria: {materia}
Tópico: {topico}

Responda apenas com JSON no formato:
{{
  "pergunta": "texto completo da questão",
  "opcoes": ["a) ...", "b) ...", "c) ...", "d) ..."],
  "correta": "b) ...",
  "explicacao": "explicação clara e correta"
}}
"""
    json_string = _make_api_call(
        system_prompt=system,
        user_prompt=user,
        model="gpt-4o",
        temperature=0.6,
        response_format={"type": "json_object"}
    )

    if json_string.startswith("❌"):
        print(f"Erro ao gerar questão: {json_string}")
        return None

    try:
        q = json.loads(json_string)
        q = validar_resposta_auto(q)
        return q
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        print(f"String recebida: {json_string}")
        return None

# =====================================================
# 🔹 Modo rápido (tira-dúvidas)
# =====================================================
def ask_quick_question(pergunta: str) -> str:
    """Responde perguntas curtas de forma didática."""
    system = (
        "Você é um professor tira-dúvidas da ETE. "
        "Explique de forma simples, direta e com exemplos. "
        "Se for um conceito, dê uma frase explicando e um exemplo."
    )
    user = f"Dúvida da aluna: {pergunta}"
    return _make_api_call(
        system_prompt=system,
        user_prompt=user,
        model="gpt-5-mini",
        temperature=0.3
    )
