import html
import os
import json
import re
import sympy as sp
import math
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
# 🔹 Geração de questão de MATEMÁTICA (CORRIGIDA)
# =====================================================
def generate_math_question(materia: str, topico: str) -> dict | None:
    system = (
        "Você é um assistente de IA especialista em criar questões de matemática para o vestibular da ETE. "
        "Crie uma pergunta de múltipla escolha com 4 alternativas (a, b, c, d) "
        "e inclua a equação SymPy correspondente, que o Python poderá resolver. "
        
        # --- REFORÇO NO PROMPT DE SISTEMA ---
        "\n\n🚨 REGRAS DE TÓPICO (MUITO IMPORTANTE):"
        "\n1. Se o Tópico for 'Problemas com as Quatro Operações', a pergunta DEVE ser um 'problema' (word problem)."
        "\n2. Se o Tópico for 'Equações', a pergunta PODE ser uma equação direta."
        "\n3. 🚫 NUNCA use o símbolo 'R$'. Escreva a palavra 'reais' por extenso. (Ex: '5 reais')."
        "\n4. NUNCA COLE PONTUAÇÕES, SÍMBOLOS OU LETRAS UNS NOS OUTROS."
        
        # --- NOVA REGRA CRÍTICA (A SOLUÇÃO) ---
        "\n5. 🚨 A RESPOSTA CORRETA (calculada pela 'equacao_para_sympy') DEVE ESTAR INCLUÍDA EM UMA DAS 'opcoes'. "
        "VERIFIQUE SUA PRÓPRIA MATEMÁTICA ANTES DE RESPONDER. ESTA É A REGRA MAIS IMPORTANTE."
        # --- FIM DO REFORÇO ---
    )
    
    # --- PROMPT DE USUÁRIO CORRIGIDO COM "REAIS" ---
    user = f"""
Matéria: {materia}
Tópico: {topico}

Responda apenas com JSON no formato. Siga o exemplo mais apropriado para o tópico:

EXEMPLO DE "PROBLEMA" (Tópicos como 'Problemas com as Quatro Operações', 'Porcentagem', etc.):
{{
  "pergunta": "Uma loja vendeu 15 camisas por 45 reais cada. Desse total, 200 reais foram usados para pagar o aluguel. Quanto sobrou no caixa?",
  "opcoes": ["a) 450 reais", "b) 475 reais", "c) 500 reais", "d) 675 reais"],
  "equacao_para_sympy": "(15 * 45) - 200",
  "variavel_solucao": null,
  "explicacao": "💡 Vamos lá! Primeiro, o total da venda: 15 camisas x 45 reais = 675 reais. Depois, tiramos o aluguel: 675 reais - 200 reais = 475 reais. ✅"
}}

EXEMPLO DE "EQUAÇÃO DIRETA" (Tópicos como 'Equações Algébricas'):
{{
  "pergunta": "Resolva: 2x + 4 = 10",
  "opcoes": ["a) 2", "b) 3", "c) 4", "d) 5"],
  "equacao_para_sympy": "Eq(2*x + 4, 10)",
  "variavel_solucao": "x",
  "explicacao": "💡 Vamos isolar o 'x'! Passamos o 4 subtraindo: 2x = 10 - 4, que dá 2x = 6. Agora, passamos o 2 dividindo: x = 6 / 2. ✅ O resultado é x = 3."
}}
"""
    # Usamos gpt-4o-mini aqui, pois o gpt-5-mini falha mais
    return _generate_question(system, user, {"type": "json_object"})

