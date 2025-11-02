import os
import json
import re
import sympy as sp
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from typing import Dict, Any, Literal

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
# 🔹 Função central de chamada à API (DEFINIDA AQUI)
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
# 🔹 Geração de nova questão (A IA SÓ CRIA, NÃO RESOLVE)
# =====================================================
def generate_new_question(materia: str, topico: str) -> dict | None:
    """
    A IA gera a pergunta, as opções e a string da equação.
    O Python (SymPy) será o único responsável por resolvê-la.
    """
    
    # --- PROMPT DE SISTEMA MELHORADO ---
    system = (
        "Você é um assistente de IA especialista em criar questões para o vestibular da ETE. "
        "Seu trabalho é criar uma pergunta de múltipla escolha (4 alternativas: a, b, c, d) sobre um tópico. "
        "Você DEVE fornecer a equação matemática pura, em formato SymPy, em um campo separado para que um "
        "computador possa resolvê-la e verificar."
        "\n\nREGRAS CRÍTICAS:\n"
        "1. PRECISÃO MATEMÁTICA É PRIORIDADE MÁXIMA.\n"
        "2. NÃO inclua a chave 'correta' no JSON. O computador irá calcular.\n"
        "3. A 'equacao_para_sympy' DEVE ser uma string que o SymPy possa resolver.\n"
        "4. A 'explicacao' deve ser um guia passo a passo, em tom AMIGÁVEL e ENCANTADOR, como se estivesse falando com um aluno de 14 anos. Use emojis (💡, 🤓, ✅) para guiar."
    )
    
    # --- EXEMPLOS DO USUÁRIO MELHORADOS (COM O NOVO TOM) ---
    user = f"""
Gere uma (1) nova questão de múltipla escolha sobre o tópico abaixo.

Matéria: {materia}
Tópico: {topico}

Responda apenas com JSON no formato:
{{
  "pergunta": "Seja y um número real tal que 5^(y - 2) = 1/25. Qual é o valor de y?",
  "opcoes": ["a) 0", "b) 1", "c) 2", "d) 3"],
  "equacao_para_sympy": "Eq(5**(y - 2), 1/25)",
  "variavel_solucao": "y",
  "explicacao": "🤓 Ei, vamos lá! O truque aqui é 'igualar as bases'.\n1. 💡 O lado esquerdo tem base 5. Precisamos reescrever o 1/25 como base 5.\n2. Lembre-se que 25 = 5^2. E quando o número está 'embaixo' (no denominador), o expoente fica negativo!\n3. Então, 1/25 = 5^(-2).\n4. Agora a equação fica: 5^(y - 2) = 5^(-2).\n5. ✅ Como as bases (o 5) são iguais, os expoentes têm que ser iguais! Então: y - 2 = -2.\n6. Resolvendo: y = -2 + 2, o que dá y = 0."
}}

---

Outro Exemplo (sem variável):
Matéria: Matemática
Tópico: Potenciação

{{
  "pergunta": "Qual é o valor de (3^4) * (3^-2)?",
  "opcoes": ["a) 9", "b) 27", "c) 1", "d) 3"],
  "equacao_para_sympy": "3**4 * 3**(-2)",
  "variavel_solucao": null,
  "explicacao": "💡 Esse é mais fácil do que parece! A regra de potência diz que quando multiplicamos números com a mesma base (a base aqui é 3), nós só precisamos SOMAR os expoentes.\n1. Os expoentes são 4 e -2.\n2. A conta é: 4 + (-2) = 2.\n3. Então, o resultado é 3^2 (três ao quadrado).\n4. ✅ 3^2 = 3 * 3 = 9."
}}
"""
    
    # AGORA A CHAMADA FUNCIONA
    json_string = _make_api_call(
        system_prompt=system,
        user_prompt=user,
        model="gpt-4o",
        temperature=0.7,
        response_format={"type": "json_object"}
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
# 🔹 FUNÇÃO DO "PROFESSOR CORRETOR" (PYTHON RESOLVE)
# =====================================================
def get_correct_answer_from_sympy(q_data: dict) -> tuple[str | None, str]:
    """
    Resolve a matemática usando SymPy para ENCONTRAR a resposta correta.
    """
    try:
        equacao_str = q_data.get("equacao_para_sympy")
        variavel_str = q_data.get("variavel_solucao")
        opcoes = q_data.get("opcoes", [])
        
        if not equacao_str:
            return None, "Erro: A IA não forneceu uma equação para verificar."
            
        # Simplifica a equação
        expr = sp.sympify(equacao_str)
        
        solucao_final = None
        
        # Se for uma equação (ex: Eq(2*x, 64))
        if isinstance(expr, sp.Equality) and variavel_str:
            variavel = sp.symbols(variavel_str)
            solucoes = sp.solve(expr, variavel)
            if solucoes:
                solucao_final = float(solucoes[0])
        
        # Se for uma expressão direta (ex: 3**4 * 3**(-2))
        elif not variavel_str:
            solucao_final = float(expr.evalf())

        if solucao_final is None:
            return None, f"Erro: SymPy não conseguiu resolver '{equacao_str}'."

        # Agora, encontre a opção que bate com a solução
        solucao_str_ponto = str(round(solucao_final, 2))      # "2.5"
        solucao_str_virgula = solucao_str_ponto.replace('.', ',') # "2,5"
        solucao_str_int = str(int(solucao_final))            # "2" ou "9"
        
        for opcao in opcoes:
            # Remove a letra (ex: "a) ", "b) ") e espaços
            opcao_limpa = re.sub(r"^[a-d]\)\s*", "", opcao.strip())
            
            # Compara com todos os formatos
            if (
                opcao_limpa == solucao_str_ponto or
                opcao_limpa == solucao_str_virgula or
                (solucao_final == int(solucao_final) and opcao_limpa == solucao_str_int)
            ):
                return opcao, "Cálculo verificado pelo Python." # Achamos a resposta correta!
        
        return None, f"Erro: Nenhuma opção ({[op for op in opcoes]}) corresponde à resposta correta ({solucao_final}). A IA criou opções inválidas."

    except Exception as e:
        return None, f"Erro fatal no SymPy: {e}"


# =====================================================
# 🔹 Funções de texto (usam modelo mais barato)
# =====================================================
def explain_like_coach(question_text: str, materia: str) -> str:
    """Gera explicações educativas e carinhosas (modo professora)."""
    system = (
        "Você é uma professora particular paciente e carinhosa para uma aluna de 14 anos "
        "que está estudando para o vestibular da ETE (Pernambuco). "
        "Explique de forma simples e com exemplos do dia a dia. "
        "Sempre divida a explicação em 3 blocos:\n"
        "1️⃣ O Pulo do Gato\n2️⃣ Passo a Passo\n3️⃣ Por que as outras estão erradas\n"
        "Finalize com uma dica divertida de memorização."
    )
    user = f"Matéria: {materia}\n\Questão:\n{question_text}\n\nExplique seguindo os 3 blocos e finalize com 1 dica curta de memorização."
    return _make_api_call(system_prompt=system, user_prompt=user, model="gpt-5-mini", temperature=0.5)

def ask_quick_question(pergunta: str) -> str:
    """Responde perguntas curtas de forma didática."""
    system = (
        "Você é um professor tira-dúvidas da ETE. "
        "Explique de forma simples, direta e com exemplos. "
        "Se for um conceito, dê uma frase explicando e um exemplo."
    )
    user = f"Dúvida da aluna: {pergunta}"
    return _make_api_call(system_prompt=system, user_prompt=user, model="gpt-5-mini", temperature=1.0)