import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import mplcyberpunk

# Configurando o estilo do gráfico para o estilo "cyberpunk"
plt.style.use("cyberpunk")

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
        retornos[ticker] = data["Adj Close"].pct_change()

    return retornos

def plotar_top3_retaveis(retornos, top_n=3):
    """
    Plota um gráfico dos top N ativos mais rentáveis.

    Args:
        retornos (DataFrame): DataFrame contendo os retornos percentuais dos ativos.
        top_n (int): Número de ativos mais rentáveis a serem exibidos no gráfico.
    """
    # Calcular a rentabilidade total para cada ativo
    rentabilidade_total = (1 + retornos).cumprod() - 1

    # Selecionar os top N ativos mais rentáveis
    top_n_ativos = rentabilidade_total.iloc[-1].sort_values(ascending=False).head(top_n).index

    # Plotar os retornos acumulados dos top N ativos
    plt.figure(figsize=(12, 6))
    for ticker in top_n_ativos:
        plt.plot(rentabilidade_total.index, rentabilidade_total[ticker], label=ticker)

    plt.title(f"Top {top_n} Ativos Mais Rentáveis")
    plt.xlabel("Data")
    plt.ylabel("Retorno Acumulado")
    plt.legend()
    plt.show()

# Lista de tickers dos ativos brasileiros
tickers_brasileiros = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "B3SA3.SA", "PETR3.SA", "ABEV3.SA", "BBAS3.SA", "SANB11.SA", "ITSA4.SA"]

# Período de tempo desejado
start_date = "2023-09-01"
end_date = "2023-10-14"

# Obter retornos
retornos_ativos_brasileiros = obter_retornos(tickers_brasileiros, start_date, end_date)

# Plotar top 3 ativos mais rentáveis
plotar_top3_retaveis(retornos_ativos_brasileiros, top_n=3)
