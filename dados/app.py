import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from PIL import Image
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Zetta Lab - Governança de Dados",
    page_icon="💙",
    layout="wide"
)

# --- FUNÇÕES DE SUPORTE (REGIONALIZAÇÃO) ---
def definir_regiao(estado):
    mapa = {
        'Norte': ['Amazonas', 'Roraima', 'Amapá', 'Pará', 'Tocantins', 'Rondônia', 'Acre'],
        'Nordeste': ['Maranhão', 'Piauí', 'Ceará', 'Rio Grande do Norte', 'Paraíba', 'Pernambuco', 'Alagoas', 'Sergipe', 'Bahia'],
        'Centro-Oeste': ['Mato Grosso', 'Mato Grosso do Sul', 'Goiás', 'Distrito Federal'],
        'Sudeste': ['São Paulo', 'Rio de Janeiro', 'Espírito Santo', 'Minas Gerais'],
        'Sul': ['Paraná', 'Rio Grande do Sul', 'Santa Catarina']
    }
    for regiao, estados in mapa.items():
        if estado in estados:
            return regiao
    return 'Outra'

def codigo_regiao(nome_regiao):
    mapa_cod = {'Norte': 1, 'Nordeste': 2, 'Centro-Oeste': 3, 'Sudeste': 4, 'Sul': 5}
    return mapa_cod.get(nome_regiao, 0)

# --- CARREGAMENTO DE DADOS (COM CAMINHO CORRIGIDO) ---
@st.cache_data
def carregar_dados():
    # 1. Caminho principal solicitado por você
    caminho_csv = os.path.join('dados', 'saidas_1_parte', 'dataset_final_tratado.csv')
    
    # 2. Caminho alternativo (caso você rode o app de dentro da pasta 'dados')
    if not os.path.exists(caminho_csv):
        caminho_alternativo = os.path.join('saidas_1_parte', 'dataset_final_tratado.csv')
        if os.path.exists(caminho_alternativo):
            caminho_csv = caminho_alternativo
    
    # Verificação final
    if not os.path.exists(caminho_csv):
        st.error(f"❌ Erro Crítico: O arquivo não foi encontrado.")
        st.code(f"O sistema procurou em:\n1. {caminho_csv}\n2. saidas_1_parte/dataset_final_tratado.csv")
        return None
    
    # Leitura
    df = pd.read_csv(caminho_csv, sep=';')
    
    # Tratamento Numérico (Conversão de vírgula para ponto)
    cols_num = ['IDHM', 'Gini', 'Leitos_SUS|10k', '%_Fumantes', 'PIB_%', 
                'Taxa_Mortes_Isquemicas_Total_por_100k', 'Taxa_Mortes_Isquemicas_Adultos_Idosos_por_100k']
    for col in cols_num:
        if col in df.columns and df[col].dtype == object:
            df[col] = df[col].str.replace(',', '.').astype(float)
            
    # Engenharia de Features (Criação das Regiões)
    df['Regiao'] = df['Estado'].apply(definir_regiao)
    df['Regiao_Cod'] = df['Regiao'].apply(codigo_regiao)
    
    return df

@st.cache_resource
def carregar_modelo(target_name):
    nome_limpo = target_name.replace(' ', '_').replace('/', '_').lower()
    
    # Procura na pasta modelos (tenta raiz e subpasta dados/modelos)
    caminhos_possiveis = [
        f'modelos/modelo_{nome_limpo}.pkl',
        f'dados/modelos/modelo_{nome_limpo}.pkl'
    ]
    
    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            return joblib.load(caminho)
            
    return None

# --- CARGA INICIAL ---
df = carregar_dados()

if df is None:
    st.stop()

# --- SIDEBAR (CONTROLE) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/heart-health.png", width=80)
    st.title("Zetta Lab 2025")
    st.markdown("---")
    
    st.info("📅 **Controle de Tempo**")
    ano_sel = st.selectbox("Ano de Referência:", sorted(df['ano'].unique(), reverse=True))
    
    st.markdown("---")
    st.caption("Sistema de Apoio à Decisão")

# Filtro Global
df_filtrado = df[df['ano'] == ano_sel]

# --- TÍTULO PRINCIPAL ---
st.title("Monitoramento Estratégico de Saúde")
st.markdown(f"**Panorama Brasil {ano_sel}** | Doenças Isquêmicas do Coração (Adultos e Idosos)")

# --- ABAS DE NAVEGAÇÃO ---
abas = st.tabs(["📊 Panorama Nacional", "🤖 Simulador de Cenários", "🧠 Inteligência do Modelo"])

