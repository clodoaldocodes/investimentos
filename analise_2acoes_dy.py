import yfinance as yf
import matplotlib.pyplot as plt
import mplcyberpunk

# Configurando o estilo do gráfico para o estilo "cyberpunk"
plt.style.use("cyberpunk")

# Escolha os tickers das ações desejadas
ticker1 = "PETR4.SA"
ticker2 = "VALE3.SA"

# Datas de início e fim para download de dados
start_date = "1994-06-01"
end_date = "2023-01-01"

# Baixar dados históricos para ambas as ações
dados_acao1 = yf.download(ticker1, start=start_date, end=end_date)
dados_acao2 = yf.download(ticker2, start=start_date, end=end_date)

# Verificar se há dados na coluna 'Dividends' para ambas as ações
if 'Dividends' in dados_acao1.columns and 'Dividends' in dados_acao2.columns:
    # Calcular o Dividend Yield para ambas as ações
    dy1 = (dados_acao1['Dividends'] / dados_acao1['Close']).dropna()
    dy2 = (dados_acao2['Dividends'] / dados_acao2['Close']).dropna()

    # Imprimir os primeiros registros dos DataFrames para verificação
    print("Dados de", ticker1)
    print(dados_acao1.head())

    print("\nDados de", ticker2)
    print(dados_acao2.head())

    # Plotar o Dividend Yield ao longo do tempo para ambas as ações
    plt.figure(figsize=(10, 6))
    if not dy1.empty:
        plt.plot(dy1.index, dy1, label=f'{ticker1} DY')
    if not dy2.empty:
        plt.plot(dy2.index, dy2, label=f'{ticker2} DY')

    plt.title('Dividend Yield de Duas Ações ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Dividend Yield')
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print("Não há dados de dividendos para ambas as ações.")
