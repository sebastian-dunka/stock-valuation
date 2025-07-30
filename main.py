import functions

ticker_symbol = "IBM"
functions.init_data(ticker_symbol)

n = 9   # Wieviel Jahre sollen Betrachtet werden (Bsp.: n = 9 die letzten 10 Werte)
prediction_y = 3   # Wieivel Jahre wir in die Zukunft schauen wollen
g = 0.02 # Langfristige Inflation + stabiles Wachstum (Muss selber festgelegt werden)
r_m = 0.08 # Erwartete Marktrendite (Muss selber geschätzt werden)
t = 0.21 # Steuersatz T (aktuell für US Unternehmen) könnte auch berechnet werden ist aber oft besser anzunhemen


last_fcf = functions.get_last_fcf(n)
annual_growth = functions.calculate_annual_growth(last_fcf, n)
cagr = functions.calculate_cagr(last_fcf, n)
tot_rev = functions.get_tot_rev(n)
fcf_margin = functions.calculate_fcf_margin(n)
average_rev = functions.calculate_average_rev(fcf_margin, n)
current_fcf = float(last_fcf [0])
future_fcf = functions.calculate_future_fcf(current_fcf, cagr , prediction_y)
capm = functions.calculate_capm(r_m)
wacc = functions.calculate_wacc(capm, t)
terminal_value = functions.calculate_tv(future_fcf, g , wacc)
b_terminal_value = functions.calculate_b_tv(terminal_value, wacc, prediction_y)
dis_fcf = functions.dis_fcf(last_fcf[0], cagr, prediction_y, wacc)
enterprise_value = functions.calculate_enterprise_value(dis_fcf, b_terminal_value)
equity_value = enterprise_value - functions.net_debt
stock_price = equity_value / functions.shares_outstanding
current_stock_price = functions.current_stock_price
currency = functions.currency

if stock_price > current_stock_price:
    print(f"The share is undervalued and should be worth {stock_price} {currency} in {prediction_y} years.")
elif stock_price < current_stock_price:
    print(f"The share is overvalued and should be worth {stock_price} {currency} in {prediction_y} years.")
else:
    print("The share is fairly valued.")