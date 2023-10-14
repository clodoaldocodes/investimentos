import yfinance as yf
import matplotlib.pyplot as plt

# Escolha os tickers das ações desejadas
ticker1 = "PETR4.SA"
ticker2 = "VALE3.SA"

# Datas de início e fim para download de dados
start_date = "1994-06-01"
end_date = "2023-01-01"

# Baixar dados históricos para ambas as ações
dados_acao1 = yf.download(ticker1, start=start_date, end=end_date)["Adj Close"]
dados_acao2 = yf.download(ticker2, start=start_date, end=end_date)["Adj Close"]

# Calcular os retornos diários para ambas as ações
retorno_diario1 = dados_acao1.pct_change().dropna()
retorno_diario2 = dados_acao2.pct_change().dropna()

# Calcular o retorno acumulado para ambas as ações
retorno_acumulado1 = (1 + retorno_diario1).cumprod() - 1
retorno_acumulado2 = (1 + retorno_diario2).cumprod() - 1

# Plotar a rentabilidade ao longo do tempo para ambas as ações
plt.figure(figsize=(10, 6))
plt.plot(retorno_acumulado1.index, retorno_acumulado1, label=ticker1)
plt.plot(retorno_acumulado2.index, retorno_acumulado2, label=ticker2)
plt.title("Rentabilidade Acumulada de Duas Ações")
plt.xlabel("Data")
plt.ylabel("Retorno Acumulado")
plt.legend()
plt.grid(True)
plt.show()
