import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def obter_retornos(tickers, start_date, end_date):
    """
    Obtém os retornos percentuais dos ativos para um período específico.

    Args:
        tickers (list): Lista de tickers dos ativos.
        start_date (str): Data de início no formato "YYYY-MM-DD".
        end_date (str): Data de fim no formato "YYYY-MM-DD".

    Returns:
        Um DataFrame contendo os retornos percentuais dos ativos.
    """
    retornos = pd.DataFrame()

    for ticker in tickers:
        data = yf.download(ticker, start=start_date, end=end_date)
        retornos[ticker] = data['Adj Close'].pct_change()

    return retornos

def criar_variaveis_preditoras(retornos, janela):
    """
    Cria variáveis preditoras para o modelo de regressão.

    Args:
        retornos (DataFrame): DataFrame contendo os retornos percentuais dos ativos.
        janela (int): O tamanho da janela para calcular as variáveis preditoras.

    Returns:
        Um DataFrame contendo variáveis preditoras.
    """
    variaveis_preditoras = pd.DataFrame()

    for ticker in retornos.columns:
        variaveis_preditoras[f'{ticker}_retorno'] = retornos[ticker]
        variaveis_preditoras[f'{ticker}_mudanca'] = retornos[ticker].shift(1)
        variaveis_preditoras[f'{ticker}_media'] = retornos[ticker].rolling(window=janela).mean()

    return variaveis_preditoras

def treinar_modelo(variaveis_preditoras, retornos_futuros):
    # Ajusta as dimensões dos dados
    X = variaveis_preditoras.values
    y = retornos_futuros.values

    # Divide os dados em conjunto de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treina o modelo
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    return modelo

def plotar_previsoes(modelo, variaveis_preditoras, retornos_futuros):
    # Adiciona a coluna de "ones" para o termo constante
    variaveis_preditoras['const'] = 1

    # Ajusta as dimensões dos dados
    X = variaveis_preditoras.values.reshape(-1, 1)  # Se necessário, ajuste a dimensão de X conforme necessário
    y = retornos_futuros.values.reshape(-1, 1)  # Se necessário, ajuste a dimensão de y conforme necessário

    # Calcula as previsões
    previsoes = modelo.predict(X)

    # Plota as previsões
    plt.figure(figsize=(12, 6))
    plt.plot(retornos_futuros.index, retornos_futuros, label='Retornos Futuros Reais', color='blue')
    plt.plot(retornos_futuros.index, previsoes, label='Previsões do Modelo', color='red', linestyle='--')
    plt.title('Previsões de Retornos Futuros')
    plt.xlabel('Data')
    plt.ylabel('Retorno')
    plt.legend()
    plt.show()

# Lista de tickers dos ativos brasileiros
tickers_brasileiros = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "B3SA3.SA", "PETR3.SA", "ABEV3.SA", "BBAS3.SA", "SANB11.SA", "ITSA4.SA"]

# Período de tempo desejado
start_date = "2023-01-01"
end_date = "2023-12-31"

# Obter retornos
retornos_ativos_brasileiros = obter_retornos(tickers_brasileiros, start_date, end_date)

# Criar variáveis preditoras
variaveis_preditoras = criar_variaveis_preditoras(retornos_ativos_brasileiros, janela=5)

# Obter os retornos futuros (pode ajustar o período de previsão)
retornos_futuros = retornos_ativos_brasileiros.iloc[-1]

# Treinar o modelo
modelo = treinar_modelo(variaveis_preditoras, retornos_futuros)

# Plotar as previsões
plotar_previsoes(modelo, variaveis_preditoras, retornos_futuros)
