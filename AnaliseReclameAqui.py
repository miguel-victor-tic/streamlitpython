import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

st.title('Análise de Dados DeepLearn')


#Dados
DF_IBYTE = pd.read_csv('RECLAMEAQUI_IBYTE.csv')
DF_HAPVIDA = pd.read_csv('RECLAMEAQUI_HAPVIDA.csv')
DF_NAGEM = pd.read_csv('RECLAMEAQUI_NAGEM.csv')

# Criando a variável para Data
if {'ANO', 'MES', 'DIA'}.issubset(DF_IBYTE.columns):

    DF_IBYTE['data'] = DF_IBYTE.apply(lambda row: f"{int(row['ANO'])}-{int(row['MES']):02d}-{int(row['DIA']):02d}", axis=1)
    DF_IBYTE['data'] = pd.to_datetime(DF_IBYTE['data'], errors='coerce')

    print(DF_IBYTE['data'].isnull().sum(), "datas inválidas foram encontradas.")
    DF_IBYTE = DF_IBYTE.dropna(subset=['data'])
    reclamacoes_por_data = DF_IBYTE.groupby('data').size().reset_index(name='count')
    num_reclamacoes = reclamacoes_por_data['count']
    colors = np.linspace(0, 1, len(num_reclamacoes))
    Fig_Numero_ReclamacoesIbyte = go.Figure()
    Fig_Numero_ReclamacoesIbyte.add_trace(go.Scatter(
        x=reclamacoes_por_data['data'],
        y=reclamacoes_por_data['count'],
        mode='lines+markers',  
        marker=dict(
            size=8,
            color=colors,  
            colorscale='Viridis',  
            showscale=True,
            colorbar=dict(title="Número de Reclamações")  
        ),
        line=dict(
            color='royalblue',
            width=2,
            dash='solid'  
        ),
        name='Reclamações',
        hovertemplate='Data: %{x}<br>Reclamações: %{y}<extra></extra>'  
    ))
    Fig_Numero_ReclamacoesIbyte.add_trace(go.Scatter(
        x=reclamacoes_por_data['data'],
        y=reclamacoes_por_data['count'],
        fill='tozeroy',
        mode='none',  
        fillcolor='rgba(0, 100, 255, 0.2)', 
        showlegend=False
    ))

    Fig_Numero_ReclamacoesIbyte.update_layout(
        title='Série Temporal do Número de Reclamações',
        xaxis_title='Data',
        yaxis_title='Número de Reclamações',
        title_x=0.5,  
        template='plotly_dark', 
        xaxis=dict(
            showgrid=True,  
            tickangle=-45, 
            type='date'
        ),
        yaxis=dict(showgrid=True), 
        hovermode='x',  
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        legend=dict(
            x=0.01,  
            y=0.99,
            bgcolor='rgba(255, 255, 255, 0.2)',  
            bordercolor='lightgrey',
            borderwidth=1
        )
    )
    Fig_Numero_ReclamacoesIbyte.update_xaxes(rangeslider_visible=True)
else:
    print("As colunas 'ANO', 'MES' e 'DIA' não estão presentes no DataFrame.")


status_frequencia = DF_IBYTE['STATUS'].value_counts()


Fig_Reclamacao_StatusIbyte = go.Figure()


for status in status_frequencia.index:
    Fig_Reclamacao_StatusIbyte.add_trace(go.Bar(
        x=[status],
        y=[status_frequencia[status]],
        name=status,  
        text=[status_frequencia[status]],  
        textposition='auto',
        marker=dict(color=status_frequencia[status], colorscale='Viridis'),  
        visible=True  
    ))

Fig_Reclamacao_StatusIbyte.update_layout(
    title="Frequência de Reclamações por Status",
    xaxis_title="Status",
    yaxis_title="Número de Reclamações",
    title_x=0.5,
    template='plotly_white',
    xaxis=dict(tickangle=-45),
    showlegend=False  
)

buttons = []
for status in status_frequencia.index:
    buttons.append(dict(
        args=[{'visible': [status == i for i in status_frequencia.index]}],
        label=status,
        method='update'
    ))

