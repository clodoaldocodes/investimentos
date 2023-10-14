import yfinance as yf
import matplotlib.pyplot as plt
import mplcyberpunk

# Configurando o estilo do gráfico para o estilo "cyberpunk"
plt.style.use("cyberpunk")

# Escolha o ticker da ação desejada
ticker = "PETR4.SA"  # Exemplo com ação da Apple, mas você pode substituir pelo ticker desejado

# Datas de início e fim para download de dados
start_date = "1994-06-01"
end_date = "2023-01-01"

# Baixar dados históricos
dados_acao = yf.download(ticker, start=start_date, end=end_date)["Adj Close"]

# Calcular os retornos diários
retorno_diario = dados_acao.pct_change().dropna()

# Calcular o retorno acumulado
retorno_acumulado = (1 + retorno_diario).cumprod() - 1

# Plotar a rentabilidade ao longo do tempo
plt.figure(figsize=(10, 6))
plt.plot(retorno_acumulado.index, retorno_acumulado, label=ticker)
plt.title(f"Rentabilidade Acumulada de {ticker}")
plt.xlabel("Data")
plt.ylabel("Retorno Acumulado")
plt.legend()
plt.grid(True)
plt.show()
