# -*- coding: utf-8 -*-
# =====================================================
# Banco de Dados de Lições e Questões
# BASEADO NO EDITAL ETE INTEGRADO 2026 (ITENS 12.1 E 12.2)
# =====================================================

# =====================================================
# 🔹 QUESTÕES DE PORTUGUÊS (12.1)
# =====================================================
questoes_portugues = [
    {
        "id": "POR_01",
        "subject": "portugues",
        "title": "Compreensão de Texto (Ideias Principais)",
        "lesson_text": "Compreender um texto é saber do que ele fala. A 'Ideia Principal' é a mensagem central que o autor quer passar, o 'resumo do resumo'. As 'Ideias Secundárias' são as explicações, exemplos ou detalhes que apoiam essa ideia principal.",
        "example": "Texto: 'O Brasil precisa investir em educação. Escolas melhores formam cidadãos mais críticos e preparam melhor para o mercado de trabalho.'\nIdeia Principal: A necessidade de investir em educação.\nIdeias Secundárias: Formar cidadãos críticos e preparar para o trabalho.",
        "train_questions": [
            {
                "q": "O que é a 'Ideia Principal' de um texto?",
                "opts": [
                    "Uma palavra bonita que o autor usou.",
                    "A mensagem central e mais importante do texto.",
                    "Um exemplo ou detalhe específico.",
                    "A primeira frase do texto, obrigatoriamente."
                ],
                "ans": "A mensagem central e mais importante do texto.",
                "exp": "A Ideia Principal é o 'coração' do texto, a tese que o autor está defendendo ou o fato principal que ele está contando."
            }
        ]
    },
    {
        "id": "POR_02",
        "subject": "portugues",
        "title": "Textualidade (Coesão e Coerência)",
        "lesson_text": "Para um texto fazer sentido, ele precisa de duas coisas: Coesão e Coerência.\n1. **Coerência:** É o sentido lógico. Não pode ter contradições (ex: 'A noite estava clara').\n2. **Coesão:** É a 'cola' do texto. São as palavras que ligam as frases (pronomes, conectivos).",
        "example": "Em 'Ele foi mal na prova, **pois** não estudou.', a palavra 'pois' é a **coesão** (a cola) que dá **coerência** (sentido lógico) à frase.",
        "train_questions": [
            {
                "q": "Qual palavra dá 'coesão' (liga as ideias) na frase: 'Estudei muito, PORÉM fui mal'?",
                "opts": [
                    "Estudei",
                    "Porém",
                    "Mal",
                    "Muito"
                ],
                "ans": "Porém",
                "exp": "'Porém' é o conectivo (a cola) que liga as duas ideias, criando um sentido de oposição."
            }
        ]
    },
    {
        "id": "POR_03",
        "subject": "portugues",
        "title": "Gêneros Textuais e Sequências",
        "lesson_text": "Gêneros são os 'tipos' de texto. O tipo é definido pelo objetivo.\n- **Narração:** Contar uma história (conto, fábula).\n- **Descrição:** Dizer como algo é (retrato falado, cardápio).\n- **Argumentação:** Defender uma opinião (artigo de opinião).\n- **Exposição:** Explicar um fato sem opinar (notícia, verbete).\n- **Injunção:** Dar uma ordem ou instrução (receita, manual).",
        "example": "Uma **receita de bolo** é do gênero 'Receita' e usa a sequência **injuntiva** (ex: 'Bata os ovos...').",
        "train_questions": [
            {
                "q": "Um manual de instruções de um videogame, que diz 'Aperte X para pular', usa qual sequência textual?",
                "opts": [
                    "Narração (conta uma história)",
                    "Injunção (dá uma instrução)",
                    "Descrição (detalha o personagem)",
                    "Argumentação (defende que o jogo é bom)"
                ],
                "ans": "Injunção (dá uma instrução)",
                "exp": "Textos que dão ordens, comandos ou instruções (como receitas, manuais, leis) são injuntivos."
            }
        ]
    },
    {
        "id": "POR_04",
        "subject": "portugues",
        "title": "Semântica (Sentido das Palavras)",
        "lesson_text": "Semântica é o estudo do significado das palavras.\n- **Sinônimos:** Sentido parecido (bonito / lindo).\n- **Antônimos:** Sentido oposto (cheio / vazio).\n- **Homonímia:** Mesma pronúncia, sentido diferente (Sessão / Seção / Cessão).\n- **Paronímia:** Palavras parecidas (Comprimento / Cumprimento).\n- **Polissemia:** Uma palavra com vários sentidos (Ex: 'Banco' de sentar e 'banco' de dinheiro).",
        "example": "Dizer 'ele é mau' (antônimo de bom) é diferente de 'ele está mal' (antônimo de bem).",
        "train_questions": [
            {
                "q": "As palavras 'acender' (atear fogo) e 'ascender' (subir) são:",
                "opts": [
                    "Sinônimos (mesmo sentido)",
                    "Antônimos (sentido oposto)",
                    "Parônimos (som parecido, escrita e sentido diferentes)",
                    "Polissêmicas (uma palavra com vários sentidos)"
                ],
                "ans": "Parônimos (som parecido, escrita e sentido diferentes)",
                "exp": "Parônimos são pares que 'enganam' por serem parecidos no som ou na escrita, mas têm significados totalmente diferentes."
            }
        ]
    },
    {
        "id": "POR_05",
        "subject": "portugues",
        "title": "Figuras de Linguagem (Conotação/Denotação)",
        "lesson_text": "Denotação e Conotação são os dois 'níveis' de sentido.\n- **Denotação:** O sentido real, do dicionário. (Ex: 'Meu cachorro morreu.').\n- **Conotação:** O sentido figurado, simbólico. (Ex: 'Estou morrendo de fome.').\nAs Figuras de Linguagem (Metáfora, Hipérbole, Ironia) usam a Conotação.",
        "example": "'Engoli um sapo' é **conotação** (sentido figurado de aguentar algo calado). 'Engoli um pão' é **denotação** (sentido real).",
        "train_questions": [
            {
                "q": "Qual frase usa o sentido CONOTATIVO (figurado)?",
                "opts": [
                    "Aquele político é uma raposa.",
                    "O leão fugiu do zoológico.",
                    "Comprei uma bicicleta nova.",
                    "A água ferveu a 100 graus."
                ],
                "ans": "Aquele político é uma raposa.",
                "exp": "Ninguém está dizendo que o político é o animal (denotação). 'Raposa' aqui é usado no sentido figurado (conotação) de 'esperto', 'astuto'. Isso é uma metáfora."
            }
        ]
    },
    {
        "id": "POR_06",
        "subject": "portugues",
        "title": "Norma Padrão e Variedades Linguísticas",
        "lesson_text": "Não existe jeito 'certo' ou 'errado' de falar, existe o 'adequado' para a situação.\n- **Norma Padrão (Formal):** Usada em documentos, entrevistas, na escola. (Ex: 'Solicito a vossa presença.').\n- **Variedade Coloquial (Informal):** Usada com amigos, família. (Ex: 'E aí, beleza?').\n- **Variações Regionais:** Sotaques e gírias de cada lugar (Ex: 'Oxente', 'Mermão').",
        "example": "Falar 'Nós vai' é inadequado na redação da ETE (que exige a Norma Padrão: 'Nós vamos'), mas é comum e aceito na fala informal.",
        "train_questions": [
            {
                "q": "Dizer 'oxente' ou 'massa' (típico de Pernambuco) é um exemplo de qual variedade linguística?",
                "opts": [
                    "Norma Padrão",
                    "Variedade Regional",
                    "Linguagem Formal",
                    "Inadequação gramatical"
                ],
                "ans": "Variedade Regional",
                "exp": "Variações regionais (regionalismos) são as marcas da fala de um determinado local e são parte da riqueza da língua."
            }
        ]
    },
    {
        "id": "POR_07",
        "subject": "portugues",
        "title": "Estrutura e Formação das Palavras",
        "lesson_text": "Palavras são como 'Lego'. O pedaço principal é o **Radical** (carrega o sentido). O que vem antes é o **Prefixo** (muda o sentido). O que vem depois é o **Sufixo** (muda a classe).",
        "example": "Palavra: 'INFELIZMENTE'\n- **FELIZ**: Radical (o sentido principal)\n- **IN-**: Prefixo (negação)\n- **-MENTE**: Sufixo (transforma em advérbio de modo)",
        "train_questions": [
            {
                "q": "Na palavra 'REFAZER', o pedaço 'RE-' é um:",
                "opts": [
                    "Radical (ideia principal)",
                    "Prefixo (indica repetição)",
                    "Sufixo (indica modo)",
                    "Vogal temática"
                ],
                "ans": "Prefixo (indica repetição)",
                "exp": "O radical é 'FAZER'. O 'RE-' vem antes, sendo um prefixo que significa 'fazer de novo'."
            }
        ]
    },
    {
        "id": "POR_08",
        "subject": "portugues",
        "title": "Classes Gramaticais",
        "lesson_text": "É o 'time' que cada palavra joga.\n- **Substantivo:** Dá nome (casa, Deus, amor).\n- **Adjetivo:** Dá qualidade (bonito, alto, azul).\n- **Verbo:** Indica ação, estado ou fenômeno (correr, ser, chover).\n- **Advérbio:** Modifica o verbo/adjetivo (Hoje, Muito, Rapidamente).\n- **Pronome:** Substitui o nome (Eu, ele, ela, meu, seu).\n- **Preposição:** Liga palavras (de, com, para, em).",
        "example": "Em 'Meu cachorro rápido correu muito', temos:\n- *Meu*: Pronome\n- *cachorro*: Substantivo\n- *rápido*: Adjetivo\n- *correu*: Verbo\n- *muito*: Advérbio",
        "train_questions": [
            {
                "q": "Na frase 'O debate foi MUITO bom', a palavra 'MUITO' pertence a qual classe?",
                "opts": [
                    "Adjetivo (dá qualidade)",
                    "Substantivo (dá nome)",
                    "Advérbio (intensifica o 'bom')",
                    "Verbo (indica ação)"
                ],
                "ans": "Advérbio (intensifica o 'bom')",
                "exp": "'Bom' é um adjetivo. 'Muito' é um advérbio de intensidade que está dando 'força' ao adjetivo 'bom'."
            }
        ]
    },
    {
        "id": "POR_09",
        "subject": "portugues",
        "title": "Conectivos (Coordenação e Subordinação)",
        "lesson_text": "Conectivos (ou Conjunções) são as 'colas' que ligam orações (frases com verbo).\n- **Coordenação:** Liga ideias independentes. Principais:\n  - *Adição:* E, NEM (Gosto de sorvete E de açaí).\n  - *Oposição:* MAS, PORÉM (Corri, MAS não cansei).\n  - *Explicação:* POIS, PORQUE (Vim, POIS choveu).\n  - *Conclusão:* LOGO, PORTANTO (Estudei, LOGO passei).\n- **Subordinação:** Liga uma ideia dependente. (Ex: 'Disse QUE viria', 'Vim QUANDO choveu').",
        "example": "Na frase 'Queria ir à praia, MAS choveu', o 'MAS' é um conectivo coordenado de oposição.",
        "train_questions": [
            {
                "q": "Na frase 'Vou dormir, POIS estou cansado', o conectivo 'POIS' dá uma ideia de:",
                "opts": [
                    "Oposição (ideia contrária)",
                    "Adição (soma de ideias)",
                    "Explicação (o motivo)",
                    "Conclusão (o resultado)"
                ],
                "ans": "Explicação (o motivo)",
                "exp": "'Pois' (assim como 'porque' ou 'que') é usado para dar o motivo, a causa ou a explicação de algo dito antes."
            }
        ]
    },
    {
        "id": "POR_10",
        "subject": "portugues",
        "title": "Pontuação",
        "lesson_text": "A pontuação organiza a escrita.\n- **Ponto Final (.)** Termina uma ideia.\n- **Vírgula (,)** Pausa breve. Usada para:\n  1. Listar itens (Ex: Comprei pão, queijo e leite.)\n  2. Chamar alguém (Vocativo) (Ex: Israel, venha cá!)\n  3. Explicar um termo (Aposto) (Ex: Lula, o presidente, viajou.)\n  4. Isolar tempo/lugar (Adj. Adverbial) (Ex: Hoje, vou estudar.)\n- **Dois Pontos (:)** Anuncia uma lista, fala ou explicação.",
        "example": "O maior erro de vírgula é separar o Sujeito do Verbo. (Errado: 'O menino, correu.' Certo: 'O menino correu.')",
        "train_questions": [
            {
                "q": "Por que a vírgula foi usada em: 'Recife, a capital de Pernambuco, é linda.'?",
                "opts": [
                    "Para listar itens.",
                    "Para chamar alguém (Vocativo).",
                    "Para separar o sujeito do verbo.",
                    "Para explicar o termo anterior (Aposto)."
                ],
                "ans": "Para explicar o termo anterior (Aposto).",
                "exp": "'A capital de Pernambuco' é uma explicação sobre o termo 'Recife'. Esse bloco explicativo que fica entre vírgulas é chamado de Aposto."
            }
        ]
    },
    {
        "id": "POR_11",
        "subject": "portugues",
        "title": "Concordância e Regência",
        "lesson_text": "**Concordância:** É a 'combinação' das palavras.\n- *Nominal:* O adjetivo combina com o nome (Ex: As meninas alt**as**).\n- *Verbal:* O verbo combina com o sujeito (Ex: Nós f**omos** / As pessoas f**oram**).\n\n**Regência:** É como os verbos pedem complementos (com ou sem preposição).\n- *Assistir (ver):* Pede 'a' (Ex: Assistir **ao** jogo).\n- *Obedecer:* Pede 'a' (Ex: Obedecer **aos** pais).\n- *Ir:* Pede 'a' (Ex: Vou **ao** shopping, e não 'no' shopping).",
        "example": "Errado: 'Fazem' dois anos. Certo: '**Faz** dois anos.' (Verbo 'fazer' de tempo não vai para o plural).",
        "train_questions": [
            {
                "q": "Qual frase está CORRETA de acordo com a norma padrão?",
                "opts": [
                    "Eu assisti o filme ontem.",
                    "Nós vai à praia amanhã.",
                    "Faziam cinco anos que não o via.",
                    "Eu obedeci ao sinal de trânsito."
                ],
                "ans": "Eu obedeci ao sinal de trânsito.",
                "exp": "O verbo 'obedecer' exige a preposição 'a' (Regência). Os outros estão errados: (Assistir 'ao' filme), (Nós 'vamos'), ('Faz' cinco anos)."
            }
        ]
    },
    {
        "id": "POR_12",
        "subject": "portugues",
        "title": "Crase",
        "lesson_text": "Crase é a fusão de 'a' + 'a'. O 'a' preposição (pedido por um verbo ou nome) + o 'a' artigo (antes de uma palavra feminina).",
        "example": "Quem obedece, obedece 'a' algo. 'A' lei é feminina. Logo: Obedeça 'à' lei. O truque é trocar por uma palavra masculina: Obedeça 'ao' regulamento. Se virar 'ao', tem crase!",
        "train_questions": [
            {
                "q": "Qual frase usa a crase INCORRETAMENTE?",
                "opts": [
                    "Refiro-me à diretora da escola.",
                    "Fui à praia no fim de semana.",
                    "Ele começou à estudar para a prova.",
                    "O prêmio foi dado à vencedora."
                ],
                "ans": "Ele começou à estudar para a prova.",
                "exp": "Nunca se usa crase antes de verbo ('estudar' é um verbo)."
            }
        ]
    }
]

