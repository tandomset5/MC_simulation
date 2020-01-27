import json
import numpy as np
import scipy.stats as ss
from yahoofinancials import YahooFinancials


def historical_price_list(ticker, start_date, end_date, frequency, col_name):
    yahoo_financials = YahooFinancials(ticker)
    yfdata = json.loads(json.dumps(yahoo_financials.get_historical_price_data(start_date, end_date, frequency)))
    col_list = []
    if len(yfdata[ticker]['prices']) > 0:
        for i in range(len(yfdata[ticker]['prices'])):
            if yfdata[ticker]['prices'][i][col_name] != None:
                col_list.append(yfdata[ticker]['prices'][i][col_name])
    return col_list

def percent_change_list(price_list = []):
    calculated_list = []
    for i in range(len(price_list)):
        if len(price_list)>i+1:
            if price_list[i] == 0:
                calculated_list.append(0)
            else:
                calculated_list.append((price_list[i+1]-price_list[i])/price_list[i])
    return calculated_list

n=12
simulation_list = []
price_data = np.array(percent_change_list(historical_price_list('VFINX','1950-01-01','1990-05-01','monthly','close')))
mu = np.average(price_data)
sigma = np.std(price_data)



for i in range(100000):
    simulation_list.append(sum(np.random.normal(mu,sigma,n)))

sim_mu = np.average(simulation_list)
sim_sigma = np.std(simulation_list)
    

print('n: ' + str(n)) 
print('Original Data Average: ' + str(mu))
print('Original Data Standard Devidation: ' + str(sigma))

print('Simulated Data Average After ' + str(n) + ' months: ' + str(sim_mu))
print('Simulated Data Standard Devidation After ' + str(n) + ' months: ' + str(sim_sigma))
print('Probability: ' + str((1-ss.norm.cdf(0.07,sim_mu,sim_sigma))*100) + '%')


