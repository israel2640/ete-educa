# data/provas_db.py (COM A NOVA CHAVE "lesson_id")

questoes_simulado_portugues = [
    {
        "ano": 2024,
        "tema": "Interpretação de Poema",
        "lesson_id": "POR_01", # <--- ADICIONADO
        "texto_contexto": "...",
        "pergunta": "No poema 'TEMOR', ...",
        "alternativas": [
            "Medo de não alcançar a felicidade...",
            "Medo da tristeza.",
            "Medo de ser feliz.",
            "Medo de não viver os breves momentos."
        ],
        "correta": "Medo de ser feliz.",
        "explicacao": "O gabarito oficial (2024, Q.01) indica 'C'..."
    },
    {
        "ano": 2024,
        "tema": "Conectivos (Sintaxe)",
        "lesson_id": "POR_09", # <--- ADICIONADO (Ref. POR_09: Conectivos)
        "pergunta": "No trecho 'Deleita o gosto, assim saboreada, / Porém, ...",
        "alternativas": ["Conclusão.","Oposição.","Finalidade.","Condição."],
        "correta": "Oposição.",
        "explicacao": "O gabarito oficial (2024, Q.04) indica 'B'..."
    },
    {
        "ano": 2024,
        "tema": "Crônica - Interpretação",
        "lesson_id": "POR_01", # <--- ADICIONADO (Ref. POR_01: Compreensão)
        "texto_contexto": "**SIMPLICIDADE** ...",
        "pergunta": "De acordo com o texto de Martha Medeiros, ...",
        "alternativas": [
            "Nos ajuda a realizar as atividades de forma prática e ágil.",
            "As coisas mais belas e atraentes não são fáceis.",
            "Tudo que precisamos é 'rascunhar' nossos desejos.",
            "Precisamos ser objetivos."
        ],
        "correta": "Nos ajuda a realizar as atividades de forma prática e ágil.",
        "explicacao": "Gabarito (2024, Q.06) é 'A'..."
    },
    {
        "ano": 2023,
        "tema": "Gêneros Textuais",
        "lesson_id": "POR_03", # <--- ADICIONADO
        "texto_contexto": "**Eletrônicos: cuidado com o uso em excesso** ...",
        "pergunta": "Levando em consideração o texto 'Eletrônicos: cuidado com o uso em excesso', ...",
        "alternativas": [
            "O texto apresenta e defende uma opinião.",
            "O texto tem por objetivo relatar um fato ocorrido.",
            "Divulgar e relatar uma experiência.",
            "Pertence ao gênero narrativo..."
        ],
        "correta": "O texto apresenta e defende uma opinião.",
        "explicacao": "O gabarito oficial (2023, Q.01) indica 'A'..."
    },
    {
        "ano": 2023,
        "tema": "Crase",
        "lesson_id": "POR_12", # <--- ADICIONADO
        "texto_contexto": "Trechos do texto 'Eletrônicos':\nI) ...",
        "pergunta": "Assinale a opção, referente ao uso da crase, ...",
        "alternativas": ["à - à - às","a - à - às","a - a - as","a - a - às"],
        "correta": "a - a - às",
        "explicacao": "O gabarito oficial (2023, Q.05) indica 'D'..."
    },
]


questoes_simulado_matematica = [
    {
        "ano": 2024,
        "tema": "Frações e Perímetro",
        "lesson_id": "MAT_02", # <--- ADICIONADO (Ref. MAT_02: Frações)
        "pergunta": "A medida do menor lado de um triângulo é 3/5 ...",
        "alternativas": ["60 cm","48 cm","30 cm","28 cm","52 cm"],
        "correta": "48 cm",
        "explicacao": "Gabarito (2024, Q.01) é 'B'..."
    },
    {
        "ano": 2024,
        "tema": "Porcentagem (Pegadinha)",
        "lesson_id": "MAT_11", # <--- ADICIONADO
        "pergunta": "O custo de um pneu é R$ 280,00 ...",
        "alternativas": ["2,5%","3%","25%","30%","35%"],
        "correta": "25%",
        "explicacao": "Gabarito (2024, Q.04) é 'C'..."
    },
    {
        "ano": 2024,
        "tema": "Geometria e Trigonometria",
        "lesson_id": "MAT_21", # <--- ADICIONADO (Ref. MAT_21: Triângulos)
        "texto_contexto": "Foram usadas duas medidas de cabo de aço...",
        "pergunta": "É CORRETO afirmar que a quantidade mínima de cabo...",
        "alternativas": ["10 m","16 m","25 m","24 m","26 m"],
        "correta": "26 m",
        "explicacao": "Gabarito (2024, Q.06) é 'E'..."
    },
    {
        "ano": 2023,
        "tema": "Operações (Decimais)",
        "lesson_id": "MAT_03", # <--- ADICIONADO
        "pergunta": "Davi comprou 3 cadernos, cada um por R$ 7,80...",
        "alternativas": ["R$ 26,60","R$ 26,20","R$ 25,60","R$ 24,40","R$ 23,40"],
        "correta": "R$ 26,60",
        "explicacao": "Gabarito (2023, Q.01) é 'A'..."
    },
    {
        "ano": 2023,
        "tema": "Regra de Três Composta",
        "lesson_id": "MAT_10", # <--- ADICIONADO
        "pergunta": "Se 8 homens levam 12 dias montando 16 máquinas...",
        "alternativas": ["18 dias","3 dias","20 dias","6 dias","16 dias"],
        "correta": "20 dias",
        "explicacao": "Gabarito (2023, Q.09) é 'C'..."
    },
    {
        "ano": 2023,
        "tema": "Teorema de Pitágoras",
        "lesson_id": "MAT_21", # <--- ADICIONADO (Ref. MAT_21: Triângulos/Retângulo)
        "pergunta": "Uma escada de 13 m está encostada no topo de uma parede...",
        "alternativas": ["12 m","11 m","10 m","9 m","8 m"],
        "correta": "12 m",
        "explicacao": "Gabarito (2023, Q.16) é 'A'..."
    }
]