buttons.append(dict(
    args=[{'visible': [True] * len(status_frequencia)}],
    label='Todos',
    method='update'
))

Fig_Reclamacao_StatusIbyte.update_layout(
    updatemenus=[{
        'buttons': buttons,
        'direction': 'down',
        'showactive': True,
        'x': 0.17, 
        'y': 1.15
    }]
)


# Estados
reclamacoes_por_estado = DF_IBYTE['LOCAL'].value_counts()
top_10_estados = reclamacoes_por_estado.nlargest(10)

Fig_Estado_ReclamacaoIbyte = go.Figure()

for estado in top_10_estados.index:
    Fig_Estado_ReclamacaoIbyte.add_trace(go.Bar(
        x=[estado],
        y=[top_10_estados[estado]],
        name=estado,
        text=[top_10_estados[estado]],  
        textposition='auto',
        marker=dict(color=top_10_estados[estado], colorscale='Viridis'),
        visible=True  
    ))

Fig_Estado_ReclamacaoIbyte.update_layout(
    title="Top 10 Estados com Mais Reclamações",
    xaxis_title="Estado",
    yaxis_title="Número de Reclamações",
    title_x=0.5,
    template='plotly_white',
    xaxis=dict(tickangle=-45),
    showlegend=False  
)

buttons = []
for estado in top_10_estados.index:
    buttons.append(dict(
        args=[{'visible': [estado == i for i in top_10_estados.index]}],
        label=estado,
        method='update'
    ))

buttons.append(dict(
    args=[{'visible': [True] * len(top_10_estados)}],
    label='Top 10',
    method='update'
))

Fig_Estado_ReclamacaoIbyte.update_layout(
    updatemenus=[{
        'buttons': buttons,
        'direction': 'down',
        'showactive': True,
        'x': 0.17,  
        'y': 1.15
    }]
)

DF_IBYTE['tamanho_descricao'] = DF_IBYTE['DESCRICAO'].apply(len)

Fig_Tamanho_DescricaoIbyte = px.histogram(
    DF_IBYTE,
    x='tamanho_descricao',
    nbins=30,
    title='Distribuição do Tamanho das Descrições',
    labels={'tamanho_descricao': 'Tamanho da Descrição (número de caracteres)'},
    color_discrete_sequence=['blue'],
    marginal='rug' 
)
kde_data = DF_IBYTE['tamanho_descricao'].plot.kde(bw_method=0.5) 
x_values = kde_data.get_lines()[0].get_xdata()
y_values = kde_data.get_lines()[0].get_ydata()

y_values_scaled = y_values * len(DF_IBYTE) * (max(DF_IBYTE['tamanho_descricao']) - min(DF_IBYTE['tamanho_descricao'])) / 30


Fig_Tamanho_DescricaoIbyte.add_trace(go.Scatter(
    x=x_values,
    y=y_values_scaled + 20,  
    mode='lines',
    name='Densidade',
    line=dict(color='orange', width=2)
))

Fig_Tamanho_DescricaoIbyte.update_layout(
    xaxis_title='Tamanho da Descrição',
    yaxis_title='Frequência',
    title_x=0.5, 
    template='plotly_white',  
    yaxis=dict(showgrid=True) 
)

