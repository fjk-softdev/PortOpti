'''
Created on 12.11.2017

@author: Felix
'''
import Covariance as Covariance
import Optimization as Optimization
import pandas as pd
import numpy as np

class Portfolio():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        print('creating portfolio')
        
        self.securityList = []
        self.obj_covariance  = []
        self.excelOuputFile = 'efficientFrontier.xls'
        
    def addSecurity2Portfolio(self,security):
        if type(security).__name__ != 'Security':
            print('addSecurity only takes securities as input!')
            return
        
        self.securityList.append(security)
    
            
    def determineCovarianceMatrix(self,startDate,endDate,fluctuationmode,):
        if len(self.securityList) > 0:
            covariance = Covariance.Covariance(self.securityList,fluctuationmode,startDate,endDate)
            self.driftDF,self.covarianceDF = covariance.getPooledCovariance()
            
            print('    determined covariance matrix of securities in portfolio')
        else:
            print('no securities in portfolio. cant determine anything')
        
    def getRiskoptimum(self,startDate,endDate,minimumReturn,fluctuationmode):
        
        if sum([hasattr(self, 'covarianceDF'),hasattr(self, 'driftDF')]) != 2:
            self.determineCovarianceMatrix(startDate, endDate, fluctuationmode)
        
        opti    = Optimization.Optimization((self.driftDF.as_matrix()).flatten(),self.covarianceDF.as_matrix(),minimumReturn)
        result,mu,var = opti.doOptimization()
        
        #annualize
        if fluctuationmode ==  'geometric':
            mu = np.exp(mu*365.25)-1
            sigma = np.exp(np.sqrt(var*365.25)) -1
            
        else:
            mu = (mu*365.25) -1
            sigma = np.sqrt(var*365.25)-1
        
        return result,mu,sigma 
        
    def getEfficientFrontier(self,startDate,endDate,fluctuationmode):
        # will only get useful solutions.. thus no "markowitz bullet" like stuff. always use constraint that return(solution) > requestedReturn, not equal!
        
        self.determineCovarianceMatrix(startDate, endDate, fluctuationmode)
        #define bins
        drift   = self.driftDF.as_matrix()
        maximum = drift.max()
        minimum = drift.min()
        
        nsteps = 100
        stepsize = (maximum-minimum)/float(nsteps)
        output = []
        for i in range(nsteps):
            minimumReturn = (stepsize * i + minimum)
            result,mu,var = self.getRiskoptimum(startDate, endDate, minimumReturn, fluctuationmode)
            resAsList   = list(result)
            resAsList.append(mu)
            resAsList.append(var)
            output.append(resAsList)
            
        columns = [etf.ID for etf in self.securityList]
        columns.append('mu')
        columns.append('var')
        self.efficientFrontier = pd.DataFrame(data = output,index = range(nsteps),columns = columns)
        
    def dumpEfficientFrontiertoExcel(self):

        writer = pd.ExcelWriter(self.excelOuputFile)
        
        self.efficientFrontier.to_excel(writer, "efficientFrontier")
        writer.save()
        writer.close()    
        
        
        