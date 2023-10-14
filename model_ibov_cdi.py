import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk
import yfinance as yf
from bcb import sgs
import matplotlib.ticker as tick

# Configurando o estilo do gráfico para o estilo "cyberpunk"
plt.style.use("cyberpunk")

# Lista de tickers dos ativos brasileiros
tickers_brasileiros = ["PETR4.SA", 
                       "VALE3.SA", 
                       "ITUB4.SA", 
                       "BBDC4.SA", 
                       "B3SA3.SA", 
                       "PETR3.SA", 
                       "ABEV3.SA", 
                       "BBAS3.SA", 
                       "SANB11.SA", 
                       "ITSA4.SA"]

# Datas de início e fim para download de dados
start_date = "1994-06-01"
end_date = "2023-01-01"

# Dicionário para armazenar os dados dos ativos
ativos_data = {}

# Baixar dados para cada ativo individualmente
for ticker in tickers_brasileiros:
    ativo = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
    ativos_data[ticker] = ativo

# Baixar dados do CDI (Certificado de Depósito Interbancário)
cdi_data = sgs.get({"cdi":11}, start=start_date)
cdi_data = cdi_data["cdi"]
cdi_returns = cdi_data/100
cdi_cumulative_return = (1 + cdi_returns).cumprod() 

# Baixar dados do Ibovespa
ibov = yf.download("^BVSP", start=start_date)["Adj Close"]
ibov.index = (pd.to_datetime(ibov.index))
ibov = ibov.sort_index(ascending=True)

# Calcular os valores finais do mês para Ibov e CDI
final_mes_ibov = ibov.resample("M").last()
final_mes_cdi = cdi_cumulative_return.resample("M").last()

# Calcular os valores iniciais do mês para Ibov e CDI
inicio_mes_ibov = ibov.resample("M").first()
inicio_mes_cdi = cdi_cumulative_return.resample("M").first()

# Calcular os retornos mensais para Ibov e CDI
retorno_final_mes_ibov = final_mes_ibov.pct_change(periods=1).dropna()
retorno_final_mes_cdi = final_mes_cdi.pct_change(periods=1).dropna()
retorno_inicio_mes_ibov = inicio_mes_ibov.pct_change(periods=1).dropna()
retorno_inicio_mes_cdi = inicio_mes_cdi.pct_change(periods=1).dropna()

# Selecionar apenas os retornos iniciais que ocorrem após os retornos finais
retorno_inicio_mes_ibov = retorno_inicio_mes_ibov[retorno_inicio_mes_ibov.index > retorno_final_mes_ibov.index[1]]
retorno_inicio_mes_cdi = retorno_inicio_mes_cdi[retorno_inicio_mes_cdi.index > retorno_final_mes_cdi.index[1]]

# Criar DataFrame para armazenar os retornos
df_retornos = pd.DataFrame(columns=["Estratégia", "Ibov", "CDI"], index=retorno_final_mes_cdi.index)

# Loop para calcular os retornos da estratégia
for i, data in enumerate(retorno_final_mes_cdi.index): 

    if i < (len(retorno_final_mes_cdi.index) - 2):

        retorno_cdi_last_month = retorno_final_mes_cdi.loc[data]
        retorno_ibov_last_month = retorno_final_mes_ibov.loc[data]
        retorno_ibov_mes_seguinte = retorno_inicio_mes_ibov.iloc[i]
        retorno_cdi_mes_seguinte = retorno_inicio_mes_cdi.iloc[i]

        if retorno_cdi_last_month > retorno_ibov_last_month:

            retorno_estrategia = retorno_cdi_mes_seguinte

        else:

            retorno_estrategia = retorno_ibov_mes_seguinte

        df_retornos.loc[data, "Estratégia"] = retorno_estrategia
        df_retornos.loc[data, "Ibov"] = retorno_ibov_mes_seguinte
        df_retornos.loc[data, "CDI"] = retorno_cdi_mes_seguinte

# Shift nos retornos para alinhar com o mês seguinte
df_retornos = df_retornos.shift(1)
df_retornos = df_retornos.dropna()

# Calcular o retorno acumulado
df_acum = (1 + df_retornos).cumprod() - 1

# Multiplicar por 1000 para facilitar a visualização
df_acum = df_acum * 1000

# Renomear as colunas
df_acum.columns = ["MODELO", "IBOV", "CDI"]

# Plotar o gráfico
ax = df_acum.plot()
ax.yaxis.set_major_formatter(tick.StrMethodFormatter("R${x:,.0f}"))
plt.legend()

# Configurar a formatação do eixo y como moeda (R$)
plt.grid(0)
plt.savefig("mtum.png", dpi=300)
plt.show()

# Criar DataFrame com os dados baixados
ativos_df = pd.DataFrame(ativos_data)

# Calcular os retornos mensais para cada ativo brasileiro
returns_ativos_brasileiros = ativos_df.pct_change().resample("M").ffill()

# Encontrar os ativos mais rentáveis por mês
ativos_mais_rentaveis = returns_ativos_brasileiros.idxmax(axis=1)

# Criar DataFrame para armazenar os resultados
df_ativos_mais_rentaveis = pd.DataFrame(ativos_mais_rentaveis, columns=['Ativo Mais Rentável'])

# Salvar os resultados em uma planilha Excel
df_ativos_mais_rentaveis.to_excel("ativos_mais_rentaveis_por_mes.xlsx")