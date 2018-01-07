'''
Created on Oct 31, 2017

@author: Felix
'''
from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt
import os as os

class Security():
    '''
    Security classes contains raw data from excel sheets 
    '''

    def __init__(self,name,worksheetID,filename):
        '''
        Constructor
        '''
        print('reading data from'+os.getcwd() + '\\'+filename)
        self.data = pd.read_excel(os.getcwd() + '\\'+filename,sheetname=worksheetID,index_col=0,na_values = 'null' )
        self.data = self.data.fillna(method = 'ffill')
        #self.ID   = (str.split(name,'.'))[0]
        separator = '_'
        self.ID   = separator.join(str.split(name,' '))
        
    def getreIndexedData(self,daterange,TagName):
        curData = self.data.ix[:,TagName]
        curData = curData.reindex(daterange)
        
        return self.checkDataForNANs(curData)
        
    def checkDataForNANs(self,data):
        
        if data.__len__() != sum(data.notnull()):
            print('have to fill data! found ' +str(sum(data.isnull())) +' entries which have to be filled!')
            
            assert(sum(data.isnull())/float(data.__len__()) <= 0.1)
            
        data = data.fillna(method='bfill')
        if data.__len__() != sum(data.notnull()):
            data = data.fillna(method='ffill') 
    
        return data
    
    def plotData(self,TagName,startdate,enddate):
        dateRange   = pd.date_range(start=startdate, end=enddate, freq='B')
        
        curData     = self.getreIndexedData(dateRange, TagName)
        
        short_rolling = curData.rolling(window=20).mean()
        long_rolling = curData.rolling(window=100).mean()
        
        # Plot everything by leveraging the very powerful matplotlib package
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.plot(curData.index, curData, label=self.ID)
        ax.plot(short_rolling.index, short_rolling, label='20 days rolling')
        ax.plot(long_rolling.index, long_rolling, label='100 days rolling')
        ax.set_xlabel('Date')
        ax.set_ylabel('Adjusted closing price (Euro)')
        ax.legend()
        plt.show()