# É CRUCIAL que _generate_question use um modelo bom
def _generate_question(system_prompt, user_prompt, response_format):
    json_string = _make_api_call(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model="gpt-4o-mini", # <--- gpt-4o-mini é MELHOR em seguir regras que gpt-5-mini
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
# 🔹 Geração de questão de PORTUGUÊS
# =====================================================
def generate_portuguese_question(materia: str, topico: str) -> dict | None:
    system = (
        "Você é um criador de questões de português para o vestibular da ETE. "
        "Crie questões focadas na **APLICAÇÃO PRÁTICA** das regras (análise de frases, identificação de erros, função em um trecho) "
        "e **NÃO APENAS em definições teóricas**. " # <-- ADIÇÃO 1
        "A questão deve ter:\n"
        "1️⃣ Um pequeno texto-base (3 a 5 linhas) coerente e claro.\n"
        "2️⃣ Uma pergunta de **análise ou aplicação** sobre o texto, baseada no tópico fornecido.\n" # <-- ADIÇÃO 2
        "3️⃣ Quatro alternativas (a, b, c, d).\n"
        "4️⃣ O campo 'correta' com a alternativa certa.\n"
        "5️⃣ Uma explicação textual mostrando por que essa é a correta.\n"
        "⚠️ Formate tudo como JSON bem estruturado."
    )
    user = f"""
Matéria: {materia}
Tópico: {topico}

**Instrução Importante:** A pergunta deve ser sobre a **APLICAÇÃO PRÁTICA** do tópico '{topico}',
não uma pergunta teórica ou de definição.
(Ex: Se o tópico for 'Pontuação', pergunte 'Em qual frase a vírgula foi usada incorretamente?' ou 'Qual a função da vírgula no trecho X?').
(Ex: Se o tópico for 'Conectivos', pergunte 'O conectivo "mas" no texto indica:').

Responda apenas com JSON no formato:
{{
 "pergunta": "O texto-base que você criou... seguido da pergunta específica de aplicação.",
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
        "IMPORTANTE: NUNCA use o símbolo 'R$'. Sempre escreva 'reais' (ex: '5 reais').\n\n"
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
    # 1. Armazena a resposta bruta da API
    resposta_bruta = _make_api_call(system_prompt=system, user_prompt=user, model="gpt-5-mini", temperature=1)

    # 2. Limpa o texto antes de retornar
    return limpar_texto_pergunta(resposta_bruta)

def ask_quick_question(pergunta: str) -> str:
    """Responde perguntas rápidas e didáticas."""
    system = (
        "Você é um professor tira-dúvidas da ETE. "
        "Explique de forma simples, direta e com exemplos. "
        "Se for um conceito, dê uma frase explicando e um exemplo."
    )
    user = f"Dúvida da aluna: {pergunta}"
    return _make_api_call(system_prompt=system, user_prompt=user, model="gpt-5-mini", temperature=1)

def limpar_texto_pergunta(texto: str) -> str:
    """
    Corrige textos bugados vindos da IA:
    - CONVERTE 'R$' e 'R15' para 'reais'.
    - Remove ruído de letras soltas.
    - Separa texto grudado (ex: 5,00porquilo).
    """

    if not texto:
        return texto

    # 1️⃣ Decodifica HTML e Normaliza (fundamental para corrigir hífens e acentos)
    texto = html.unescape(texto)
    texto = unicodedata.normalize('NFKC', texto)
    
    # 2️⃣ CORREÇÃO CRÍTICA 1: Converte R$ para 'reais'
    # "R$ 5" ou "R$5" -> " 5 reais"
    texto = re.sub(r"R\$\s*([\d,.]+)", r" \1 reais", texto)
    
    # 3️⃣ CORREÇÃO CRÍTICA 2: Converte R15, R3, R5,00 para 'reais'
    # "R15" -> "15 reais"
    # "R5,00" -> "5,00 reais"
    texto = re.sub(r"R([\d,.]+)", r" \1 reais", texto)

    # 4️⃣ Remove ruído de caracteres minúsculos soltos (o 'g anh o u')
    texto = re.sub(r'[\s.,;!?:]{1}[a-z][\s.,;!?:]{1}', ' ', texto) 

    # 5️⃣ Adiciona espaço após pontuações grudadas
    texto = re.sub(r'([.,;!?:])([A-Za-z])', r'\1 \2', texto) 
    
    # 6️⃣ Corrige números/palavras grudados (O "5,00porquilo")
    texto = re.sub(r"(\d)([A-Za-z])", r"\1 \2", texto)  
    texto = re.sub(r"([A-Za-z])(\d)", r"\1 \2", texto)  
    texto = re.sub(r"(\d[,.]\d{2})([A-Za-z])", r"\1 \2", texto)

    # 7️⃣ Final: remove espaços excessivos e corrige pontuação
    texto = re.sub(r"\s+", " ", texto).strip()
    texto = re.sub(r"\s+([.,!?:;])", r"\1", texto)
    texto = re.sub(r"\.([A-Z])", r". \1", texto)

    return texto

def generate_speech(text_to_speak: str, voice: str = "nova") -> bytes | None:
    """
    Gera o áudio usando a API de Text-to-Speech (TTS) da OpenAI, forçando o Português do Brasil (pt-BR).
    A voz 'nova' é a mais adequada para o pt-BR.
    """
    try:
        # A instrução SSML (Speech Synthesis Markup Language) é a forma
        # mais robusta de FORÇAR o idioma e sotaque no motor TTS.
        # Envolve a string com as tags <speak> e <lang> para pt-BR.
        ssml_input = f'<speak><lang xml:lang="pt-BR">{text_to_speak}</lang></speak>'

        # Assumindo que _client() retorna o objeto OpenAI (como está configurado no seu código)
        client = _client() 
        
        response = client.audio.speech.create(
            model="tts-1",  
            voice=voice,    # 'nova' é uma voz feminina com sotaque pt-BR
            input=ssml_input, # Agora USAMOS o texto formatado com SSML
            response_format="mp3" 
        )
        
        # Concatena os bytes do áudio
        audio_bytes = b"".join(response.iter_bytes())
        return audio_bytes

    except OpenAIError as e:
        print(f"Erro TTS da OpenAI: {e.message}")
        return None
    except Exception as e:
        print(f"Erro TTS inesperado: {e}")
        return None