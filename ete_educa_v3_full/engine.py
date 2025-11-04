import os
import json
import random
import streamlit as st
import base64
from typing import Dict, List, Tuple, Optional, Any
from github import Github, UnknownObjectException

# CORREÇÃO: Importar 'questoes' de dentro da pasta 'data'
try:
    from data.questoes import questoes_portugues, questoes_matematica
    ALL_LESSONS = questoes_portugues + questoes_matematica
except ImportError:
    print("AVISO: arquivo 'data/questoes.py' não encontrado ou vazio.")
    ALL_LESSONS = []

# =====================================================
# 🔹 Configuração do GitHub (Sua lógica)
# =====================================================
PROGRESS_FILE_PATH = "data/progress.json"

@st.cache_resource
def init_github_client():
    """Sua função original para inicializar o cliente GitHub."""
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

# =====================================================
# 🔹 Classe principal do motor de questões (Sua lógica)
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
# 🔹 Progresso Padrão (Sua lógica)
# =====================================================
DEFAULT_USER_PROGRESS = {
    "aluna1": {
        "password": "123", # Senha padrão para o usuário padrão
        "portugues": {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0},
        "matematica": {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0},
        "reforco": [],
        "plano_14_dias": {str(dia+1): False for dia in range(14)},
        "nivel_atual": "Bronze"
    }
}

