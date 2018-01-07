'''
Created on 14.11.2017

@author: Felix
'''
import numpy as np
from scipy.optimize import minimize


class Optimization():
    '''
    optimization class
    '''


    def __init__(self,driftVector,covarianceMatrix,minReturn):
        '''
        Constructor for optimization. using least square
        '''
        self.covarianceMatrix   = covarianceMatrix
        self.rowCount           = len(covarianceMatrix)
        
        self.driftVector        = driftVector
        
        if minReturn == None:
            self.minReturn = 0
        else:
            self.minReturn = minReturn
        
        self.constraints = ({'type': 'eq','fun' : lambda x: np.array([sum(x)-1])},{'type': 'ineq','fun': lambda x: np.array(self.returnFunction(x)-minReturn)})
        self.bounds  = tuple([(0,1) for i in range(self.rowCount)])
    
    def doOptimization(self):
        res = minimize(self.objectiveFunction,np.ones(self.rowCount)/float(self.rowCount), args=(+1.0,), jac=self.objectiveFuncDerivative,constraints=self.constraints,bounds=self.bounds,
                        method='SLSQP',tol=1e-15)
               
        self.checkConstraints(res.x, self.minReturn)
        return res.x,self.returnFunction(res.x),self.objectiveFunction(res.x,1)
    
    def returnFunction(self,x):
        return np.inner(x,self.driftVector)
        
    def objectiveFunction(self,x,sign = 1.0):
        # objective function xTAx
        return sign*np.dot(np.transpose(x),np.dot(self.covarianceMatrix,x))
    
    def objectiveFuncDerivative(self,x,sign = 1.0):
        # derivative of objective function 
        return sign*np.dot(2*self.covarianceMatrix,x)
    
    def checkConstraints(self,x,minreturn):
        # loop over constraints:
        for con in self.constraints:
            if con['type'] == 'eq':
                assert(con['fun'](x) >= -0.000001)
                
            else:
                assert(con['fun'](x) +minreturn >= 0.000001)
