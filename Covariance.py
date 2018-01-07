'''
Created on Oct 31, 2017

@author: Felix
'''
import numpy as np
import pandas as pd
from scipy.stats import norm

class Covariance():
    '''
    uses Security data and determines covariance matrix
    '''

    def __init__(self,ETFList,fluctuationMode,startdate,enddate):
        '''
        Constructor
        '''
        self.startdate = startdate
        self.enddate = enddate
        
        # set etfs
        self.ETFList = ETFList
        
        # set fluctuation mode
        self.fluctuationmode = self.setfluctuationmode(fluctuationMode)
        
        # define calcfunction dictionary
        self.defineCalcFunction()
        
    def setfluctuationmode(self,mode):
        if mode == 'geometric' or mode == 'linear':
            print('    chosen mode is ' + mode)
            return mode
        else:
            print('can not handle other modes than geometric or linear')
  
    def defineCalcFunction(self):
        self.funcDict= {
            'linear' : lambda x,y : x-y,
            'geometric' : lambda x,y : np.log(x/y)
            }
    
    def getPooledCovariance(self):
        frequencymodes = ['W-MON','W-TUE','W-WED','W-THU','W-FRI']
        normalize = float(frequencymodes.__len__())
        # get row and column number for matrix
        columnNumber = rowNumber = self.ETFList.__len__()
        dummyMatrixCorr = np.matrix([[0 for i in range(columnNumber)] for i in range(rowNumber)],dtype = float)
        dummyMatrixCov = np.matrix([[0 for i in range(columnNumber)] for i in range(rowNumber)],dtype = float)
        
        dummyReturnVector = np.matrix([0 for i in range(columnNumber)],dtype = float) 
        
        # loop over time grids
        for freq in frequencymodes:
            curCorr,curCov,drift = self.determineCovariance(freq)
            dummyMatrixCorr += curCorr.as_matrix() 
            dummyMatrixCov  += curCov.as_matrix()
            dummyReturnVector += drift.as_matrix()
            
        self.correlationFrame  = pd.DataFrame(data = dummyMatrixCorr/normalize,columns = [etf.ID for etf in self.ETFList],index = [etf.ID for etf in self.ETFList])
        self.covarianceFrame   = pd.DataFrame(data = dummyMatrixCov/normalize,columns = [etf.ID for etf in self.ETFList],index = [etf.ID for etf in self.ETFList])
        self.ReturnFrame       = pd.DataFrame(data = dummyReturnVector/normalize,columns = [etf.ID for etf in self.ETFList],index = ['mu'])
        
        print('    pooled correlation matrix: ')
        print(self.correlationFrame)
        
        print('    pooled covariance matrix: ')
        print(self.covarianceFrame)
        
        print('    return vector:')
        print(self.ReturnFrame)
        
        
        return self.ReturnFrame,self.covarianceFrame
    
    def determineCovariance(self,timeFrequencyMode):
        # keep in mind output is like correlationMatrix,covarianceMatrix
        
        # inits
        if timeFrequencyMode == None : timeFrequencyMode = 'B'
        timeGrid = pd.date_range(self.startdate,self.enddate,freq = timeFrequencyMode)
        
        Returns = pd.DataFrame(data = [] )
        data2 = []
        
        for etf in self.ETFList:
            curData = etf.getreIndexedData(timeGrid,'Adj Close')
            logret,mu,statVar = self.getDriftMeanAndVariance(curData)
            
            Returns = pd.concat([Returns, logret.rename(etf.ID)], axis=1)
            data2.append(mu)
        
        drift = pd.DataFrame(data = [data2],index = ['mu'],columns = [etf.ID for etf in self.ETFList])
        
        correlationMatrix  = Returns.corr('pearson')
        covarianceMatrix   = Returns.cov()
        
        return correlationMatrix,covarianceMatrix,drift
        
    def getDriftMeanAndVariance(self,data):
        Stk = data[1:-1]
        StkMin1 = data[0:-2]
        
        tk   = Stk.index
        tkMin1 = StkMin1.index
        
        deltas = (tk-tkMin1).days
        returnData  = []
        
        for i in np.arange(Stk.__len__()):
            # sophisticated function call to linear or geometric fluctuation mode
            returnData.append(self.funcDict[self.fluctuationmode](Stk[i],StkMin1[i])/float(deltas[i]))
            
        logreturns = np.array(returnData)
        mean = logreturns.mean()
        statVar = logreturns.var(ddof = 1) # need ddof = 1 for unbiased estimator of variance 1/n-1 !
        
        # test results for normal distribution using kolmogorov smirnov
        self.checkforNormalDistribution(logreturns,mean,statVar)
        
        if self.fluctuationmode == 'geometric': mu = mean + 1/2 * statVar
        else : mu = mean
        
        returns = pd.Series(data = logreturns, index = tk)
        return returns,mu,statVar
    
    def checkforNormalDistribution(self,returns,mean,variance):
        # required confidence level is 99.9%
        
        #empirical data
        normalizedReturns = (returns-mean)/np.sqrt(variance)
        H,X1 = np.histogram( normalizedReturns, bins = 100, normed = True )
        dx = X1[1] - X1[0]
        F1 = np.cumsum(H)*dx
        
        # cumulative normal distri
        normalCDF = norm.cdf(X1[1:])
        diffMaxUp    = max(abs(F1 - normalCDF))
        diffMaxDown  = max(abs(F1[0:-2]-normalCDF[1:-1]))
        completeMax = max([diffMaxUp,diffMaxDown])
        
        print(completeMax*np.sqrt(returns.__len__()))
        #assert(completeMax*np.sqrt(returns.__len__()) > 1.358)
        
        