# =====================================================
# 🔹 NOVO: Padrão Singleton - ProgressManager
# =====================================================
class ProgressManager:
    """
    Esta classe usa o padrão Singleton.
    Ela garante que SÓ EXISTA UMA instância dela em toda a aplicação.
    Ela carrega o 'progress.json' do GitHub UMA VEZ e o gerencia em memória.
    """
    _instance: Optional['ProgressManager'] = None
    
    # 1. A "mágica" do Singleton
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ProgressManager, cls).__new__(cls)
        return cls._instance

    # 2. O __init__ só roda na primeira vez
    def __init__(self):
        if not hasattr(self, 'initialized'):
            # Pega a conexão cacheada do GitHub
            self.github_client, self.github_repo = init_github_client()
            
            # Carrega o progresso do GitHub (ou o padrão) UMA VEZ para a memória
            self.progress_data: Dict[str, Any] = self._load_progress_from_github()
            self.initialized: bool = True

    # --- Métodos Internos (Sua lógica do GitHub) ---

    def _load_progress_from_github(self) -> Dict[str, Any]:
        """Carrega o progresso do GitHub. (Adaptado da sua função)"""
        if not self.github_repo:
            print("AVISO: Repositório GitHub não conectado. Usando progresso local temporário.")
            return DEFAULT_USER_PROGRESS
        
        try:
            file = self.github_repo.get_contents(PROGRESS_FILE_PATH, ref="main")
            content_decoded = base64.b64decode(file.content).decode("utf-8")
            progress_dict = json.loads(content_decoded)
            return progress_dict
        except UnknownObjectException:
            # O arquivo data/progress.json não existe no repo.
            print("AVISO: 'data/progress.json' não encontrado no GitHub. Usando padrão.")
            # Retorna o padrão, mas não salva ainda.
            return DEFAULT_USER_PROGRESS
        except Exception as e:
            print(f"Erro ao carregar progresso do GitHub: {e}")
            return DEFAULT_USER_PROGRESS

    def save_progress(self):
        """Salva o progresso da MEMÓRIA para o GitHub. (Adaptado da sua função)"""
        if not self.github_repo:
            print("AVISO: GitHub não conectado. Progresso não salvo.")
            return

        try:
            # Pega os dados ATUAIS da memória (self.progress_data)
            data_str = json.dumps(self.progress_data, indent=2, ensure_ascii=False)
            commit_message = f"Atualizando progresso ETE_Educa"
            
            # Tenta pegar o arquivo para saber o "SHA" (ID da versão)
            try:
                file = self.github_repo.get_contents(PROGRESS_FILE_PATH, ref="main")
                # Se achou, atualiza o arquivo
                self.github_repo.update_file(
                    path=PROGRESS_FILE_PATH,
                    message=commit_message,
                    content=data_str,
                    sha=file.sha,
                    branch="main"
                )
                print("Progresso atualizado no GitHub.")
            except UnknownObjectException:
                # Se não achou, cria o arquivo
                self.github_repo.create_file(
                    path=PROGRESS_FILE_PATH,
                    message=commit_message + " (criação)",
                    content=data_str,
                    branch="main"
                )
                print("Arquivo de progresso criado no GitHub.")

            # Limpa o cache para que a próxima *sessão* de usuário carregue do zero
            st.cache_data.clear()
            
        except Exception as e:
            print(f"Erro ao salvar progresso no GitHub: {e}")

    # --- Métodos Públicos (Suas funções, agora como métodos) ---
    
    def get_progress(self) -> Dict[str, Any]:
        """Retorna o dicionário de progresso que está em memória."""
        return self.progress_data

    def ensure_user(self, user, password):
        """Garante que o usuário exista no progresso (em memória)."""
        if user not in self.progress_data:
            self.progress_data[user] = {
                "password": password, 
                "portugues": {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0},
                "matematica": {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0},
                "reforco": [],
                "plano_14_dias": {str(dia+1): False for dia in range(14)}, 
                "nivel_atual": "Bronze"
            }
        
        # Garante que as chaves de matéria existam (para perfis antigos)
        if "portugues" not in self.progress_data[user]:
             self.progress_data[user]["portugues"] = {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0}
        if "matematica" not in self.progress_data[user]:
            self.progress_data[user]["matematica"] = {"treinos_ok": 0, "erros": [], "badges": [], "simulados": 0}
        if "reforco" not in self.progress_data[user]:
            self.progress_data[user]["reforco"] = []
        if "plano_14_dias" not in self.progress_data[user]:
            self.progress_data[user]["plano_14_dias"] = {str(dia+1): False for dia in range(14)}
        
        # Não precisa retornar 'progress', pois estamos modificando self.progress_data

    def add_reforco(self, user, lesson_id):
        if lesson_id not in self.progress_data[user]["reforco"]:
            self.progress_data[user]["reforco"].append(lesson_id)

    def set_train_ok(self, user, subject_key, lesson_id):
        self.progress_data[user][subject_key]["treinos_ok"] = self.progress_data[user][subject_key].get("treinos_ok", 0) + 1
        if lesson_id in self.progress_data[user]["reforco"]:
            self.progress_data[user]["reforco"].remove(lesson_id)

    def set_studied(self, user, subject_key, lesson_id):
        if "badges" not in self.progress_data[user][subject_key]:
            self.progress_data[user][subject_key]["badges"] = []
        if lesson_id not in self.progress_data[user][subject_key]["badges"]:
            self.progress_data[user][subject_key]["badges"].append(lesson_id)

    def delete_user(self, user, password) -> tuple[bool, str]:
        """Remove um usuário do progresso (em memória) e salva no GitHub."""
        if user not in self.progress_data:
            return False, "Usuário não encontrado."
            
        saved_password = self.progress_data[user].get("password")
        if not saved_password:
            return False, "Perfil antigo sem senha, não pode ser deletado."
        
        if password != saved_password:
            return False, "Senha incorreta. Você só pode deletar seu próprio perfil."

        try:
            self.progress_data.pop(user)
            self.save_progress() # <--- Salva a mudança no GitHub
            return True, f"Perfil '{user}' deletado com sucesso."
        except Exception as e:
            return False, f"Erro ao deletar perfil: {e}"

    def check_user_login(self, user, password) -> tuple[bool, str]:
        """Verifica se o usuário existe e a senha está correta (em memória)."""
        if user not in self.progress_data:
            return False, "Usuário não encontrado."
        
        saved_password = self.progress_data[user].get("password")
        if not saved_password:
            return False, "Este perfil é antigo e não tem senha. Por favor, crie um novo."

        if password == saved_password:
            return True, "Login com sucesso."
        else:
            return False, "Senha incorreta."

# =====================================================
# 🔹 NOVO: Função de Acesso ao Singleton
# =====================================================
@st.cache_resource
def get_progress_manager() -> ProgressManager:
    """
    Função global para obter a instância ÚNICA do ProgressManager.
    Todas as páginas do Streamlit devem usar ESTA função.
    """
    return ProgressManager()

# =f====================================================
# 🔹 Funções Utilitárias (Sua lógica, sem mudanças)
# =====================================================
def shuffled_options(options):
    """Retorna as alternativas embaralhadas."""
    opts = list(options)
    random.shuffle(opts)
    return opts

def load_lessons():
    """Carrega todas as lições (sem mudança)."""
    if not ALL_LESSONS:
        try:
            from data.questoes import questoes_portugues, questoes_matematica
            return questoes_portugues + questoes_matematica
        except ImportError:
            return [] 
    return ALL_LESSONS