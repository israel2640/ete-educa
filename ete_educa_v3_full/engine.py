import os
import json
import random
import streamlit as st
import base64
from typing import Dict, List, Tuple
from github import Github, UnknownObjectException

# CORREÇÃO: Importar 'questoes' de dentro da pasta 'data'
try:
    from data.questoes import questoes_portugues, questoes_matematica
    ALL_LESSONS = questoes_portugues + questoes_matematica
except ImportError:
    print("AVISO: arquivo 'data/questoes.py' não encontrado ou vazio.")
    ALL_LESSONS = []

# =====================================================
# 🔹 Configuração do GitHub
# =====================================================
PROGRESS_FILE_PATH = "data/progress.json"

@st.cache_resource
def init_github_client():
    token = st.secrets.get("GITHUB_TOKEN")
    repo_name = st.secrets.get("GITHUB_REPO")
    
    if not token or not repo_name:
        print("AVISO: GITHUB_TOKEN ou GITHUB_REPO não encontrados nos segredos.")
        return None, None
        
    try:
        g = Github(token)
        repo = g.get_repo(repo_name)
        return g, repo
    except Exception as e:
        print(f"Erro ao conectar ao GitHub: {e}")
        return None, None

github_client, github_repo = init_github_client()

# =====================================================
# 🔹 Classe principal do motor de questões (Sem Mudança)
# =====================================================
class QuizEngine:
    def __init__(self, questoes_lista: List[Dict]):
        self.questoes = questoes_lista
        self.atual = 0
        self.acertos = 0
        self.erros = 0

    def responder(self, resposta: str) -> tuple[bool, str]:
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
# 🔹 Progresso do usuário (MODIFICADO PARA GITHUB)
# =====================================================
DEFAULT_USER_PROGRESS = {
    "aluna1": {
        "portugues": {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0},
        "matematica": {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0},
        "reforco": [],
        "nivel": "Bronze"
    }
}

# Carrega o progresso de TODOS os usuários do GitHub
@st.cache_data(ttl=60) # Cache de 1 minuto
def load_progress_from_github():
    if not github_repo:
        print("AVISO: Repositório GitHub não conectado. Usando progresso local temporário.")
        return DEFAULT_USER_PROGRESS
    try:
        file = github_repo.get_contents(PROGRESS_FILE_PATH, ref="main")
        content_decoded = base64.b64decode(file.content).decode("utf-8")
        progress_dict = json.loads(content_decoded)
        return progress_dict
    except UnknownObjectException:
        # O arquivo data/progress.json não existe no repo.
        print("AVISO: 'data/progress.json' não encontrado no GitHub. Criando um novo.")
        return DEFAULT_USER_PROGRESS
    except Exception as e:
        print(f"Erro ao carregar progresso do GitHub: {e}")
        return DEFAULT_USER_PROGRESS

# Carrega o dicionário de progresso (AGORA DO GITHUB)
def load_progress():
    return load_progress_from_github()

# Salva o progresso no GitHub
def save_progress(progress: Dict):
    if not github_repo:
        print("AVISO: GitHub não conectado. Progresso não salvo.")
        return

    try:
        data_str = json.dumps(progress, indent=2, ensure_ascii=False)
        user_id = list(progress.keys())[0] if progress else "aluna1"
        commit_message = f"Atualizando progresso de {user_id}"
        
        # Tenta pegar o arquivo para saber o "SHA" (ID da versão)
        try:
            file = github_repo.get_contents(PROGRESS_FILE_PATH, ref="main")
            # Se achou, atualiza o arquivo
            github_repo.update_file(
                path=PROGRESS_FILE_PATH,
                message=commit_message,
                content=data_str,
                sha=file.sha,
                branch="main"
            )
            print("Progresso atualizado no GitHub.")
        except UnknownObjectException:
            # Se não achou, cria o arquivo
            github_repo.create_file(
                path=PROGRESS_FILE_PATH,
                message=commit_message,
                content=data_str,
                branch="main"
            )
            print("Arquivo de progresso criado no GitHub.")

        # Limpa o cache para que a próxima leitura pegue os dados novos
        st.cache_data.clear()
        
    except Exception as e:
        print(f"Erro ao salvar progresso no GitHub: {e}")

# Garante que o usuário exista no dicionário de progresso (sem mudança)
def ensure_user(progress, user):
    if user not in progress:
        progress[user] = DEFAULT_USER_PROGRESS.get("aluna1", {}).copy()
    
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