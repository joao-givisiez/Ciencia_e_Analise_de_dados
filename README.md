# 🩺 Análise de Mortalidade por Doenças Isquêmicas do Coração no Brasil

**Projeto Integrado de Ciência de Dados e Governança - Zettalab 2025**

Este projeto realiza uma análise completa sobre a relação entre fatores socioeconômicos e a taxa de mortalidade por doenças isquêmicas do coração nos estados brasileiros, dividido em **duas fases complementares**: análise exploratória descritiva (Fase 1) e modelagem preditiva com inteligência artificial (Fase 2).

---

## 🎯 Objetivos Gerais

✅ **Fase 1 - Análise Exploratória:**
- Integrar dados públicos de múltiplas fontes (mortalidade, população, PIB, saúde, educação)
- Identificar padrões e correlações entre indicadores
- Gerar visualizações para comunicação clara dos insights

✅ **Fase 2 - Modelagem Preditiva:**
- Prever taxa de mortalidade usando variáveis socioeconômicas
- Identificar quais fatores mais impactam a mortalidade
- Criar um dashboard interativo para simulação de cenários

---

## 🗂️ Estrutura do Projeto

```
Analise-de-dados-sobre-mortes-por-doen-as-isqu-micas-do-cora-o-no-brasil/
│
├── dados/                                      # 📁 Raiz do processamento
│   ├── dados_sem_tratamento/                  # 📥 Dados brutos originais (9 arquivos)
│   │   ├── mortes_2016 - Página1.csv
│   │   ├── mortes_2017 - Página1.csv
│   │   ├── mortes_2018 - Página1.csv
│   │   ├── populaçao br - Página1.csv
│   │   ├── pib em % - Página1 (2).csv
│   │   ├── tabagismo - Página1.csv
│   │   ├── IDHM - Página1.csv
│   │   ├── gini geral - Página1.csv
│   │   └── leitos sus.csv
│   │
│   ├── saidas_1_parte/                        # 📊 Output Fase 1: Dados integrados
│   │   └── ...dataset_final_tratado.csv          # Dataset unificado (81 linhas × 25+ colunas)
│   │
│   ├── saidas_2_parte/                        # 📈 Output Fase 2: SHAP visualizations
│   │   ├── shap_summary_taxa_mortes_isquemicas_total_por_100k.png
│   │   └── shap_summary_taxa_mortes_isquemicas_adultos_idosos_por_100k.png
│   │
│   ├── modelos/                               # 🤖 Modelos treinados (serialização .pkl)
│   │   ├── modelo_taxa_mortes_isquemicas_total_por_100k.pkl
│   │   └── modelo_taxa_mortes_isquemicas_adultos_idosos_por_100k.pkl
│   │
│   ├── Analise_de_Dados.ipynb                 # 📓 Notebook Fase 1: Análise Exploratória
│   ├── Analise_preditiva.ipynb                # 📓 Notebook Fase 2: Modelagem IA & SHAP
│   └── app.py                                 # 🚀 Dashboard Streamlit interativo
│
├── .gitignore                                 # 🔒 Arquivos ignorados no Git 
├── README.md                                  

```

**Notas sobre a estrutura:**
- ✅ `dados_sem_tratamento/` contém **9 arquivos CSV brutos** de diferentes fontes públicas
- ✅ `saidas_1_parte/` é a saída da **Fase 1** (dataset integrado)
- ✅ `saidas_2_parte/` é a saída da **Fase 2** (visualizações SHAP)
- ✅ `modelos/` armazena os **modelos treinados** para o dashboard reutilizar

---

## 📖 Dicionário de Dados Completo

### Variáveis de Identificação

| Variável | Tipo | Descrição | Fonte |
|----------|------|-----------|-------|
| **Estado** | Categórica | Nome do estado brasileiro | IBGE |
| **Ano** | Numérica (Inteira) | Ano de referência (2016-2018) | Diversas |
| **Região** | Categórica | Região geográfica (Norte, Nordeste, Centro-Oeste, Sudeste, Sul) | Engenharia de Features |
| **Região_Cod** | Numérica (1-5) | Código numérico da região para o modelo | Feature Engineered |
| **População** | Numérica (Inteira) | População total do estado | IBGE |

### Variáveis Alvo (Targets)

| Variável | Tipo | Descrição | Unidade | Fonte |
|----------|------|-----------|--------|-------|
| **Taxa_Mortes_Isquemicas_Total_por_100k** | Numérica (Contínua) | Taxa total de mortalidade por doenças isquêmicas | Mortes/100k hab. | DATASUS |
| **Taxa_Mortes_Isquemicas_Adultos_Idosos_por_100k** | Numérica (Contínua) | Taxa de mortalidade para adultos (≥30 anos) e idosos | Mortes/100k hab. | DATASUS |
| **Taxa_Mortes_Isquemicas_Infantil_por_100k** | Numérica (Contínua) | Taxa de mortalidade para crianças (<5 anos) | Mortes/100k hab. | DATASUS |

