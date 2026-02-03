from narwhals import col
import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry
import os


# Ajustar path de busca de demais arquivos relacionados ao dashboard
try:
    # Tenta usar o __file__ (funciona no VS Code / Streamlit)
    path_app = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Se der erro, usa o diretório atual (funciona no Colab)
    path_app = os.getcwd()


# Configuração da página com Streamlit
st.set_page_config(
    page_title="Análise de Profissionais de Dados",
    page_icon="📊",
    layout="wide"  # Página ocupando a largura inteira disponível
)

# Carregar o dataset do path exato
caminho_arquivo = os.path.join(path_app, 'dados-imersao-final.csv')
df = pd.read_csv(caminho_arquivo)

# Barra lateral de filtros
st.sidebar.header("Filtros")

# Filtro por Ano
# Obtendo os anos únicos disponíveis no DataFrame
anos_disponiveis = sorted(df['ano'].unique())
# Chamada Streamlit que cria a caixa do filtro, com seleção múltipla dos anos disponíveis, 
# deixando todos os anos selecionados por padrão
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

# Filtro por Senioridade (Nível de Experiência)
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

# Filtro por Tipo de Contrato
contrato_disponiveis = sorted(df['contrato'].unique())
contrato_selecionados = st.sidebar.multiselect("Tipo de Contrato", contrato_disponiveis, default=contrato_disponiveis)

# Filtro por Tamanho da Empresa
tamanho_empresa_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanho_empresa_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanho_empresa_disponiveis, 
                                                      default=tamanho_empresa_disponiveis)   

# Filtragem do DataFrame com base nas seleções de Filtro do usuário
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contrato_selecionados)) &
    (df['tamanho_empresa'].isin(tamanho_empresa_selecionados))
]

# Conteúdo Principal da Página
# Título da Página
st.title("📊 Dashboard de Análise de Salários na área de Dados")
st.markdown("Explore os dados salariais na área de Dados nos últimos anos. " \
"Utilize os filtros na barra lateral para refinar a consulta.")

# --- Métricas Principais (KPIs) ---
st.subheader("Métricas Gerais (salário anual em USD) ")

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    salario_minimo = df_filtrado['usd'].min()
    total_registros = df_filtrado.shape[0]
    # "mode()" retorna a categoria mais frequente em formato tabela (visual padrão do Python). 
    # "mode()[0]" retorna só o valor da categoria mais frequente.
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
else:
    salario_medio, salario_maximo, salario_minimo, total_registros, cargo_mais_frequente = 0, 0, 0, 0, ""

# Layout em colunas para exibir as métricas principais
col1, col2, col3, col4 = st.columns(4)
# Definindo os conteúdos das colunas -- métrica e seu valor formatado
col1.metric("Salário Médio", f"${salario_medio:,.0f}")
col2.metric("Salário Máximo", f"${salario_maximo:,.0f}")
col3.metric("Salário Mínimo", f"${salario_minimo:,}")
col4.metric("Total de Registros", f"{total_registros:,}")

# # Novo layout em colunas para exibir mais métricas principais
col5, col6, col7, col8 = st.columns(4)
col5.metric("Cargo Mais Frequente", cargo_mais_frequente)

st.markdown("---")

# --- Análises visuais com Pltly ---
st.subheader("Gráficos")

col.graph1, col.graph2 = st.columns(2)

with col.graph1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        # OU:
        #top_cargos = df_filtrado.groupby('cargo')['usd'].mean().sort_values(ascending=False).head(10).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title='Top 10 Cargos com Maior Salário Médio Anual',
            labels={'usd': 'Salário Médio Anual (USD)', 'cargo': 'Cargo'}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado a exibir para gráfico de Cargos.")

with col.graph2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado, 
            x='usd', 
            nbins=30, 
            title='Distribuição dos Salários Anuais em USD',
            labels={'usd': 'Salário Anual (USD)'},
            color_discrete_sequence=['#636EFA']
        )
        # Ajustes no layout do gráfico
        grafico_hist.update_layout(title_x=0.1, yaxis_title='Quantidade de Pofissionais')
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado a exibir para gráfico de Distribuição de Salários.")

col.graph3, col.graph4 = st.columns(2)

with col.graph3:
    if not df_filtrado.empty:
        grafico_linha = px.line(
            df_filtrado.groupby('ano')['usd'].mean().reset_index(), 
            x='ano', 
            y='usd', 
            title='Evolução do Salário Médio Anual ao Longo dos Anos',
            labels={'ano': 'Ano', 'usd': 'Salário Médio Anual (USD)'},
            markers=True
        )
        grafico_linha.update_layout(title_x=0.1)
        st.plotly_chart(grafico_linha, use_container_width=True)
    else:
        st.warning("Nenhum dado a exibir para gráfico de Evolução de Salários.")

with col.graph4:
    if not df_filtrado.empty:
        contagem_remoto = df_filtrado['remoto'].value_counts().reset_index()
        contagem_remoto.columns = ['modo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            contagem_remoto, 
            names='modo_trabalho', 
            values='quantidade', 
            title='Proporção dos Modos de Trabalho',
            hole=0.5
        )
        grafico_remoto.update_traces(textposition='inside', textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado a exibir para gráfico de Modo de Trabalho.")


# Função que converte as siglas do DataFrame de iso-2 para iso-3.
def iso2_para_iso3(code):
  try:
    return pycountry.countries.get(alpha_2=code).alpha_3
  except:
    return None

# Adiciona nova coluna ao DataFrame com os países em formato iso-3
df_filtrado['empresa_iso3'] = df_filtrado['empresa'].apply(iso2_para_iso3)

# Cria dataframe apenas com os registros com cargo "Data Scientist"
df_ds = df_filtrado[df_filtrado['cargo'] == "Data Scientist"]

# Cria o bloco de dados para o gráfico, agrupando apenas Pais da Empresa e Média salarial
media_sal_paisempresa_ds = df_ds.groupby('empresa_iso3')['usd'].mean().reset_index()

# Gerar o gráfico lúdico (choropleth)
col.graph5 = st.columns(1)

with col.graph5[0]:
    if not media_sal_paisempresa_ds.empty:
        grafico_salario_pais = px.choropleth(
            media_sal_paisempresa_ds,
            locations='empresa_iso3',
            color='usd',
            hover_name='empresa_iso3',
            title='Média Salarial Anual de Cientista de Dados por País',
            color_continuous_scale='rdylgn',
            labels={'usd': 'Salário (USD)', 'empresa_iso3': 'País da Empresa'}
        )
        st.plotly_chart(grafico_salario_pais, use_container_width=True)
    else:
        st.warning("Nenhum dado a exibir para gráfico de Média Salarial por País.")

st.markdown("---")

# Seção com visual da tabela de dados
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
