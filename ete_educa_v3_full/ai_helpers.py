import os
import json
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from typing import Dict, Any, Literal

# Carrega variáveis do arquivo .env automaticamente
load_dotenv()

@dataclass
class AIConfig:
    api_key_env: str = "OPENAI_API_KEY"
    # O modelo foi removido daqui, pois cada função escolherá o seu.

def _client() -> OpenAI:
    """Cria e valida o cliente OpenAI."""
    cfg = AIConfig()
    api_key = os.getenv(cfg.api_key_env)

    if not api_key:
        raise RuntimeError(f"Defina {cfg.api_key_env} no arquivo .env.")

    # Aceita tanto sk- quanto sk-proj-
    if not api_key.startswith(("sk-", "sk-proj-")):
        raise RuntimeError(
            "Chave OPENAI_API_KEY inválida. Ela deve começar com 'sk-' ou 'sk-proj-'."
        )

    try:
        return OpenAI(api_key=api_key)
    except Exception as e:
        raise RuntimeError(f"Erro ao inicializar o cliente OpenAI: {e}")

# =====================================================
# 🔹 FUNÇÃO CENTRAL DE CHAMADA DE API (MELHORIA 1)
# =====================================================
def _make_api_call(
    system_prompt: str, 
    user_prompt: str, 
    model: str, 
    temperature: float,
    response_format: Dict[str, str] | None = None
) -> str:
    """
    Função centralizada para fazer chamadas à API OpenAI.
    Lida com a criação do cliente e o tratamento de erros.
    """
    try:
        client = _client()
        
        # Constrói os parâmetros da chamada
        call_params = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }
        
        # Adiciona o formato de resposta (JSON) se for solicitado
        if response_format:
            call_params["response_format"] = response_format

        resp = client.chat.completions.create(**call_params)
        return resp.choices[0].message.content.strip()

    except OpenAIError as e:
        # Lida com erros da API (chave errada, sem crédito, etc.)
        return f"❌ Erro ao conectar à OpenAI: {e.message}\nVerifique sua chave, cota e conexão."
    except Exception as e:
        # Lida com outros erros (ex: RuntimeError do _client)
        return f"❌ Erro inesperado: {e}"

# =====================================================
# 🔹 Funções Públicas (Agora mais limpas)
# =====================================================

def explain_like_coach(question_text: str, materia: str) -> str:
    """
    Gera explicações educativas e carinhosas para aluna de 14 anos estudando para a ETE.
    """
    system = (
        "Você é uma professora particular paciente e carinhosa para uma aluna de 14 anos "
        "se preparando para o vestibular da ETE (Pernambuco). "
        "Explique de forma simples, divertida e com exemplos reais do dia a dia. "
        "Sempre organize a resposta em três blocos: "
        "1️⃣ O Pulo do Gato, 2️⃣ Passo a Passo, 3️⃣ Por que as outras estão erradas. "
        "Finalize com uma dica de memorização curta e divertida."
    )

    user = f"""
Matéria: {materia}

Questão (com alternativas, se houver):
{question_text}

Explique em 3 blocos:
1) O Pulo do Gato
2) Passo a Passo
3) Por que as outras estão erradas
Finalize com 1 dica de memorização.
"""
    # Chama a função central com o modelo rápido
    return _make_api_call(
        system_prompt=system,
        user_prompt=user,
        model="gpt-5-mini", # Rápido e barato para explicações
        temperature=0.5
    )


def generate_new_question(materia: str, topico: str) -> dict | None:
    """
    Gera uma nova questão de múltipla escolha no estilo da ETE, 
    retornando um dicionário (JSON).
    """
    
    # --- MELHORIA 2: PROMPT CORRIGIDO PARA MATEMÁTICA ---
    system = (
        "Você é um assistente de IA especialista em criar questões para o vestibular da ETE de Pernambuco (nível Ensino Médio). "
        "Você cria perguntas originais, no formato de múltipla escolha (4 alternativas: a, b, c, d), "
        "que seguem o estilo e o nível de dificuldade das provas passadas (como as da ETEP)."
        "\n\n"
        "REGRAS CRÍTICAS:"
        "1. PRECISÃO MATEMÁTICA É A PRIORIDADE MÁXIMA."
        "2. Pense passo a passo. Verifique todos os seus cálculos aritméticos antes de gerar a resposta."
        "3. A explicação deve ser 100% correta e justificar a resposta correta."
        "4. Exemplo de verificação: Se a expressão for 81 - 8 + 5, o resultado é 73 + 5 = 78. NÃO 70."
    )
    
    user = f"""
    Por favor, gere uma (1) nova questão de múltipla escolha sobre o seguinte tópico:
    
    Matéria: {materia}
    Tópico do Edital: {topico}
    
    A questão deve ser desafiadora, mas justa, similar às encontradas nas provas reais.
    
    Responda APENAS com um objeto JSON. O JSON deve ter a seguinte estrutura:
    {{
      "pergunta": "O enunciado completo da pergunta...",
      "opcoes": [
        "a) Texto da alternativa A",
        "b) Texto da alternativa B",
        "c) Texto da alternativa C",
        "d) Texto da alternativa D"
      ],
      "correta": "c) Texto da alternativa C",
      "explicacao": "Uma explicação detalhada do porquê esta é a resposta certa e as outras estão erradas."
    }}
    """

    # --- MELHORIA 2: MODELO CORRIGIDO ---
    # 1. Chama a API com o modelo mais inteligente
    json_string = _make_api_call(
        system_prompt=system,
        user_prompt=user,
        model="gpt-4o", # Modelo potente para garantir a matemática correta
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    
    # 2. Verifica se a API retornou um erro
    if json_string.startswith("❌"):
        print(f"Erro ao gerar questão: {json_string}")
        return None

    # 3. Tenta fazer o parse do JSON (o erro agora é só aqui)
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON da IA: {e}")
        print(f"String recebida: {json_string}")
        return None


def ask_quick_question(pergunta: str) -> str:
    """
    Responde perguntas rápidas, como um dicionário ou um professor tira-dúvidas.
    """
    system = (
        "Você é um professor 'tira-dúvidas' para uma aluna de 14 anos. "
        "Sua especialidade é a prova da ETE (Pernambuco). "
        "Responda de forma direta, simples e muito didática. "
        "Se for uma definição de palavra, dê o significado e um exemplo de uso."
    )

    user = f"""
    Dúvida da aluna:
    "{pergunta}"
    """
    
    # Chama a função central com o modelo rápido
    return _make_api_call(
        system_prompt=system,
        user_prompt=user,
        model="gpt-5-mini", # Rápido e barato para dúvidas
        temperature=0.3
    )