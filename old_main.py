import requests
import pandas
import numpy
import os
from dotenv import load_dotenv
load_dotenv()
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")

#------------------------------------------------------------------------------#
#----------------------------------API CALLS-----------------------------------#
#------------------------------------------------------------------------------#

cashflow = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey={ALPHA_API_KEY}'# symbol=TickerSymbol
r = requests.get(cashflow)
data1 = r.json()
annual_reports1 = data1['annualReports']

income_statement = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey={ALPHA_API_KEY}'
t = requests.get(income_statement)
data2 = t.json()
annual_reports2 = data2['annualReports']

overview = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey={ALPHA_API_KEY}'
z = requests.get(overview)
data3 = z.json()

balance_sheet = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey={ALPHA_API_KEY}'
u = requests.get(balance_sheet)
data4 = u.json() 

FRED = f'https://api.stlouisfed.org/fred/series/observations?series_id=GS10&api_key={FRED_API_KEY}&file_type=json'
p = requests.get(FRED)
data5 = p.json()
latest_observation = data5['observations'][-1]

#------------------------------------------------------------------------------#
#----------------------------------VARIABLEN-----------------------------------#
#------------------------------------------------------------------------------#

market_cap = data3['MarketCapitalization'] # Marktkapitalisierung
beta = data3['Beta']
D = data4['shortLongTermDebtTotal'] # Fremdkapital
g = 0.02 # Langfristige Inflation + stabiles Wachstum (Muss selber festgelegt werden)
rm = 0.08 # Erwartete Marktrendite (Muss selber geschätzt werden)
rf = float(latest_observation["value"]) / 100 # Risikofreier Zinssatz
years_traceback = 10
n = 9
prediction_y = 3

#------------------------------------------------------------------------------#
#------------------------DATEN MIGRATION & BERECHNUNGEN------------------------#
#------------------------------------------------------------------------------#

last_fcf = [
        float(i["operatingCashflow"]) - float(i["capitalExpenditures"])
    for i in annual_reports1[:years_traceback]
]
annual_growth = [
       ((last_fcf[i]-last_fcf[i+1])/last_fcf[i+1])
    for i in range(n)
]

CAGR = ((last_fcf[0]/last_fcf[n])**(1/n))-1

last_tot_rev = [
        float(i["totalRevenue"])
    for i in annual_reports2[:years_traceback]
]

fcf_margin = [
    last_fcf[i]/last_tot_rev[i]
    for i in range(years_traceback)
]

average_rev = sum(fcf_margin)/years_traceback

future_fcf = last_fcf[0] * (1+CAGR) ** prediction_y
print(average_rev)
print(future_fcf)