### Variáveis Preditoras (Features)

| Variável | Tipo | Intervalo | Descrição | Papel no Modelo |
|----------|------|-----------|-----------|-----------------|
| **IDHM** | Numérica (0-1) | 0.5 - 0.9 | Índice de Desenvolvimento Humano Municipal | Feature (Proteção) |
| **Gini** | Numérica (0-1) | 0.3 - 0.7 | Coeficiente de Gini (desigualdade de renda) | Feature (Risco) |
| **Leitos_SUS\|10k** | Numérica | 0 - 50 | Leitos hospitalares por 10.000 habitantes | Feature (Proteção) |
| **%_Fumantes** | Numérica (%) | 5 - 25 | Prevalência de tabagismo na população | Feature (Risco) |
| **PIB_%** | Numérica (%) | -5 - 5 | Variação do PIB estadual | Feature (Complexo) |

### Variáveis de Faixa Etária (Dados Brutos - Fase 1)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| **Menor 1 ano** | Numérica (Inteira) | Contagem absoluta de óbitos |
| **1 a 4 anos** | Numérica (Inteira) | Contagem absoluta de óbitos |
| **5 a 9 anos** até **80 anos e mais** | Numérica (Inteira) | Contagem absoluta por faixa etária |
| **Total** | Numérica (Inteira) | Total de óbitos no período |

---

## 🚀 Fase 1: Análise Exploratória e Integração de Dados

### Objetivo
Transformar dados brutos de múltiplas fontes em um dataset unificado e explorar padrões socioeconômicos.

### O que foi feito
1. **Coleta e Limpeza:** Importação de 9 arquivos CSV de diferentes fontes
2. **Engenharia de Features Inicial:** Criação de colunas derivadas (taxas por 100k hab., agregações por região)
3. **Validação:** Verificação de consistência, tratamento de valores faltantes
4. **Visualização Exploratória:** Gráficos de dispersão, heatmaps de correlação, séries temporais
5. **Saída:** Dataset unificado (`dataset_final_tratado.csv`) com 81 linhas (27 estados × 3 anos)

### Resultado
Dataset consolidado pronto para modelagem, com 100% de cobertura temporal e sem valores faltantes críticos.

---

## 🤖 Fase 2: Modelagem Preditiva e Inteligência Artificial

### 🧠 Minha Estratégia de Modelagem (Passo a Passo)

#### 1️⃣ Refinamento e Engenharia de Features
Ao iniciar a modelagem, percebi que tratar o Brasil como um bloco único limitava a precisão das previsões. A realidade sanitária do Norte é muito diferente do Sul.

**O "Pulo do Gato":** Criei uma nova variável chamada `Regiao_Cod`, ensinando ao modelo o contexto geográfico de cada estado (Norte=1, Nordeste=2, Centro-Oeste=3, Sudeste=4, Sul=5).

**Limpeza:** Garanti que todos os dados numéricos (originalmente com vírgulas no padrão PT-BR) fossem convertidos corretamente para floats processáveis.

#### 2️⃣ A Batalha dos Modelos
Seguindo as boas práticas de Ciência de Dados, não escolhi um algoritmo cegamente. Realizei um torneio comparativo entre:

- **Regressão Linear (Baseline):** Para testar se uma abordagem simples resolveria
- **Random Forest Regressor (Vencedor):** Escolhi este modelo pela sua capacidade de lidar com relações não-lineares complexas e alta robustez a outliers

#### 3️⃣ Otimização e Ajuste Fino (GridSearchCV)
Não usei os parâmetros "de fábrica". Implementei uma validação cruzada (cv=5) testando diversas combinações:
- **n_estimators:** [100, 200] árvores de decisão
- **max_depth:** [3, 4, 5] níveis de profundidade
- **min_samples_split:** [2, 4] amostras mínimas para dividir

**Descoberta:** Notei que modelos muito profundos decoravam os dados (overfitting). Restringi a profundidade (max_depth≤5), o que garantiu um modelo mais generalista e honesto.

### 📊 Resultados Obtidos

Ao separar o alvo da previsão, cheguei a uma conclusão estratégica importante sobre a qualidade dos dados:

| Modelo | R² Score | Interpretação |
|--------|----------|----------------|
| **Adultos e Idosos (≥30 anos)** | **74.19%** | ✅ Excelente - Variáveis explicam bem a mortalidade |
| **População Total** | ~62% | ✅ Bom - Dados infantis adicionam ruído |

**Decisão Estratégica:** Optei por focar o Dashboard final no modelo de Adultos/Idosos, pois é onde:
- A intervenção de política pública é mais eficaz
- Os dados são mais confiáveis
- As variáveis socioeconômicas têm maior impacto

