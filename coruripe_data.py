import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def carrega_dados(caminho_arquivo):
    dados = pd.read_csv(caminho_arquivo, sep=';', encoding="utf-8", on_bad_lines='warn', skiprows=10)
   
    dados.rename(columns={
        'PRECIPITACAO TOTAL, DIARIO (AUT)(mm)': 'PRECIPITACAO',
        'TEMPERATURA MAXIMA, DIARIA (AUT)(°C)': 'TEMP MAXIMA',
        'TEMPERATURA MINIMA, DIARIA (AUT)(°C)': 'TEMP MINIMA', 
        'Data Medicao': 'DATA'
    }, inplace=True)

    if dados['PRECIPITACAO'].dtype == 'object':
        dados['PRECIPITACAO'] = dados['PRECIPITACAO'].str.replace(',', '.').astype(float)

    if dados['TEMP MAXIMA'].dtype == 'object':
        dados['TEMP MAXIMA'] = dados['TEMP MAXIMA'].str.replace(',', '.').astype(float)

    if dados['TEMP MINIMA'].dtype == 'object':
        dados['TEMP MINIMA'] = dados['TEMP MINIMA'].str.replace(',', '.').astype(float)

    dados['DATA'] = pd.to_datetime(dados['DATA'], format="%Y-%m-%d", errors='coerce') 

    return dados


#calculos do primeiro grafico

def calcula_infos(dados):
    temperatura_maior = dados['TEMP MAXIMA'].max()
    temperatura_menor = dados['TEMP MINIMA'].min()

    moda_temp_max = dados['TEMP MAXIMA'].mode()
    moda_temp_max_value = round(moda_temp_max.iloc[0], 2)

    moda_temp_min = dados['TEMP MINIMA'].mode()
    moda_temp_min_value = round(moda_temp_min.iloc[0], 2)

    media_temp_max = round(dados['TEMP MAXIMA'].mean(), 2)
    media_temp_min = round(dados['TEMP MINIMA'].mean(), 2)


    amplitude_termica = temperatura_maior - temperatura_menor

    return {
            "temperatura_maior": temperatura_maior,
            "temperatura_menor": temperatura_menor,
            "moda_temp_max_value": moda_temp_max_value,
            "moda_temp_min_value": moda_temp_min_value,
            "media_temp_max": media_temp_max,
            "media_temp_min": media_temp_min,
            "amplitude_termica": amplitude_termica
        }



def gera_grafico_temperaturas(dados, estatisticas_temp):
    plt.figure(figsize=(10, 6))
    plt.bar(dados['DATA'], dados['TEMP MAXIMA'], label='Temperatura Máxima', color='red')
    plt.bar(dados['DATA'], dados['TEMP MINIMA'], label='Temperatura Mínima', color='blue', alpha=0.7)
    plt.title('Temperaturas Máxima e Mínima em Coruripe')
    plt.xlabel('Data')
    plt.ylabel('Temperatura (°C)')
    plt.legend()
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True, prune='both'))
    plt.grid(True)
    #informações uteis do gráfico
    plt.figtext(0.018, 0.01, f'T. Máxima mais alta: {estatisticas_temp['temperatura_maior']}°C', color='red', fontsize=10, ha='left')
    plt.figtext(0.018, 0.04, f'Modas das temperaturas máximas: {estatisticas_temp["moda_temp_max_value"]}°C', color='red', fontsize=10, ha='left')
    plt.figtext(0.25, 0.01, f'T. Mínima mais baixa: {estatisticas_temp["temperatura_menor"]}°C', color='blue', fontsize=10, ha='left')
    plt.figtext(0.25, 0.04, f'Moda das temperaturas minimas: {estatisticas_temp["moda_temp_min_value"]}°C', color='blue', fontsize=10, ha='left')
    plt.figtext(0.55, 0.04, f'Média da Temperatura Mínima: {estatisticas_temp["media_temp_min"]}°C', color='blue', fontsize=10, ha='left')
    plt.figtext(0.55, 0.01, f'Média da Temperatura Máxima: {estatisticas_temp["media_temp_max"]}°C', color='red', fontsize=10, ha='left')
    plt.figtext(0.85, 0.01, f'Amplitude térmica: {round(estatisticas_temp["amplitude_termica"], 3)}°C', color='black', fontsize=10, ha='left')
    plt.tight_layout()
    plt.show()