if {'ANO', 'MES', 'DIA'}.issubset(DF_NAGEM.columns):

    DF_NAGEM['data'] = DF_NAGEM.apply(lambda row: f"{int(row['ANO'])}-{int(row['MES']):02d}-{int(row['DIA']):02d}", axis=1)
    DF_NAGEM['data'] = pd.to_datetime(DF_NAGEM['data'], errors='coerce')

    print(DF_NAGEM['data'].isnull().sum(), "datas inválidas foram encontradas.")
    DF_NAGEM = DF_NAGEM.dropna(subset=['data'])
    reclamacoes_por_data = DF_NAGEM.groupby('data').size().reset_index(name='count')
    num_reclamacoes = reclamacoes_por_data['count']
    colors = np.linspace(0, 1, len(num_reclamacoes))
    Fig_Numero_ReclamacoesNAGEM = go.Figure()
    Fig_Numero_ReclamacoesNAGEM.add_trace(go.Scatter(
        x=reclamacoes_por_data['data'],
        y=reclamacoes_por_data['count'],
        mode='lines+markers',  
        marker=dict(
            size=8,
            color=colors,  
            colorscale='Viridis',  
            showscale=True,
            colorbar=dict(title="Número de Reclamações")  
        ),
        line=dict(
            color='royalblue',
            width=2,
            dash='solid'  
        ),
        name='Reclamações',
        hovertemplate='Data: %{x}<br>Reclamações: %{y}<extra></extra>'  
    ))
    Fig_Numero_ReclamacoesNAGEM.add_trace(go.Scatter(
        x=reclamacoes_por_data['data'],
        y=reclamacoes_por_data['count'],
        fill='tozeroy',
        mode='none',  
        fillcolor='rgba(0, 100, 255, 0.2)', 
        showlegend=False
    ))

    Fig_Numero_ReclamacoesNAGEM.update_layout(
        title='Série Temporal do Número de Reclamações',
        xaxis_title='Data',
        yaxis_title='Número de Reclamações',
        title_x=0.5,  
        template='plotly_dark', 
        xaxis=dict(
            showgrid=True,  
            tickangle=-45, 
            type='date'
        ),
        yaxis=dict(showgrid=True), 
        hovermode='x',  
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        legend=dict(
            x=0.01,  
            y=0.99,
            bgcolor='rgba(255, 255, 255, 0.2)',  
            bordercolor='lightgrey',
            borderwidth=1
        )
    )
    Fig_Numero_ReclamacoesNAGEM.update_xaxes(rangeslider_visible=True)
else:
    print("As colunas 'ANO', 'MES' e 'DIA' não estão presentes no DataFrame.")


status_frequencia = DF_HAPVIDA['STATUS'].value_counts()

Fig_Reclamacao_StatusHAPVIDA = go.Figure()


for status in status_frequencia.index:
    Fig_Reclamacao_StatusHAPVIDA.add_trace(go.Bar(
        x=[status],
        y=[status_frequencia[status]],
        name=status,  
        text=[status_frequencia[status]],  
        textposition='auto',
        marker=dict(color=status_frequencia[status], colorscale='Viridis'),  
        visible=True  
    ))

Fig_Reclamacao_StatusHAPVIDA.update_layout(
    title="Frequência de Reclamações por Status",
    xaxis_title="Status",
    yaxis_title="Número de Reclamações",
    title_x=0.5,
    template='plotly_white',
    xaxis=dict(tickangle=-45),
    showlegend=False  
)

buttons = []
for status in status_frequencia.index:
    buttons.append(dict(
        args=[{'visible': [status == i for i in status_frequencia.index]}],
        label=status,
        method='update'
    ))

buttons.append(dict(
    args=[{'visible': [True] * len(status_frequencia)}],
    label='Todos',
    method='update'
))

Fig_Reclamacao_StatusHAPVIDA.update_layout(
    updatemenus=[{
        'buttons': buttons,
        'direction': 'down',
        'showactive': True,
        'x': 0.17, 
        'y': 1.15
    }]
)


status_frequencia = DF_NAGEM['STATUS'].value_counts()


Fig_Reclamacao_StatusNAGEM = go.Figure()


for status in status_frequencia.index:
    Fig_Reclamacao_StatusNAGEM.add_trace(go.Bar(
        x=[status],
        y=[status_frequencia[status]],
        name=status,  
        text=[status_frequencia[status]],  
        textposition='auto',
        marker=dict(color=status_frequencia[status], colorscale='Viridis'),  
        visible=True  
    ))

Fig_Reclamacao_StatusNAGEM.update_layout(
    title="Frequência de Reclamações por Status",
    xaxis_title="Status",
    yaxis_title="Número de Reclamações",
    title_x=0.5,
    template='plotly_white',
    xaxis=dict(tickangle=-45),
    showlegend=False  
)

