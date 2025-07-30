import requests
import os
import time
from dotenv import load_dotenv
load_dotenv()
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")

#------------------------------------------------------------------------------#
#----------------------------------API CALLS-----------------------------------#
#------------------------------------------------------------------------------#

# Globale Variablen
cashflow_data = income_data = overview_data = balance_data = global_data = fred_data = None
market_cap = beta = d = z = r_f = r_d = net_debt = shares_outstanding = current_stock_price = currency = None

# init_data damit Ticker Symbol dynamisch übergeben werden kann
def init_data(ticker_symbol):
    global cashflow_data, income_data, overview_data, balance_data, global_data, fred_data
    global market_cap, beta, d, z, r_f, r_d, net_debt, shares_outstanding, current_stock_price, currency

    def get_api_data(api):
        r = requests.get(api)
        data = r.json()
        if "Note" in data or data is None:
            raise Exception(f"Fehlerhafte API-Antwort: {data}")
        return data

    cashflow = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker_symbol}&apikey={ALPHA_API_KEY}'
    income_statement = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker_symbol}&apikey={ALPHA_API_KEY}'
    overview = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker_symbol}&apikey={ALPHA_API_KEY}'
    balance_sheet = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker_symbol}&apikey={ALPHA_API_KEY}'
    global_quote = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker_symbol}&apikey={ALPHA_API_KEY}'
    fred = f'https://api.stlouisfed.org/fred/series/observations?series_id=GS10&api_key={FRED_API_KEY}&file_type=json'

    cashflow_data = get_api_data(cashflow)['annualReports']
    time.sleep(20)
    income_data = get_api_data(income_statement)['annualReports']
    time.sleep(20)
    overview_data = get_api_data(overview)
    time.sleep(20)
    balance_data = get_api_data(balance_sheet)['annualReports']
    time.sleep(20)
    global_data = get_api_data(global_quote)['Global Quote']
    fred_data = get_api_data(fred)

#------------------------------------------------------------------------------#
#------------------------------GLOBALE VARIABLEN-------------------------------#
#------------------------------------------------------------------------------#
   
    market_cap = float(overview_data['MarketCapitalization'])
    beta = float(overview_data['Beta'])
    d = float(balance_data[0]['shortLongTermDebtTotal'])
    z = float(income_data[0]['interestExpense'])
    r_f = float(fred_data['observations'][-1]['value']) / 100
    r_d = z / d if d != 0 else 0
    net_debt = d - float(balance_data[0]['cashAndCashEquivalentsAtCarryingValue'])
    shares_outstanding = float(overview_data['SharesOutstanding'])
    current_stock_price = float(global_data['05. price'])
    currency = overview_data['Currency']

#------------------------------------------------------------------------------#
#------------------------DATEN MIGRATION & BERECHNUNGEN------------------------#
#------------------------------------------------------------------------------#

def get_last_fcf(n):
    return [
        float(i["operatingCashflow"]) - float(i["capitalExpenditures"])
        for i in cashflow_data[:n]
    ]

def calculate_annual_growth(fcf_list, n):
    return [
        (fcf_list[i] - fcf_list[i + 1]) / fcf_list[i + 1]
        for i in range(len(fcf_list) - 1)
    ] 

def calculate_cagr(fcf_list, n): 
    return ((fcf_list[0] / fcf_list[-1]) ** (1 / n)) - 1

def get_tot_rev(n):
    return [
        float(i['totalRevenue'])
    for i in income_data[:n]
    ]

def calculate_fcf_margin(n):
    return [
        get_last_fcf(n)[i] / get_tot_rev(n)[i]
    for i in range(n)
    ]

def calculate_average_rev(fcf_margin, n): 
    return sum(fcf_margin) / n

def calculate_future_fcf(current_fcf, cagr, years): 
    return current_fcf * (1 + cagr) ** years

def calculate_capm(r_m):
    return r_f + beta * (r_m - r_f)

def calculate_wacc(capm, t):
    return (market_cap / (market_cap + d)) * capm + (d / (market_cap + d)) * r_d * (1 - t)

def calculate_tv(future_fcf, g, wacc):
    return (future_fcf * (1 + g)) / (wacc - g)

def calculate_b_tv (terminal_value, wacc, prediction_y):
    return (terminal_value / ((1 + wacc) ** prediction_y))

def dis_fcf(current_fcf, cagr, prediction_y, wacc):
    return [
        calculate_future_fcf(current_fcf, cagr, i) / ((1 + wacc) ** i)
        for i in range(1, prediction_y + 1)
    ]

def calculate_enterprise_value(dis_fcf, b_terminal_value):
    return sum(dis_fcf) + b_terminal_value