def calcular_estatisticas_precipitacao(dados):
    media_precipitacao = round(dados['PRECIPITACAO'].mean(), 2)

    precipitacao_maxima = dados['PRECIPITACAO'].max()

    precipitacao_minima = dados['PRECIPITACAO'].min()

    mediana_precipitacao = dados['PRECIPITACAO'].median()

    moda_precipitacao = dados['PRECIPITACAO'].mode()

    if not moda_precipitacao.empty:
        moda_precipitacao_value = moda_precipitacao.iloc[0]
        moda_precipitacao_value = round(moda_precipitacao_value, 2)
    else:
        moda_precipitacao_value = None


    amplitude_precipitacao = precipitacao_maxima - precipitacao_minima

    Q1 = dados['PRECIPITACAO'].quantile(0.25)
    Q3 = dados['PRECIPITACAO'].quantile(0.75)
    intervalo_quartis = Q3 - Q1

    return {
        "media_precipitacao": media_precipitacao,
        "precipitacao_maxima": precipitacao_maxima,
        "precipitacao_minima": precipitacao_minima,
        "mediana_precipitacao": mediana_precipitacao,
        "moda_precipitacao": moda_precipitacao_value,
        "amplitude_precipitacao": amplitude_precipitacao,
        "Q1": Q1,
        "Q3": Q3,
        "intervalo_quartis": intervalo_quartis
    }
#calculos segundo grafico


def gerar_grafico_precipitacao(dados, estatisticas_precipitacao):
    plt.figure(figsize=(10, 6))
    plt.bar(dados['DATA'], dados['PRECIPITACAO'], color='green')
    plt.title('Precipitação Total Diária de Coruripe')
    plt.xlabel('Data')
    plt.ylabel('Precipitação (mm)')
    # plt.xticks(rotation=45, ha='right')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True, prune='both'))
    #informações uteis do gráfico
    dados_filtrados = dados.dropna(subset=['PRECIPITACAO'])

    if not dados_filtrados.empty:
        plt.figtext(0.018, 0.01, f'Maior precipitação em um dia: {estatisticas_precipitacao["precipitacao_maxima"]}mm', color='red', fontsize=10, ha='left')
        plt.figtext(0.018, 0.04, f'Menor precipitação em um dia: {estatisticas_precipitacao["precipitacao_minima"]}mm', color='red', fontsize=10, ha='left')
        plt.figtext(0.25, 0.01, f'Mediana das precipitações: {estatisticas_precipitacao["mediana_precipitacao"]}mm', color='blue', fontsize=10, ha='left')
        plt.figtext(0.25, 0.04, f'Moda das precipitações: {estatisticas_precipitacao["moda_precipitacao"]}mm', color='blue', fontsize=10, ha='left')
        plt.figtext(0.25, 0.07, f'Média das precipitações: {estatisticas_precipitacao["media_precipitacao"]}mm', color='blue', fontsize=10, ha='left')
        plt.figtext(0.55, 0.07, f'Primeiro quartil (25%): {estatisticas_precipitacao["Q1"]}mm', color='green', fontsize=10, ha='left')
        plt.figtext(0.55, 0.04, f'Terceiro quartil (75%): {estatisticas_precipitacao["Q3"]}mm', color='green', fontsize=10, ha='left')
        plt.figtext(0.55, 0.01, f'Intervalo Interquartílico: {estatisticas_precipitacao["intervalo_quartis"]}mm', color='green', fontsize=10, ha='left')
        plt.figtext(0.85, 0.01, f'Amplitude das precipitações: {round(estatisticas_precipitacao["amplitude_precipitacao"], 3)}mm', color='black', fontsize=10, ha='left')
    else:
        plt.figtext(0.1, 0.01, f'CONCLUSÃO: Não houve precipitações na base de dados.', color='black', fontsize=10, ha='left')
    plt.tight_layout()
    plt.show()