buttons = []
for status in status_frequencia.index:
    buttons.append(dict(
        args=[{'visible': [status == i for i in status_frequencia.index]}],
        label=status,
        method='update'
    ))

buttons.append(dict(
    args=[{'visible': [True] * len(status_frequencia)}],
    label='Todos',
    method='update'
))

Fig_Reclamacao_StatusNAGEM.update_layout(
    updatemenus=[{
        'buttons': buttons,
        'direction': 'down',
        'showactive': True,
        'x': 0.17, 
        'y': 1.15
    }]
)

# Estados
reclamacoes_por_estado = DF_NAGEM['LOCAL'].value_counts()
top_10_estados = reclamacoes_por_estado.nlargest(10)

Fig_Estado_ReclamacaoNAGEM = go.Figure()

for estado in top_10_estados.index:
    Fig_Estado_ReclamacaoNAGEM.add_trace(go.Bar(
        x=[estado],
        y=[top_10_estados[estado]],
        name=estado, 
        text=[top_10_estados[estado]],  
        textposition='auto',
        marker=dict(color=top_10_estados[estado], colorscale='Viridis'),
        visible=True  
    ))

Fig_Estado_ReclamacaoNAGEM.update_layout(
    title="Top 10 Estados com Mais Reclamações",
    xaxis_title="Estado",
    yaxis_title="Número de Reclamações",
    title_x=0.5,
    template='plotly_white',
    xaxis=dict(tickangle=-45),
    showlegend=False  
)

buttons = []
for estado in top_10_estados.index:
    buttons.append(dict(
        args=[{'visible': [estado == i for i in top_10_estados.index]}],
        label=estado,
        method='update'
    ))

buttons.append(dict(
    args=[{'visible': [True] * len(top_10_estados)}],
    label='Top 10',
    method='update'
))

Fig_Estado_ReclamacaoNAGEM.update_layout(
    updatemenus=[{
        'buttons': buttons,
        'direction': 'down',
        'showactive': True,
        'x': 0.17, 
        'y': 1.15
    }]
)

DF_NAGEM['tamanho_descricao'] = DF_NAGEM['DESCRICAO'].apply(len)

Fig_Tamanho_DescricaoNAGEM = px.histogram(
    DF_NAGEM,
    x='tamanho_descricao',
    nbins=30,
    title='Distribuição do Tamanho das Descrições',
    labels={'tamanho_descricao': 'Tamanho da Descrição (número de caracteres)'},
    color_discrete_sequence=['blue'],
    marginal='rug'  
)
kde_data = DF_NAGEM['tamanho_descricao'].plot.kde(bw_method=0.5)  
x_values = kde_data.get_lines()[0].get_xdata()
y_values = kde_data.get_lines()[0].get_ydata()

y_values_scaled = y_values * len(DF_NAGEM) * (max(DF_NAGEM['tamanho_descricao']) - min(DF_NAGEM['tamanho_descricao'])) / 30

Fig_Tamanho_DescricaoNAGEM.add_trace(go.Scatter(
    x=x_values,
    y=y_values_scaled + 20,  
    mode='lines',
    name='Densidade',
    line=dict(color='orange', width=2)
))

Fig_Tamanho_DescricaoNAGEM.update_layout(
    xaxis_title='Tamanho da Descrição',
    yaxis_title='Frequência',
    title_x=0.5,  
    template='plotly_white',  
    yaxis=dict(showgrid=True)  
)

