import random
# CORREÇÃO: Importar o novo banco de dados de provas
try:
    from data.provas_db import questoes_simulado_portugues, questoes_simulado_matematica
except ImportError: 
    # Se der erro, imprime no terminal (em vez de st.error)
    print("ERRO: Não foi possível encontrar 'data/provas_db.py'")
    questoes_simulado_portugues = []
    questoes_simulado_matematica = []


def gerar_prova(materia: str, n_questoes: int) -> list:
    """
    Gera uma prova simulada buscando questões reais do 
    banco de dados 'data/provas_db.py'.
    """
    
    if materia.lower() == "português":
        todas_as_questoes = questoes_simulado_portugues
    else:
        todas_as_questoes = questoes_simulado_matematica
            
    if not todas_as_questoes:
        return [] # Retorna vazio se não achar nenhuma

    # Se o número pedido (n_questoes) for maior que o disponível, usa o máximo
    if n_questoes > len(todas_as_questoes):
        n_questoes = len(todas_as_questoes)

    # Embaralha e seleciona o número de questões pedido
    random.shuffle(todas_as_questoes)
    return todas_as_questoes[:n_questoes]