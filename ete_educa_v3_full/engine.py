import os
import json
import random
import streamlit as st # Importar streamlit para ler os segredos
from typing import Dict, List, Tuple # <--- IMPORTANTE: Adicionar Tuple
from supabase import create_client, Client

# CORREÇÃO: Importar 'questoes' de dentro da pasta 'data'
try:
    from data.questoes import questoes_portugues, questoes_matematica
    ALL_LESSONS = questoes_portugues + questoes_matematica
except ImportError:
    print("AVISO: arquivo 'data/questoes.py' não encontrado ou vazio.")
    ALL_LESSONS = []

# =====================================================
# 🔹 Configuração do Supabase
# =====================================================

@st.cache_resource
def init_supabase_client():
    # Tenta carregar dos segredos do Streamlit (nuvem)
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY")
    
    # Fallback para .env (se rodar localmente)
    if not url or not key:
        from dotenv import load_dotenv
        load_dotenv()
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        print("AVISO: Variáveis SUPABASE_URL ou SUPABASE_KEY não encontradas.")
        return None
        
    try:
        return create_client(url, key)
    except Exception as e:
        print(f"Erro ao conectar ao Supabase: {e}")
        return None

supabase: Client = init_supabase_client()

# =====================================================
# 🔹 Classe principal do motor de questões
# =====================================================
class QuizEngine:
    def __init__(self, questoes_lista: List[Dict]):
        self.questoes = questoes_lista
        self.atual = 0
        self.acertos = 0
        self.erros = 0

    # --- ESTA É A LINHA CORRIGIDA ---
    def responder(self, resposta: str) -> tuple[bool, str]:
    # --- FIM DA CORREÇÃO ---
        """Verifica se a resposta está correta e retorna (bool, explicação)."""
        if self.atual >= len(self.questoes):
            return False, "Não há mais questões."
        
        questao = self.questoes[self.atual]
        correta = None
        explicacao = "Explicação não disponível."

        if "train_questions" in questao and questao["train_questions"]:
            q_treino = questao["train_questions"][0]
            correta = q_treino.get("ans")
            explicacao = q_treino.get("exp", "Sem explicação.")
        
        if not correta:
            correta = questao.get("resposta") or questao.get("ans")
        
        if not explicacao:
            explicacao = questao.get("exp", "Sem explicação.")

        if not resposta or not correta:
            return False, "❌ Nenhuma resposta ou gabarito encontrado."

        acertou = resposta.strip().lower() == correta.strip().lower()
        if acertou:
            self.acertos += 1
            feedback = f"✅ Correto! {explicacao}"
        else:
            self.erros += 1
            feedback = f"❌ Errado! A resposta correta é **{correta}**. \n\n{explicacao}"

        return acertou, feedback

# =====================================================
# 🔹 Progresso do usuário (MODIFICADO PARA SUPABASE)
# =====================================================
DEFAULT_USER_PROGRESS = {
    "portugues": {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0},
    "matematica": {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0},
    "reforco": [],
    "nivel": "Bronze"
}

# Carrega o progresso de TODOS os usuários do Supabase
# Usamos cache para não ler o DB toda hora
@st.cache_data(ttl=60) # Cache de 1 minuto
def load_progress_from_db():
    if not supabase:
        print("AVISO: Supabase não conectado. Usando progresso local temporário.")
        return {} # Retorna vazio se o Supabase não estiver conectado
    try:
        response = supabase.table("user_progress").select("user_id", "progress_data").execute()
        data = response.data
        progress_dict = {}
        for item in data:
            progress_dict[item['user_id']] = item['progress_data']
        return progress_dict
    except Exception as e:
        print(f"Erro ao carregar progresso: {e}")
        return {}

# Carrega o dicionário de progresso (AGORA DO SUPABASE)
def load_progress():
    return load_progress_from_db()

# Salva o progresso no Supabase
def save_progress(progress: Dict):
    if not supabase:
        print("AVISO: Supabase não conectado. Progresso não salvo.")
        return
    
    try:
        # O progresso que recebemos é o dict inteiro.
        # Precisamos salvar usuário por usuário.
        for user_id, data in progress.items():
            supabase.table("user_progress").upsert({
                "user_id": user_id,
                "progress_data": data,
                "updated_at": "now()"
            }).execute()
        
        # Limpa o cache para que a próxima leitura pegue os dados novos
        st.cache_data.clear()
        
    except Exception as e:
        print(f"Erro ao salvar progresso: {e}")

# Garante que o usuário exista no dicionário de progresso
def ensure_user(progress, user):
    if user not in progress:
        progress[user] = DEFAULT_USER_PROGRESS.copy()
    
    # Garante que as chaves de matéria existam
    if "portugues" not in progress[user]:
         progress[user]["portugues"] = {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0}
    if "matematica" not in progress[user]:
        progress[user]["matematica"] = {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0}
    if "reforco" not in progress[user]:
        progress[user]["reforco"] = []
        
    return progress

# =====================================================
# 🔹 Funções auxiliares do treino/reforço (sem mudança)
# =====================================================
def shuffled_options(options):
    opts = list(options)
    random.shuffle(opts)
    return opts

def add_reforco(progress, user, lesson_id):
    if lesson_id not in progress[user]["reforco"]:
        progress[user]["reforco"].append(lesson_id)

def set_train_ok(progress, user, subject_key, lesson_id):
    progress[user][subject_key]["treinos_ok"] = progress[user][subject_key].get("treinos_ok", 0) + 1
    if lesson_id in progress[user]["reforco"]:
        progress[user]["reforco"].remove(lesson_id)

def set_studied(progress, user, subject_key, lesson_id):
    if lesson_id not in progress[user]["badges"]:
        progress[user][subject_key]["badges"].append(lesson_id)

# =====================================================
# 🔹 Carregamento das lições (sem mudança)
# =====================================================
def load_lessons():
    if not ALL_LESSONS:
        try:
            from data.questoes import questoes_portugues, questoes_matematica
            return questoes_portugues + questoes_matematica
        except ImportError:
            return [] 
    return ALL_LESSONS