if {'ANO', 'MES', 'DIA'}.issubset(DF_HAPVIDA.columns):

    DF_HAPVIDA['data'] = DF_HAPVIDA.apply(lambda row: f"{int(row['ANO'])}-{int(row['MES']):02d}-{int(row['DIA']):02d}", axis=1)
    DF_HAPVIDA['data'] = pd.to_datetime(DF_HAPVIDA['data'], errors='coerce')

    print(DF_HAPVIDA['data'].isnull().sum(), "datas inválidas foram encontradas.")
    DF_HAPVIDA = DF_HAPVIDA.dropna(subset=['data'])
    reclamacoes_por_data = DF_HAPVIDA.groupby('data').size().reset_index(name='count')
    num_reclamacoes = reclamacoes_por_data['count']
    colors = np.linspace(0, 1, len(num_reclamacoes))
    Fig_Numero_ReclamacoesHAPVIDA = go.Figure()
    Fig_Numero_ReclamacoesHAPVIDA.add_trace(go.Scatter(
        x=reclamacoes_por_data['data'],
        y=reclamacoes_por_data['count'],
        mode='lines+markers',  
        marker=dict(
            size=8,
            color=colors,  
            colorscale='Viridis',  
            showscale=True,
            colorbar=dict(title="Número de Reclamações")  
        ),
        line=dict(
            color='royalblue',
            width=2,
            dash='solid'  
        ),
        name='Reclamações',
        hovertemplate='Data: %{x}<br>Reclamações: %{y}<extra></extra>'  
    ))
    Fig_Numero_ReclamacoesHAPVIDA.add_trace(go.Scatter(
        x=reclamacoes_por_data['data'],
        y=reclamacoes_por_data['count'],
        fill='tozeroy',
        mode='none',  
        fillcolor='rgba(0, 100, 255, 0.2)', 
        showlegend=False
    ))

    Fig_Numero_ReclamacoesHAPVIDA.update_layout(
        title='Série Temporal do Número de Reclamações',
        xaxis_title='Data',
        yaxis_title='Número de Reclamações',
        title_x=0.5,  
        template='plotly_dark', 
        xaxis=dict(
            showgrid=True,  
            tickangle=-45, 
            type='date'
        ),
        yaxis=dict(showgrid=True), 
        hovermode='x',  
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        legend=dict(
            x=0.01,  
            y=0.99,
            bgcolor='rgba(255, 255, 255, 0.2)',  
            bordercolor='lightgrey',
            borderwidth=1
        )
    )
    Fig_Numero_ReclamacoesHAPVIDA.update_xaxes(rangeslider_visible=True)
else:
    print("As colunas 'ANO', 'MES' e 'DIA' não estão presentes no DataFrame.")

reclamacoes_por_estado = DF_HAPVIDA['LOCAL'].value_counts()
top_10_estados = reclamacoes_por_estado.nlargest(10)

Fig_Estado_ReclamacaoHAPVIDA = go.Figure()

for estado in top_10_estados.index:
    Fig_Estado_ReclamacaoHAPVIDA.add_trace(go.Bar(
        x=[estado],
        y=[top_10_estados[estado]],
        name=estado,  
        text=[top_10_estados[estado]], 
        textposition='auto',
        marker=dict(color=top_10_estados[estado], colorscale='Viridis'),
        visible=True  
    ))

Fig_Estado_ReclamacaoHAPVIDA.update_layout(
    title="Top 10 Estados com Mais Reclamações",
    xaxis_title="Estado",
    yaxis_title="Número de Reclamações",
    title_x=0.5,
    template='plotly_white',
    xaxis=dict(tickangle=-45),
    showlegend=False  
)

buttons = []
for estado in top_10_estados.index:
    buttons.append(dict(
        args=[{'visible': [estado == i for i in top_10_estados.index]}],
        label=estado,
        method='update'
    ))

buttons.append(dict(
    args=[{'visible': [True] * len(top_10_estados)}],
    label='Top 10',
    method='update'
))

Fig_Estado_ReclamacaoHAPVIDA.update_layout(
    updatemenus=[{
        'buttons': buttons,
        'direction': 'down',
        'showactive': True,
        'x': 0.17,  
        'y': 1.15
    }]
)

DF_HAPVIDA['tamanho_descricao'] = DF_HAPVIDA['DESCRICAO'].apply(len)

Fig_Tamanho_DescricaoHAPVIDA = px.histogram(
    DF_HAPVIDA,
    x='tamanho_descricao',
    nbins=30,
    title='Distribuição do Tamanho das Descrições',
    labels={'tamanho_descricao': 'Tamanho da Descrição (número de caracteres)'},
    color_discrete_sequence=['blue'],
    marginal='rug'  
)