### 🔍 Explicabilidade (XAI - Explainable AI)

Para garantir a governança dos dados e não criar uma "caixa preta", utilizei a biblioteca **SHAP** (SHapley Additive exPlanations). Isso permitiu ver não só o **que** o modelo previu, mas **por que** ele previu, identificando claramente:

- Como a desigualdade regional (Gini) atua como fator de risco
- Como o IDH atua como fator de proteção
- O impacto relativo de cada variável

**Arquivos Gerados:**
- `shap_summary_taxa_mortes_isquemicas_adultos_idosos_por_100k.png` - Gráfico principal de impacto

### 🛠️ Entrega Técnica (MLOps)

Finalizei o processo salvando os modelos treinados em formato `.pkl` (serialização) para garantir que:
- ✅ O Dashboard interativo roda instantaneamente
- ✅ Sem necessidade de re-treinamento a cada acesso
- ✅ Modelos são versionados e reproducíveis (random_state=42)

---

## ⚙️ Como Executar o Projeto

### Pré-requisitos
- Python ≥ 3.8
- pip ou conda
- (Opcional) Git para versionamento

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/Analise-de-dados-sobre-mortes-por-doen-as-isqu-micas-do-cora-o-no-brasil.git
cd Analise-de-dados-sobre-mortes-por-doen-as-isqu-micas-do-cora-o-no-brasil
```

### 2. Criar e ativar ambiente virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar Fase 1 (Análise Exploratória)

```bash
jupyter notebook dados/Analise_de_Dados.ipynb
```

**Resultado esperado:** Arquivo `dados/saidas/dataset_final_tratado.csv` gerado


### 5. Executar Fase 2 (Modelagem Preditiva)

```bash
jupyter notebook dados/Analise_preditiva.ipynb
```

**Resultado esperado:** 
- Modelos salvos em `dados/modelos/`
- Gráficos SHAP em `dados/saidas_2_parte/`

### 6. Executar Dashboard Interativo

```bash
cd dados
streamlit run app.py
```

Acesse `http://localhost:8501` no navegador

---

## 📊 Visualizações Disponíveis

### Fase 1 (pasta:saidas_1_fase)
- **Heatmap de Correlação:** Relação entre todas as variáveis
- **Scatter Plots:** IDHM vs Mortalidade, Tabagismo vs Mortalidade, etc.
- **Séries Temporais:** Evolução da mortalidade por estado (2016-2018)
- **Distribuições Regionais:** Box plots e violin plots por região

### Fase 2 - Dashboard Streamlit
- **Panorama:** Métricas principais (mortalidade média, IDHM, tabagismo) com filtros por ano e região
- **Simulador (IA):** Ferramenta interativa para prever mortalidade com diferentes cenários de política pública
- **Explicabilidade:** Gráfico SHAP mostrando importância relativa de cada fator

---

## 📥 Fontes de Dados

| Fonte | Link | Variáveis |
|-------|------|-----------|
| **DATASUS** | http://tabnet.datasus.gov.br/ | Taxa de mortalidade por doenças isquêmicas |
| **IBGE** | https://www.ibge.gov.br/ | População, PIB, IDHM |
| **PNUD Brasil** | http://www.br.undp.org/ | Índice de Desenvolvimento Humano Municipal (IDHM) |
| **IPEA** | https://www.ipea.gov.br/ | Coeficiente de Gini |
| **CNES** | http://cnes.datasus.gov.br/ | Leitos hospitalares SUS |
| **VIGITEL** | https://www.gov.br/saude/ | Taxa de tabagismo (VIGITEL - Vigilância de Fatores de Risco) |

---

## 🔐 Governança e Boas Práticas

✅ **Reprodutibilidade:** Todo código usa `random_state=42`  
✅ **Versionamento:** Arquivos .gitignore configurado para não versionar dependências  
✅ **Documentação:** Comentários TODO em cada célula explicando o passo a passo  
✅ **Explicabilidade:** SHAP values para interpretar predições  
✅ **Validação:** Validação cruzada (5-fold) em todos os modelos  

---

## 📌 Observações Importantes

- Os dados de mortalidade abrangem **2016 a 2018** (tendências de 3 anos)
- Análise foca em **estados brasileiros** (27 unidades federativas)
- O projeto é **reproduzível** em qualquer SO com Python instalado
- Modelos são **agnósticos a outliers** (Random Forest é robusto)
- Dashboard funciona **offline** (sem dependência de APIs externas)


---

## 🤝 Contato & Contribuição

**Desenvolvido por:** João Vitor Givisiez Lessa

🔗 [LinkedIn](https://linkedin.com/in/joão-vitor-givisiez-lessa)  
📧 [Email](mailto:joaovitorgivisiez@gmail.com)

---

## 📄 Licença

Este projeto está sob licença [MIT](LICENSE) e pode ser usado livremente para fins educacionais e de pesquisa.

---
