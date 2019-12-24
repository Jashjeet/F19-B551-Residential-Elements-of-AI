# -- coding: utf-8 --
# Authors: DEVANSH JAIN - devajain
#           SANYAM RAJPAL - srajpal
#           JASHJEET SINGH MADAN - jsmadan

import pandas as pd
import numpy as np

class KNN(object):
    def __init__(self,k):
        self.k=k
        
    def predict(self,train,test):
        X_train=train.drop(columns=[0,1],axis=1)
        y_train=train[1]     
        
        X_train=X_train.to_numpy()
        y_train=y_train.to_numpy()
            
        ypred=[]
        
        for i in range(len(test)):
            
            temp=test[i]
            a=temp-X_train
            b=a*a
            c=np.sum(b,axis=1)
            d=np.argsort(c)[0:self.k]
            e=y_train[d]
            f=list(e)
            g=max(set(f), key=f.count)            
            ypred.append(g)
        return(ypred)    
