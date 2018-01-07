'''
Created on 11.10.2017

@author: Felix
'''
from pandas_datareader import data
from pandas import DataFrame, read_csv
import pandas as pd
import matplotlib.pyplot as plt

import Security as Security
import Portfolio as Portfolio


# -------------------------------

startDate = '01/01/2013'
endDate   = '10/13/2017'

EuropeSmallCapETF = Security.Security('EuropeSmallCap','SXRJ.DE','MSCI EuropeSmallCap.xls')

JapanETF = Security.Security('MSCI Japan','DBXJ.F','MSCI Japan.xls')

LatinAmericaETF = Security.Security('MSCI LatinAmerica','LYM0.F','MSCI LatinAmerica.xls')

AfricaETF = Security.Security('MSCI AfricaTOP50','XMKA.DE','MSCI Africa TOP 50.xls')

DaxETF = Security.Security('DekaDax','EL4A.DE','Deka Dax.xls')

AsiaETF = Security.Security('MSCI AsiaEXJapan','DXS5.DE','DBXT MSCI Asia ex Japan.xls')

EuroStoxxETF = Security.Security('EuroStoxx50','DBXE.DE','DBXT Euro Stoxx 50.xls')

WorldETF = Security.Security('MSCI World','EUNL.DE','iShares Core MSCI World.xls')

# add securities to portfolio
etfPortfolio = Portfolio.Portfolio()


#etfPortfolio.addSecurity2Portfolio(EuropeSmallCapETF)
#etfPortfolio.addSecurity2Portfolio(JapanETF)
#etfPortfolio.addSecurity2Portfolio(LatinAmericaETF)
etfPortfolio.addSecurity2Portfolio(AfricaETF)
etfPortfolio.addSecurity2Portfolio(DaxETF)
etfPortfolio.addSecurity2Portfolio(AsiaETF)
#etfPortfolio.addSecurity2Portfolio(EuroStoxxETF)
etfPortfolio.addSecurity2Portfolio(WorldETF)

etfPortfolio.getEfficientFrontier(startDate,endDate,fluctuationmode='geometric')
etfPortfolio.dumpEfficientFrontiertoExcel()