# --- ABA 1: PANORAMA ---
with abas[0]:
    col1, col2, col3, col4 = st.columns(4)
    mortes_adulto = df_filtrado['Taxa_Mortes_Isquemicas_Adultos_Idosos_por_100k'].mean()
    
    col1.metric("Mortalidade Média", f"{mortes_adulto:.2f}", help="Óbitos por 100k habitantes (Adultos/Idosos)")
    col2.metric("IDHM Médio", f"{df_filtrado['IDHM'].mean():.3f}")
    col3.metric("Leitos SUS (Média)", f"{df_filtrado['Leitos_SUS|10k'].mean():.1f}")
    col4.metric("Estados Analisados", len(df_filtrado))
    
    st.markdown("---")
    
    c_graf1, c_graf2 = st.columns(2)
    
    # Ranking
    fig_bar = px.bar(df_filtrado.sort_values('Taxa_Mortes_Isquemicas_Adultos_Idosos_por_100k'), 
                     x='Taxa_Mortes_Isquemicas_Adultos_Idosos_por_100k', y='Estado', color='Regiao',
                     title="Ranking Nacional de Mortalidade", orientation='h', height=600)
    c_graf1.plotly_chart(fig_bar, use_container_width=True)
    
    # Correlação
    fig_scat = px.scatter(df_filtrado, x='IDHM', y='Taxa_Mortes_Isquemicas_Adultos_Idosos_por_100k', 
                          size='Populacao', color='Regiao', title="Desenvolvimento (IDH) vs Mortalidade", height=400)
    c_graf2.plotly_chart(fig_scat, use_container_width=True)

# --- ABA 2: SIMULADOR (IA) ---
with abas[1]:
    st.header("Simulador Preditivo")
    st.markdown("Configure um cenário hipotético abaixo. O modelo IA recalculará a previsão baseada nos padrões históricos e regionais.")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.subheader("Parâmetros")
        
        regiao_sim = st.selectbox("Região do Cenário:", ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'])
        cod_reg_sim = codigo_regiao(regiao_sim)
        
        st.markdown("---")
        novo_idhm = st.slider("IDHM", 0.5, 0.9, 0.75)
        novo_gini = st.slider("Desigualdade (Gini)", 0.3, 0.7, 0.5)
        novos_leitos = st.slider("Leitos SUS/10k", 0.0, 50.0, 15.0)
        novo_fumo = st.slider("Tabagismo (%)", 5.0, 25.0, 10.0)
        novo_pib = st.slider("PIB (%)", -5.0, 5.0, 1.0)
        
        # Nota Explicativa (Paradoxos)
        with st.expander("ℹ️ Dúvidas sobre o comportamento?"):
            st.markdown("""
            **Por que aumentar Leitos parece aumentar a morte?**
            *Causalidade Reversa.* O modelo detectou que locais com mais mortes (grandes centros) possuem mais UTIs instaladas.
            
            **Por que Tabagismo parece proteger?**
            *Viés de Renda.* Estados com maior IDH (que salvam mais vidas) historicamente possuem registros mais altos de tabagismo neste dataset.
            """)

    with c2:
        st.subheader("Projeção do Modelo (Adultos/Idosos)")
        
        # Carrega o modelo vencedor
        modelo = carregar_modelo('Taxa_Mortes_Isquemicas_Adultos_Idosos_por_100k')
        
        if modelo:
            # Dataframe de entrada para o modelo (Mesma estrutura do treino)
            entrada = pd.DataFrame({
                'IDHM': [novo_idhm],
                'Gini': [novo_gini],
                'Leitos_SUS|10k': [novos_leitos],
                '%_Fumantes': [novo_fumo],
                'PIB_%': [novo_pib],
                'Regiao_Cod': [cod_reg_sim]
            })
            
            try:
                previsao = modelo.predict(entrada)[0]
                delta = previsao - mortes_adulto
                
                st.metric(label=f"Taxa Prevista para {regiao_sim}", value=f"{previsao:.2f}", delta=f"{delta:.2f}", delta_color="inverse")
                
                if delta < 0:
                    st.success("✅ Cenário de Redução de Mortalidade.")
                else:
                    st.error("⚠️ Cenário de Aumento de Mortalidade.")
            except Exception as e:
                st.error(f"Erro na predição: {e}")
                st.warning("Verifique se o modelo foi treinado com a coluna 'Regiao_Cod'.")
                
            st.info(f"Base de Comparação (Média Brasil {ano_sel}): {mortes_adulto:.2f}")
        else:
            st.warning("⚠️ Modelo não encontrado na pasta 'modelos'. Rode o notebook para gerar o arquivo .pkl.")

# --- ABA 3: EXPLICABILIDADE ---
with abas[2]:
    st.header("O que define o Risco?")
    st.write("Interpretação do Modelo (SHAP Values)")
    
    # Tenta carregar a imagem de várias pastas possíveis
    img_nome = "shap_summary_Taxa_Mortes_Isquemicas_Adultos_Idosos_por_100k.png"
    caminhos_img = [img_nome, f"dados/saidas_2_parte/{img_nome}", f"saidas_2_parte/{img_nome}"]
    
    img_carregada = False
    for p in caminhos_img:
        if os.path.exists(p):
            st.image(Image.open(p), caption="Impacto das Variáveis na Decisão da IA")
            img_carregada = True
            break
            
    if not img_carregada:
        st.warning(f"Imagem SHAP não encontrada. Verifique se o arquivo '{img_nome}' foi gerado pelo notebook.")