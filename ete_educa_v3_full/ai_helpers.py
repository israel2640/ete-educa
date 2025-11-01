import os
import json
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI

# Carrega variáveis do arquivo .env automaticamente
load_dotenv()

@dataclass
class AIConfig:
    api_key_env: str = "OPENAI_API_KEY"
    model: str = "gpt-4o-mini"  # modelo rápido e econômico

def _client(cfg: AIConfig | None = None):
    cfg = cfg or AIConfig()
    api_key = os.getenv(cfg.api_key_env)

    if not api_key:
        raise RuntimeError(f"Defina {cfg.api_key_env} no arquivo .env.")

    # Aceita tanto sk- quanto sk-proj-
    if not api_key.startswith(("sk-", "sk-proj-")):
        raise RuntimeError(
            "Chave OPENAI_API_KEY inválida. Ela deve começar com 'sk-' ou 'sk-proj-'."
        )

    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        raise RuntimeError(f"Erro ao inicializar o cliente OpenAI: {e}")

    return client, cfg

def explain_like_coach(question_text: str, materia: str) -> str:
    """
    Gera explicações educativas e carinhosas para aluna de 14 anos estudando para a ETE.
    Divide a resposta em blocos: Pulo do Gato, Passo a Passo e Por que as outras estão erradas.
    """
    client, cfg = _client()

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

    try:
        resp = client.chat.completions.create(
            model=cfg.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.5,
        )

        return resp.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Erro ao conectar à OpenAI: {e}\nVerifique sua chave e conexão."

# =====================================================
# 🔹 FUNÇÃO ANTIGA - GERAR QUESTÃO (Modo Livre)
# =====================================================
def generate_new_question(materia: str, topico: str) -> dict | None:
    """
    Gera uma nova questão de múltipla escolha no estilo da ETE, 
    retornando um dicionário (JSON).
    """
    client, cfg = _client()

    system = (
        "Você é um assistente de IA especialista em criar questões para o vestibular da ETE de Pernambuco (nível Ensino Médio). "
        "Você cria perguntas originais, no formato de múltipla escolha (4 alternativas: a, b, c, d), "
        "que seguem o estilo e o nível de dificuldade das provas passadas (como as da ETEP)."
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

    try:
        resp = client.chat.completions.create(
            model=cfg.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.7, 
            response_format={"type": "json_object"} 
        )
        
        # Carrega a string JSON para um dicionário Python
        question_data = json.loads(resp.choices[0].message.content)
        return question_data

    except Exception as e:
        print(f"Erro ao gerar questão: {e}")
        return None

# =====================================================
# 🔹 NOVA FUNÇÃO - DICIONÁRIO / DÚVIDA RÁPIDA
# =====================================================
def ask_quick_question(pergunta: str) -> str:
    """
    Responde perguntas rápidas, como um dicionário ou um professor tira-dúvidas.
    """
    client, cfg = _client()

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

    try:
        resp = client.chat.completions.create(
            model=cfg.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.3, # Respostas mais diretas e focadas
        )

        return resp.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Erro ao conectar à OpenAI: {e}\nVerifique sua chave e conexão."