kde_data = DF_HAPVIDA['tamanho_descricao'].plot.kde(bw_method=0.5) 
x_values = kde_data.get_lines()[0].get_xdata()
y_values = kde_data.get_lines()[0].get_ydata()

y_values_scaled = y_values * len(DF_HAPVIDA) * (max(DF_HAPVIDA['tamanho_descricao']) - min(DF_HAPVIDA['tamanho_descricao'])) / 30

Fig_Tamanho_DescricaoHAPVIDA.add_trace(go.Scatter(
    x=x_values,
    y=y_values_scaled + 20,  
    mode='lines',
    name='Densidade',
    line=dict(color='orange', width=2)
))

Fig_Tamanho_DescricaoHAPVIDA.update_layout(
    xaxis_title='Tamanho da Descrição',
    yaxis_title='Frequência',
    title_x=0.5, 
    template='plotly_white',  
    yaxis=dict(showgrid=True)
)

# MENU LATERAL 
with st.sidebar:
        seletor=st.selectbox(
    "Selecione a Loja",["--SELECIONE--","IBYTE","NAGEM","HAPVIDA"]
)


# Gráfico
if seletor=="--SELECIONE--":
    st.write("---")
    st.write("Selecione uma loja no menu ao lado")
    st.write("---")
    
if seletor=="IBYTE":
    st.write("---")
    st.header("Este dashboard apresenta uma análise das reclamações no portal Reclame Aqui sobre a empresa Ibyte.")
    st.write("---")   
    st.subheader("Série temporal do número de reclamações.")      
    st.plotly_chart(Fig_Numero_ReclamacoesIbyte) 
    st.write("---")   
    st.subheader("Frequência de reclamações por estado.")      
    st.plotly_chart(Fig_Estado_ReclamacaoIbyte) 
    st.write("---")   
    st.subheader("Frequência de cada tipo de status.")      
    st.plotly_chart(Fig_Reclamacao_StatusIbyte)
    st.write("---")   
    st.subheader("Distribuição do tamanho do texto.")      
    st.plotly_chart(Fig_Tamanho_DescricaoIbyte)

if seletor=="NAGEM":
    st.write("---")
    st.header("Este dashboard apresenta uma análise das reclamações no portal Reclame Aqui sobre a empresa Nagem.")
    st.write("---")   
    st.subheader("Série temporal do número de reclamações.")      
    st.plotly_chart(Fig_Numero_ReclamacoesNAGEM) 
    st.write("---")   
    st.subheader("Frequência de reclamações por estado.")      
    st.plotly_chart(Fig_Estado_ReclamacaoNAGEM) 
    st.write("---")   
    st.subheader("Frequência de cada tipo de status.")      
    st.plotly_chart(Fig_Reclamacao_StatusNAGEM)
    st.write("---")   
    st.subheader("Distribuição do tamanho do texto.")      
    st.plotly_chart(Fig_Tamanho_DescricaoNAGEM)

if seletor=="HAPVIDA":
    st.write("---")
    st.header("Este dashboard apresenta uma análise das reclamações no portal Reclame Aqui sobre a empresa Hapvida.")
    st.write("---")   
    st.subheader("Série temporal do número de reclamações.")      
    st.plotly_chart(Fig_Numero_ReclamacoesHAPVIDA) 
    st.write("---")   
    st.subheader("Frequência de reclamações por estado.")      
    st.plotly_chart(Fig_Estado_ReclamacaoHAPVIDA) 
    st.write("---")   
    st.subheader("Frequência de cada tipo de status.")      
    st.plotly_chart(Fig_Reclamacao_StatusHAPVIDA)
    st.write("---")   
    st.subheader("Distribuição do tamanho do texto.")      
    st.plotly_chart(Fig_Tamanho_DescricaoHAPVIDA)
    
# Gráfico
#st.bar_chart(data.set_index('Categoria'))
