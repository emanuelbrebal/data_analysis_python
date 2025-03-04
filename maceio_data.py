import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

caminho_arquivo = os.path.join("C:\\", "Users", "Emmanuel", "Desktop", "SI - CESMAC", "QUARTO_PERIODO", "proj_mat_computacional", "dados_A303_D_2025-01-01_2025-02-24.csv")

dados = pd.read_csv(caminho_arquivo, sep=';', encoding="utf-8", on_bad_lines='warn', skiprows=10)
dados_header = pd.read_csv(caminho_arquivo, sep=';', encoding="utf-8", on_bad_lines='warn', nrows=1)

dados.rename(columns={
    'PRECIPITACAO TOTAL, DIARIO (AUT)(mm)': 'PRECIPITACAO',
    'TEMPERATURA MAXIMA, DIARIA (AUT)(°C)': 'TEMP MAXIMA',
    'TEMPERATURA MINIMA, DIARIA (AUT)(°C)': 'TEMP MINIMA', 
    'Data Medicao': 'DATA'
}, inplace=True)


dados['PRECIPITACAO'] = dados['PRECIPITACAO'].str.replace(',', '.').astype(float)
dados['TEMP MAXIMA'] = dados['TEMP MAXIMA'].str.replace(',', '.').astype(float)
dados['TEMP MINIMA'] = dados['TEMP MINIMA'].str.replace(',', '.').astype(float)


dados['DATA'] = pd.to_datetime(dados['DATA'], dayfirst=True) 

#calculos do primeiro grafico
temperatura_maior = dados['TEMP MAXIMA'].max()
temperatura_menor = dados['TEMP MINIMA'].min()

moda_temp_max = dados['TEMP MAXIMA'].mode()
moda_temp_max_value = moda_temp_max.iloc[0]
moda_temp_max_value = round(moda_temp_max_value, 2)

moda_temp_min = dados['TEMP MINIMA'].mode()
moda_temp_min_value = moda_temp_min.iloc[0]
moda_temp_min_value = round(moda_temp_min_value, 2)

media_temp_max = dados['TEMP MAXIMA'].mean()
media_temp_min = dados['TEMP MINIMA'].mean()

media_temp_max = round(media_temp_max, 2)
media_temp_min = round(media_temp_min, 2)

amplitude_termica = temperatura_maior - temperatura_menor

#primeiro grafico
plt.figure(figsize=(10, 6))
plt.bar(dados['DATA'], dados['TEMP MAXIMA'], label='Temperatura Máxima', color='red')
plt.bar(dados['DATA'], dados['TEMP MINIMA'], label='Temperatura Mínima', color='blue', alpha=0.7)
plt.title('Temperaturas Máxima e Mínima em Maceió')
plt.xlabel('Data')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True, prune='both'))
plt.grid(True)
#informações uteis do gráfico
plt.figtext(0.018, 0.01, f'T. Máxima mais alta: {temperatura_maior}°C', color='red', fontsize=10, ha='left')
plt.figtext(0.018, 0.04, f'Modas das temperaturas máximas: {moda_temp_max_value}°C', color='red', fontsize=10, ha='left')
plt.figtext(0.25, 0.01, f'T. Mínima mais baixa: {temperatura_menor}°C', color='blue', fontsize=10, ha='left')
plt.figtext(0.25, 0.04, f'Moda das temperaturas minimas: {moda_temp_min_value}°C', color='blue', fontsize=10, ha='left')
plt.figtext(0.55, 0.04, f'Média da Temperatura Mínima: {media_temp_min}°C', color='blue', fontsize=10, ha='left')
plt.figtext(0.55, 0.01, f'Média da Temperatura Máxima: {media_temp_max}°C', color='red', fontsize=10, ha='left')
plt.figtext(0.85, 0.01, f'Amplitude térmica: {round(amplitude_termica, 3)}°C', color='black', fontsize=10, ha='left')
plt.tight_layout()
plt.show()


#calculos segundo grafico

media_precipitacao = round(dados['PRECIPITACAO'].mean(), 2)

precipitacao_maxima = dados['PRECIPITACAO'].max()

precipitacao_minima = dados['PRECIPITACAO'].min()

mediana_precipitacao = dados['PRECIPITACAO'].median()

moda_precipitacao = dados['PRECIPITACAO'].mode()
moda_precipitacao_value = moda_precipitacao.iloc[0]
moda_precipitacao_value = round(moda_precipitacao_value, 2)

amplitude_precipitacao = precipitacao_maxima - precipitacao_minima

Q1 = dados['PRECIPITACAO'].quantile(0.25)
Q3 = dados['PRECIPITACAO'].quantile(0.75)
intervalo_quartis = Q3 - Q1

#segundo grafico
plt.figure(figsize=(10, 6))
plt.bar(dados['DATA'], dados['PRECIPITACAO'], color='green')
plt.title('Precipitação Total Diária de Maceió')
plt.xlabel('Data')
plt.ylabel('Precipitação (mm)')
# plt.xticks(rotation=45, ha='right')
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True, prune='both'))
#informações uteis do gráfico
plt.figtext(0.018, 0.01, f'Maior precipitação em um dia: {precipitacao_maxima}mm', color='red', fontsize=10, ha='left')
plt.figtext(0.018, 0.04, f'Menor precipitação em um dia: {precipitacao_minima}mm', color='red', fontsize=10, ha='left')
plt.figtext(0.25, 0.01, f'Mediana das precipitações: {mediana_precipitacao}mm', color='blue', fontsize=10, ha='left')
plt.figtext(0.25, 0.04, f'Moda das precipitações: {moda_precipitacao_value}mm', color='blue', fontsize=10, ha='left')
plt.figtext(0.25, 0.07, f'Média das precipitações: {media_precipitacao}mm', color='blue', fontsize=10, ha='left')
plt.figtext(0.55, 0.07, f'Primeiro quartil (25%): {Q1}mm', color='green', fontsize=10, ha='left')
plt.figtext(0.55, 0.04, f'Terceiro quartil (75%): {Q3}mm', color='green', fontsize=10, ha='left')
plt.figtext(0.55, 0.01, f'Intervalo Interquartílico: {intervalo_quartis}mm', color='green', fontsize=10, ha='left')
plt.figtext(0.85, 0.01, f'Amplitude das precipitações: {round(amplitude_precipitacao, 3)}mm', color='black', fontsize=10, ha='left')
plt.tight_layout()
plt.show()