# =====================================================
# 🔹 QUESTÕES DE MATEMÁTICA (12.2)
# =====================================================
questoes_matematica = [
    {
        "id": "MAT_01",
        "subject": "matematica",
        "title": "Problemas com as Quatro Operações",
        "lesson_text": "São a base de tudo: Adição (+), Subtração (-), Multiplicação (*) e Divisão (/). A chave é ler o problema e entender qual operação usar.",
        "example": "João comprou 3 cadernos por R\$ 7,80 cada. Ele pagou com uma nota de R\$ 50,00. Quanto ele recebeu de troco?\n1º (Multiplicação): 3 * 7,80 = R\$ 23,40 (custo total).\n2º (Subtração): 50,00 - 23,40 = R\$ 26,60 (troco).",
        "train_questions": [
            {
                "q": "Maria tem 30 balas. Ela deu 5 para seu irmão e dividiu o restante igualmente entre seus 5 amigos. Quantas balas cada amigo ganhou?",
                "opts": [
                    "5 balas",
                    "6 balas",
                    "4 balas",
                    "30 balas"
                ],
                "ans": "5 balas",
                "exp": "1º (Subtração): 30 - 5 = 25 balas restantes. 2º (Divisão): 25 / 5 = 5 balas por amigo."
            }
        ]
    },
    {
        "id": "MAT_02",
        "subject": "matematica",
        "title": "Operações com Frações",
        "lesson_text": "1. **Soma/Subtração:** Só com denominadores (número de baixo) iguais. Se forem diferentes (ex: 1/2 + 1/3), ache o MMC (Mínimo Múltiplo Comum) (ex: 6).\n2. **Multiplicação:** O mais fácil. Cima * Cima / Baixo * Baixo.\n3. **Divisão:** Repete o primeiro e multiplica pelo inverso do segundo.",
        "example": "1/2 + 1/3 = (MMC é 6) = 3/6 + 2/6 = 5/6.\n(1/2) * (3/4) = 3/8.",
        "train_questions": [
            {
                "q": "Quanto é 2/3 (dois terços) de 60?",
                "opts": [
                    "30",
                    "40",
                    "60",
                    "20"
                ],
                "ans": "40",
                "exp": "A preposição 'de' na matemática significa 'vezes' (*). Então, 2/3 * 60 = (2 * 60) / 3 = 120 / 3 = 40."
            }
        ]
    },
    {
        "id": "MAT_03",
        "subject": "matematica",
        "title": "Operações com Números Decimais",
        "lesson_text": "São os números com vírgula.\n- **Soma/Subtração:** Alinhe as vírgulas (vírgula embaixo de vírgula).\n- **Multiplicação:** Multiplique normal e, no final, conte o total de casas decimais.\n- **Divisão:** Iguale as casas decimais antes de cortar a vírgula e dividir.",
        "example": "Soma: 2,5 + 0,25 = 2,75. Multiplicação: 0,2 * 0,3 = 0,06 (duas casas decimais).",
        "train_questions": [
            {
                "q": "Quanto é 12,00 dividido por 0,5?",
                "opts": [
                    "6,00",
                    "24,00",
                    "12,5",
                    "2,4"
                ],
                "ans": "24,00",
                "exp": "Para dividir, iguale as casas: 12,00 ÷ 0,50. Corte as vírgulas: 1200 ÷ 50. Corte um zero: 120 ÷ 5 = 24."
            }
        ]
    },
    {
        "id": "MAT_04",
        "subject": "matematica",
        "title": "Potenciação",
        "lesson_text": "É uma multiplicação repetida. Regras importantes:\n- $N^0 = 1$ (Todo número elevado a zero é 1).\n- $N^{-1} = 1/N$ (Expoente negativo inverte a base).\n- $A^m * A^n = A^{m+n}$ (Multiplicação de mesma base: soma os expoentes).\n- $A^m / A^n = A^{m-n}$ (Divisão de mesma base: subtrai os expoentes).",
        "example": "$2^3 = 2 * 2 * 2 = 8$. | $5^{-2} = (1/5)^2 = 1/25$.",
        "train_questions": [
            {
                "q": "Qual o valor da expressão $10^2 + 5^0 - 2^{-1}$?",
                "opts": [
                    "100,5",
                    "100",
                    "99,5",
                    "101,5"
                ],
                "ans": "100,5",
                "exp": "$10^2 = 100$. | $5^0 = 1$. | $2^{-1} = 1/2 = 0,5$. | Soma: 100 + 1 - 0,5 = 100,5."
            }
        ]
    },
    {
        "id": "MAT_05",
        "subject": "matematica",
        "title": "Raiz Quadrada Exata",
        "lesson_text": "A Raiz Quadrada ($\sqrt{n}$) é a operação oposta da potência ao quadrado. Ela pergunta: 'Qual número, vezes ele mesmo, dá N?'.",
        "example": "$\sqrt{49} = 7$, pois $7 * 7 = 49$. | $\sqrt{144} = 12$, pois $12 * 12 = 144$.",
        "train_questions": [
            {
                "q": "Qual o valor de $\sqrt{64}$?",
                "opts": [
                    "6",
                    "7",
                    "8",
                    "32"
                ],
                "ans": "8",
                "exp": "O valor é 8, pois 8 * 8 = 64."
            }
        ]
    },
    {
        "id": "MAT_06",
        "subject": "matematica",
        "title": "Expressões com Números Reais (PEMDAS)",
        "lesson_text": "Para resolver expressões, existe uma ordem de prioridade (PEMDAS):\n1. **P**arênteses ( ), Chaves { } ou Colchetes [ ].\n2. **E**xpoentes (Potências e Raízes).\n3. **M**ultiplicação (*) e **D**ivisão (/), na ordem que aparecem.\n4. **A**dição (+) e **S**ubtração (-), na ordem que aparecem.",
        "example": "$5 + 2 * 3 = 5 + 6 = 11$. (Multiplicação primeiro!).\n$(5 + 2) * 3 = 7 * 3 = 21$. (Parênteses primeiro!).",
        "train_questions": [
            {
                "q": "Qual o valor da expressão $10 + 20 / (2 + 3) * 2$?",
                "opts": [
                    "18",
                    "12",
                    "6",
                    "30"
                ],
                "ans": "18",
                "exp": "1º Parênteses: (2+3) = 5. A expressão vira $10 + 20 / 5 * 2$. \n2º Divisão: 20 / 5 = 4. A expressão vira $10 + 4 * 2$. \n3º Multiplicação: 4 * 2 = 8. \n4º Adição: 10 + 8 = 18."
            }
        ]
    },
    {
        "id": "MAT_07",
        "subject": "matematica",
        "title": "Sistemas de Medidas",
        "lesson_text": "Unidades mais comuns:\n- **Comprimento:** km, metro (m), cm, mm. (1 km = 1000 m; 1 m = 100 cm).\n- **Capacidade:** Litro (L), ml. (1 L = 1000 ml).\n- **Massa:** kg, grama (g). (1 kg = 1000 g).\n- **Área ($m^2$):** 1 $m^2$ = 10.000 $cm^2$ (pois é 100 * 100).\n- **Volume ($m^3$):** 1 $m^3$ = 1.000 Litros.",
        "example": "Para converter 2,5 km para metros, multiplica-se por 1000: 2,5 * 1000 = 2500 m.",
        "train_questions": [
            {
                "q": "Uma caixa d'água de 2 $m^3$ (metros cúbicos) tem capacidade para quantos litros?",
                "opts": [
                    "200 litros",
                    "20 litros",
                    "2000 litros",
                    "2 litros"
                ],
                "ans": "2000 litros",
                "exp": "O fator de conversão é 1 $m^3$ = 1000 Litros. Portanto, 2 $m^3$ = 2000 Litros."
            }
        ]
    },
    {
        "id": "MAT_08",
        "subject": "matematica",
        "title": "Razão e Proporção",
        "lesson_text": "Uma **Razão** é uma divisão (fração) entre duas grandezas. (Ex: Razão de 2 para 4 é 2/4).\nUma **Proporção** é uma igualdade entre duas razões. (Ex: 1/2 = 3/6).\nO truque da proporção é a **multiplicação em cruz**.",
        "example": "Se 2/5 = X/10. Multiplicando em cruz: 5 * X = 2 * 10 -> 5X = 20 -> X = 4.",
        "train_questions": [
            {
                "q": "A escala de um mapa é 1:100.000. Se a distância entre duas cidades no mapa é 5 cm, qual a distância real?",
                "opts": [
                    "500.000 cm (ou 5 km)",
                    "100.000 cm (ou 1 km)",
                    "50.000 cm (ou 0,5 km)",
                    "5.000 cm (ou 50 m)"
                ],
                "ans": "500.000 cm (ou 5 km)",
                "exp": "Montamos a proporção: (Mapa / Real) = 1 / 100.000 = 5 / X. Multiplicando em cruz: X = 5 * 100.000 = 500.000 cm. (Para converter cm para km, corta-se 5 zeros)."
            }
        ]
    },
    {
        "id": "MAT_09",
        "subject": "matematica",
        "title": "Divisão Proporcional",
        "lesson_text": "É dividir um total em partes 'justas' (proporcionais) a certos números. O truque é usar o 'k' (constante de proporção).",
        "example": "Dividir R\$ 100 em partes **diretamente proporcionais** a 2 e 3.\n1. A = 2k; B = 3k\n2. Soma: 2k + 3k = 100 -> 5k = 100 -> k = 20.\n3. A = 2*20 = R\$ 40; B = 3*20 = R\$ 60.",
        "train_questions": [
            {
                "q": "Divida o número 60 em partes diretamente proporcionais a 1 e 5. Quais são as partes?",
                "opts": [
                    "10 e 50",
                    "30 e 30",
                    "1 e 5",
                    "12 e 48"
                ],
                "ans": "10 e 50",
                "exp": "A = 1k; B = 5k. Soma: 1k + 5k = 60 -> 6k = 60 -> k = 10. As partes são: A = 1*10 = 10; B = 5*10 = 50."
            }
        ]
    },
    {
        "id": "MAT_10",
        "subject": "matematica",
        "title": "Regra de Três Simples e Composta",
        "lesson_text": "Usada para resolver proporções. \n**Simples (2 grandezas):** Monte a tabela e multiplique em cruz (se direta) ou em linha (se inversa).\n**Composta (3+ grandezas):** Fixe a coluna do X. Compare cada coluna com a do X para ver se é Direta ou Inversa. Inverta as colunas Inversas na equação.",
        "example": "Se 2 pedreiros fazem 1 muro em 4 dias (Simples). 4 pedreiros farão em X dias. (Mais pedreiros, MENOS dias = INVERSA). Multiplica em linha: 4 * X = 2 * 4 -> 4X = 8 -> X = 2 dias.",
        "train_questions": [
            {
                "q": "Se 5 impressoras imprimem 1000 folhas em 2 horas, 10 impressoras imprimem 1000 folhas em quanto tempo?",
                "opts": [
                    "1 hora",
                    "2 horas",
                    "4 horas",
                    "30 minutos"
                ],
                "ans": "1 hora",
                "exp": "Mais impressoras (dobro), para o mesmo trabalho, levam MENOS tempo (metade). É inversa. O dobro de impressoras leva metade do tempo. Metade de 2 horas = 1 hora."
            }
        ]
    },
    {
        "id": "MAT_11",
        "subject": "matematica",
        "title": "Porcentagem",
        "lesson_text": "Porcentagem é uma fração com denominador 100. '25%' significa 25/100 ou 0,25. Para achar 'X% de Y', multiplique (X/100) * Y.",
        "example": "Para calcular 20% de 500: (20/100) * 500 = 0,20 * 500 = 100.",
        "train_questions": [
            {
                "q": "Um produto custava R\$ 80,00 e teve um desconto de 15%. Qual o novo preço?",
                "opts": [
                    "R\$ 68,00",
                    "R\$ 70,00",
                    "R\$ 12,00",
                    "R\$ 92,00"
                ],
                "ans": "R\$ 68,00",
                "exp": "Desconto = 15% de 80 = 0,15 * 80 = R\$ 12,00. Novo preço = 80 - 12 = R\$ 68,00."
            }
        ]
    },
    {
        "id": "MAT_12",
        "subject": "matematica",
        "title": "Médias",
        "lesson_text": "1. **Média Aritmética (Simples):** Some todos os valores e divida pela quantidade de valores.\n2. **Média Ponderada (com Pesos):** Multiplique cada valor pelo seu peso, some os resultados, e divida pela soma total dos pesos.",
        "example": "Média Simples das notas 5, 6 e 7: (5 + 6 + 7) / 3 = 18 / 3 = 6.\nMédia Ponderada: Nota 10 (peso 1) e Nota 8 (peso 2). (10*1 + 8*2) / (1+2) = (10 + 16) / 3 = 26 / 3 = 8,66.",
        "train_questions": [
            {
                "q": "Qual a média aritmética simples dos números 10, 20 e 45?",
                "opts": [
                    "25",
                    "75",
                    "30",
                    "22,5"
                ],
                "ans": "25",
                "exp": "Soma: 10 + 20 + 45 = 75. Quantidade: 3 números. Média: 75 / 3 = 25."
            }
        ]
    },
    {
        "id": "MAT_13",
        "subject": "matematica",
        "title": "Polinômios (Valor Numérico e Operações)",
        "lesson_text": "Polinômios são expressões com letras (ex: $3x^2 + 2x - 5$).\n- **Valor Numérico:** Substitua o 'x' pelo número dado. (Ex: $P(x) = 2x+1$. $P(3) = 2*3 + 1 = 7$).\n- **Operações (Soma/Subtração):** Só se pode somar termos semelhantes (ex: $x^2$ com $x^2$; $x$ com $x$).",
        "example": "$(5x + 3) + (2x - 1) = (5x+2x) + (3-1) = 7x + 2$.",
        "train_questions": [
            {
                "q": "Qual o valor do polinômio $P(x) = x^2 + 5x - 10$ para $x = 2$?",
                "opts": [
                    "4",
                    "10",
                    "14",
                    "-6"
                ],
                "ans": "4",
                "exp": "Substitua o x por 2: $P(2) = (2)^2 + 5*(2) - 10 = 4 + 10 - 10 = 4$."
            }
        ]
    },
    {
        "id": "MAT_14",
        "subject": "matematica",
        "title": "Produtos Notáveis",
        "lesson_text": "São 3 fórmulas para decorar:\n1. **Quadrado da Soma:** $(a + b)^2 = a^2 + 2ab + b^2$\n2. **Quadrado da Diferença:** $(a - b)^2 = a^2 - 2ab + b^2$\n3. **Produto da Soma pela Diferença:** $(a + b)(a - b) = a^2 - b^2$",
        "example": "$(x + 3)^2 = x^2 + 2*x*3 + 3^2 = x^2 + 6x + 9$. (NÃO é $x^2 + 9$!)",
        "train_questions": [
            {
                "q": "Qual o resultado de $(x - 5)(x + 5)$?",
                "opts": [
                    "$x^2 - 10x + 25$",
                    "$x^2 + 10x + 25$",
                    "$x^2 - 25$",
                    "$x^2 + 25$"
                ],
                "ans": "$x^2 - 25$",
                "exp": "Este é o 'Produto da Soma pela Diferença' $(a-b)(a+b) = a^2 - b^2$. Onde a=x e b=5. O resultado é $x^2 - 5^2 = x^2 - 25$."
            }
        ]
    },
    {
        "id": "MAT_15",
        "subject": "matematica",
        "title": "Fatoração",
        "lesson_text": "Fatorar é o inverso de Produtos Notáveis. É transformar uma soma em multiplicação.\n- **Fator Comum:** O que se repete em todos os termos? (Ex: $ax + ay = a(x+y)$).\n- **Diferença de Quadrados:** O inverso do Produto Notável 3. (Ex: $a^2 - b^2 = (a+b)(a-b)$).",
        "example": "Fatorar $x^2 - 49$. Isso é $x^2 - 7^2$. A forma fatorada é $(x + 7)(x - 7)$.",
        "train_questions": [
            {
                "q": "Qual a forma fatorada da expressão $5x + 10y$?",
                "opts": [
                    "$5(x + 10y)$",
                    "$5(x + 2y)$",
                    "$10(x + y)$",
                    "$5(x + y) + 5y$"
                ],
                "ans": "$5(x + 2y)$",
                "exp": "O 'Fator Comum' é o 5 (pois 10 é 5*2). Colocando o 5 em evidência (para fora): $5 * (x + 2y)$."
            }
        ]
    },
    {
        "id": "MAT_16",
        "subject": "matematica",
        "title": "Radiciação (Simplificação de Raízes)",
        "lesson_text": "Radiciação ($\sqrt{n}$) é achar a raiz. Às vezes a raiz não é exata, mas podemos simplificar 'fatorando' o número.",
        "example": "$\sqrt{20}$. Fatorando o 20 temos $2 * 2 * 5$, ou $2^2 * 5$. Então $\sqrt{20} = \sqrt{2^2 * 5}$. Quem tem o expoente 2 ('$2^2$') 'sai' da raiz. O 5 fica.\nResultado: $2\sqrt{5}$.",
        "train_questions": [
            {
                "q": "Qual a forma simplificada de $\sqrt{18}$?",
                "opts": [
                    "$9\sqrt{2}$",
                    "$2\sqrt{9}$",
                    "$3\sqrt{2}$",
                    "Não dá para simplificar"
                ],
                "ans": "$3\sqrt{2}$",
                "exp": "Fatorando o 18, temos $2 * 9$, que é $2 * 3^2$. $\sqrt{18} = \sqrt{3^2 * 2}$. O 3 'sai' da raiz e o 2 'fica'. Resultado: $3\sqrt{2}$."
            }
        ]
    },
    {
        "id": "MAT_17",
        "subject": "matematica",
        "title": "Equações Algébricas do 1º Grau",
        "lesson_text": "O objetivo é achar o valor de 'x'. A regra é: 'letra de um lado, número do outro'. Quem pula o sinal de '=' (igual), inverte a operação ( + vira - | * vira / ).",
        "example": "$3x - 5 = 10$. \nPasso 1 (número): $3x = 10 + 5$ -> $3x = 15$. \nPasso 2 (letra): $x = 15 / 3$ -> $x = 5$.",
        "train_questions": [
            {
                "q": "Qual o valor de X na equação $5x + 2 = 3x + 10$?",
                "opts": [
                    "x = 4",
                    "x = 2",
                    "x = 8",
                    "x = 6"
                ],
                "ans": "x = 4",
                "exp": "1. Letras para a esquerda: $5x - 3x = 10 - 2$. \n2. Simplifica: $2x = 8$. \n3. Isola o x: $x = 8 / 2$. \n4. Resposta: $x = 4$."
            }
        ]
    },
    {
        "id": "MAT_18",
        "subject": "matematica",
        "title": "Sistemas Lineares do 1º Grau",
        "lesson_text": "São duas equações com 'x' e 'y' para descobrir. O 'Método da Adição' é o mais rápido: some as duas equações para 'cortar' uma das letras.",
        "example": "Equações: \n(1) $x + y = 10$ \n(2) $x - y = 4$ \nSomando (1) + (2): \n$(x+x) + (y-y) = (10+4)$ \n$2x = 14$ -> $x = 7$. \nSubstituindo na (1): $7 + y = 10$ -> $y = 3$.",
        "train_questions": [
            {
                "q": "Se $x + y = 20$ e $x - y = 10$, quais os valores de x e y?",
                "opts": [
                    "x = 10, y = 10",
                    "x = 15, y = 5",
                    "x = 20, y = 0",
                    "x = 5, y = 15"
                ],
                "ans": "x = 15, y = 5",
                "exp": "Usando o Método da Adição: (x+y) + (x-y) = 20 + 10 -> 2x = 30 -> x = 15. \nSe x = 15, e x+y=20, então 15+y=20 -> y=5."
            }
        ]
    },
    {
        "id": "MAT_19",
        "subject": "matematica",
        "title": "Ângulos",
        "lesson_text": "- **Agudo:** Menor que 90°.\n- **Reto:** Exatamente 90° (o 'L' de um canto).\n- **Obtuso:** Maior que 90°.\n- **Raso:** Exatamente 180° (uma linha reta).\n- **Complementares:** Dois ângulos que somam 90°.\n- **Suplementares:** Dois ângulos que somam 180°.",
        "example": "O ângulo complementar de 60° é 30° (pois 60+30=90). O ângulo suplementar de 60° é 120° (pois 60+120=180).",
        "train_questions": [
            {
                "q": "Qual é o ângulo SUPLEMENTAR de 70°?",
                "opts": [
                    "20° (complementar)",
                    "110° (suplementar)",
                    "90° (reto)",
                    "70° (oposto)"
                ],
                "ans": "110° (suplementar)",
                "exp": "Ângulos suplementares são aqueles que, somados, dão 180°. A conta é 180 - 70 = 110°."
            }
        ]
    },
    {
        "id": "MAT_20",
        "subject": "matematica",
        "title": "Polígonos (Soma dos Ângulos)",
        "lesson_text": "Polígonos são figuras fechadas (Triângulo, Quadrado, Pentágono, etc.).\n- **Soma dos Ângulos Internos (Si):** É a fórmula mais importante. $Si = (n - 2) * 180$, onde 'n' é o número de lados.\n- **Diagonais (d):** $d = n(n-3) / 2$.",
        "example": "Qual a soma dos ângulos internos de um Pentágono (n=5)?\n$Si = (5 - 2) * 180 = 3 * 180 = 540°$.",
        "train_questions": [
            {
                "q": "Qual é a soma dos ângulos internos de um Hexágono (6 lados)?",
                "opts": [
                    "180°",
                    "360°",
                    "540°",
                    "720°"
                ],
                "ans": "720°",
                "exp": "Usando a fórmula $Si = (n - 2) * 180$. Para n=6: $Si = (6 - 2) * 180 = 4 * 180 = 720°$."
            }
        ]
    },
    {
        "id": "MAT_21",
        "subject": "matematica",
        "title": "Triângulos (Classificação e Lei Angular)",
        "lesson_text": "**Lei Angular de Tales:** A soma dos 3 ângulos internos de QUALQUER triângulo é sempre **180°**.\n**Classificação (Lados):**\n- *Equilátero:* 3 lados iguais.\n- *Isósceles:* 2 lados iguais.\n- *Escaleno:* 3 lados diferentes.\n**Classificação (Ângulos):**\n- *Acutângulo:* 3 ângulos agudos (< 90°).\n- *Retângulo:* 1 ângulo reto (= 90°).\n- *Obtusângulo:* 1 ângulo obtuso (> 90°).",
        "example": "Se um triângulo tem ângulos de 50° e 70°, o terceiro ângulo TEM que ser 60° (pois 50+70+60 = 180).",
        "train_questions": [
            {
                "q": "Um triângulo retângulo tem um ângulo de 40°. Qual o valor do outro ângulo agudo?",
                "opts": [
                    "50°",
                    "40°",
                    "90°",
                    "140°"
                ],
                "ans": "50°",
                "exp": "Triângulo retângulo já tem um ângulo de 90°. A soma total é 180°. Então, 180 - 90 (o reto) - 40 (o dado) = 50°."
            }
        ]
    },
    {
        "id": "MAT_22",
        "subject": "matematica",
        "title": "Semelhança de Triângulos (Teorema de Tales)",
        "lesson_text": "Dois triângulos são 'semelhantes' se são 'cópias' um do outro, mas de tamanhos diferentes. Seus ângulos são iguais e seus lados são proporcionais.\n**Teorema de Tales:** Se retas paralelas são cortadas por transversais, os segmentos são proporcionais.",
        "example": "Um prédio de 30m de altura faz uma sombra de 10m. No mesmo instante, um poste de 6m faz uma sombra 'x'.\nProporção (Altura/Sombra): 30/10 = 6/x -> 3 = 6/x -> 3x = 6 -> x = 2 metros.",
        "train_questions": [
            {
                "q": "Um triângulo pequeno tem base 5 e altura 4. Um triângulo maior semelhante tem base 10. Qual a altura do maior?",
                "opts": [
                    "4",
                    "5",
                    "8",
                    "10"
                ],
                "ans": "8",
                "exp": "A base dobrou (de 5 para 10). Logo, a altura também deve dobrar (de 4 para 8). Proporção: 5/10 = 4/x -> 5x = 40 -> x=8."
            }
        ]
    },
    {
        "id": "MAT_23",
        "subject": "matematica",
        "title": "Cevianas (Mediana, Bissetriz, Altura)",
        "lesson_text": "Cevianas são retas que saem de um vértice (ponta) do triângulo e cortam o lado oposto.\n- **Mediana:** Liga o vértice ao **ponto médio** do lado oposto (divide o lado em 2 partes iguais).\n- **Bissetriz:** Liga o vértice ao lado oposto **dividindo o ângulo** em 2 partes iguais.\n- **Altura:** Liga o vértice ao lado oposto formando um **ângulo de 90°** (reto).",
        "example": "Em um triângulo isósceles (com 2 lados iguais), a altura, a mediana e a bissetriz relativas à base (o lado diferente) são a mesma reta.",
        "train_questions": [
            {
                "q": "A reta que sai de um vértice e divide o ângulo desse vértice em dois ângulos iguais chama-se:",
                "opts": [
                    "Mediana",
                    "Bissetriz",
                    "Altura",
                    "Hipotenusa"
                ],
                "ans": "Bissetriz",
                "exp": "Bissetriz = 'Bi' (dois) + 'setriz' (corte). Ela corta o ângulo em dois."
            }
        ]
    },
    {
        "id": "MAT_24",
        "subject": "matematica",
        "title": "Raiz Quadrada (Aproximação Decimal)",
        "lesson_text": "O que fazer quando a raiz não é exata (ex: $\sqrt{10}$)? Você precisa 'cercar' ela. Pense: Qual a raiz exata *antes* e *depois* dela?\n- $\sqrt{9} = 3$\n- $\sqrt{10} = ?$\n- $\sqrt{16} = 4$\nIsso significa que a $\sqrt{10}$ está em algum lugar entre o 3 e o 4. Como 10 está mais perto do 9, a resposta será '3,alguma coisinha' (ex: 3,1 ou 3,2).",
        "example": "Para achar $\sqrt{80}$: Está entre $\sqrt{64} = 8$ e $\sqrt{81} = 9$. Como 80 está 'colado' no 81, a resposta será um número muito próximo de 9 (ex: 8,9).",
        "train_questions": [
            {
                "q": "O número $\sqrt{30}$ está localizado na reta numérica entre quais dois números inteiros?",
                "opts": [
                    "4 e 5",
                    "5 e 6",
                    "6 e 7",
                    "29 e 31"
                ],
                "ans": "5 e 6",
                "exp": "Para 'cercar' o $\sqrt{30}$, procuramos os quadrados perfeitos mais próximos. $\sqrt{25} = 5$ e $\sqrt{36} = 6$. Como 30 está entre 25 e 36, a raiz de 30 tem que estar entre 5 e 6."
            }
        ]
    },
    {
        "id": "MAT_25",
        "subject": "matematica",
        "title": "Outras Médias (Geométrica e Harmônica)",
        "lesson_text": "Além da Média Aritmética (somar e dividir) e Ponderada (dos pesos), o edital  cita outras duas. Elas são raras, mas é bom saber:\n1. **Média Geométrica (MG):** Usada para taxas de crescimento. Você multiplica os 'n' números e tira a raiz 'n' (Ex: se forem 2 números, tire a raiz quadrada; se forem 3, a raiz cúbica).\n2. **Média Harmônica (MH):** Usada para velocidades médias. É a 'inversa da média dos inversos'. Para 2 números 'a' e 'b', a fórmula é $MH = 2 / (1/a + 1/b)$.",
        "example": "Média Geométrica entre 4 e 9: $MG = \sqrt{4 \times 9} = \sqrt{36} = 6$.\nMédia Harmônica entre 2 e 3: $MH = 2 / (1/2 + 1/3) = 2 / (5/6) = 12/5 = 2,4$.",
        "train_questions": [
            {
                "q": "Um carro sobe uma ladeira a 20 km/h e desce a mesma ladeira a 30 km/h. Qual a sua velocidade média (Média Harmônica)?",
                "opts": [
                    "25 km/h (Média Aritmética)",
                    "24 km/h (Média Harmônica)",
                    "22 km/h",
                    "50 km/h"
                ],
                "ans": "24 km/h (Média Harmônica)",
                "exp": "Velocidade média usa Média Harmônica. $MH = 2 / (1/20 + 1/30) = 2 / (3/60 + 2/60) = 2 / (5/60) = 2 \times (60/5) = 120/5 = 24$ km/h."
            }
        ]
    }
]