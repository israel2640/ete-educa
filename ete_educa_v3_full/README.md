# ETE_Educa v3 (OpenAI opcional) — Local
Foco: ETE Integrado (PE). Fluxo pedagógico **Aprender → Treinar → Desafiar**, com **Reforço** e **Plano (14 dias)**.

## Rodar local
```
pip install -r requirements.txt
# opcional: criar .env com a chave
# echo OPENAI_API_KEY=sk-... > .env
streamlit run app.py
```

## Modos
- **Estudar**: mini-aulas.
- **Treinar**: 3 questões por lição (ganha selo se acertar ≥2).
- **Desafiar (Simulado)**: questões de prova; itens errados vão para Reforço.
- **Reforço**: fila automática dos tópicos com mais erros.
- **Revisão com IA**: usa OpenAI (se tiver .env).
- **Plano (14 dias)**: agenda sugerida até a prova.
