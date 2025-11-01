import os
import json
import random
from typing import Dict, List
# CORREÇÃO: Importar 'questoes' de dentro da pasta 'data'
try:
    from data.questoes import questoes_portugues, questoes_matematica
    ALL_LESSONS = questoes_portugues + questoes_matematica
except ImportError:
    print("AVISO: arquivo 'data/questoes.py' não encontrado ou vazio.")
    ALL_LESSONS = []

# =====================================================
# 🔹 Utilitários básicos
# =====================================================
DATA_DIR = "data"
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")

# =====================================================
# 🔹 Classe principal do motor de questões
# =====================================================
class QuizEngine:
    def __init__(self, questoes_lista: List[Dict]):
        self.questoes = questoes_lista
        self.atual = 0
        self.acertos = 0
        self.erros = 0

    def responder(self, resposta: str) -> (bool, str):
        """Verifica se a resposta está correta e retorna (bool, explicação)."""
        if self.atual >= len(self.questoes):
            return False, "Não há mais questões."
            
        questao = self.questoes[self.atual]
        correta = None
        explicacao = "Explicação não disponível."

        # Procura a resposta dentro de 'train_questions' (para o Modo Estudar)
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
# 🔹 Progresso do usuário (Consolidado)
# =====================================================
DEFAULT_PROGRESS = {
    "aluna1": {
        "portugues": {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0},
        "matematica": {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0},
        "reforco": [], # Lista de IDs de lições
        "nivel": "Bronze"
    }
}

def _ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_progress():
    """Carrega o progresso salvo do usuário."""
    _ensure_dirs()
    if not os.path.exists(PROGRESS_FILE):
        save_progress(DEFAULT_PROGRESS)
        return DEFAULT_PROGRESS
    
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return DEFAULT_PROGRESS

def save_progress(progress):
    """Salva o progresso atual no arquivo JSON."""
    _ensure_dirs()
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def ensure_user(progress, user):
    """Garante que o usuário exista no progresso."""
    if user not in progress:
        progress[user] = {
            "portugues": {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0},
            "matematica": {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0},
            "reforco": [],
            "nivel": "Bronze"
        }
    # Garante que as chaves de matéria existam
    if "portugues" not in progress[user]:
         progress[user]["portugues"] = {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0}
    if "matematica" not in progress[user]:
        progress[user]["matematica"] = {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0}
    if "reforco" not in progress[user]:
        progress[user]["reforco"] = []
        
    return progress

# =====================================================
# 🔹 Funções auxiliares do treino/reforço
# =====================================================
def shuffled_options(options):
    """Retorna as alternativas embaralhadas."""
    opts = list(options)
    random.shuffle(opts)
    return opts

def add_reforco(progress, user, lesson_id):
    """Adiciona uma lição à lista DE REFORÇO global."""
    if lesson_id not in progress[user]["reforco"]:
        progress[user]["reforco"].append(lesson_id)

def set_train_ok(progress, user, subject_key, lesson_id):
    """Marca uma lição como concluída no treino."""
    progress[user][subject_key]["treinos_ok"] = progress[user][subject_key].get("treinos_ok", 0) + 1
    # Remove da lista de reforço, se estiver lá
    if lesson_id in progress[user]["reforco"]:
        progress[user]["reforco"].remove(lesson_id)

def set_studied(progress, user, subject_key, lesson_id):
    """Registra que a lição foi estudada (adiciona badge)."""
    if lesson_id not in progress[user][subject_key]["badges"]:
        progress[user][subject_key]["badges"].append(lesson_id)

# =====================================================
# 🔹 Carregamento das lições
# =====================================================
def load_lessons():
    """
    Carrega todas as lições do 'data/questoes.py'.
    """
    if not ALL_LESSONS:
        try:
            from data.questoes import questoes_portugues, questoes_matematica
            return questoes_portugues + questoes_matematica
        except ImportError:
            return [] 
            
    return ALL_LESSONS