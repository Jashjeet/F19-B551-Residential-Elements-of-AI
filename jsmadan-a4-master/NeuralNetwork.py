# -*- coding: utf-8 -*-
# Authors: DEVANSH JAIN - devajain
#           SANYAM RAJPAL - srajpal
#           JASHJEET SINGH MADAN - jsmadan


import numpy as np
import pandas as pd
np.random.seed(0)
import pickle

class NeuralNetwork(object):    
    def __init__(self, epochs, learning_rate, rho):
        self.epochs=epochs
        self.learning_rate=learning_rate
        self.rho=rho
        self.weight1=0
        self.weight2=0
        self.weight3=0
        self.bias1=0
        self.bias2=0
        self.bias3=0
    
    def relu(self,hx):
        return (np.maximum(hx, 0))
    
    def relu_derivative(self,hx):
        hx[hx<=0]=0
        hx[hx>0]=1
        return(hx)
        
    def compute(self, h, theta, bias):
        output=np.dot(h, theta) + bias
        return output
    
    def rmsprop(self,sdw,dw):
        sdw=self.rho*sdw + (1-self.rho)*dw*dw
        return sdw
    
    def softmax(self,yhat):
      ymean=np.mean(yhat)
      ystd=np.std(yhat)
      yhat=(yhat-ymean)/ystd
      ex = np.exp(yhat)
      p  = ex/np.sum(ex,axis=0)
      return p
        
    def cross_entropy_loss(self,prob,y):
        m = y.shape[0]
        logprob=np.log(prob.clip(min=0.00000001))*-1
        product=logprob*y
        total_loss=np.sum(product)
        print('Total Loss ',total_loss)

        zero_one=(prob == prob.max(axis=1)[:,None]).astype(int)
        diff=(y == zero_one).sum(axis=1)
        accuracy=np.count_nonzero(diff == y.shape[1])
        print('Training Accuracy ',accuracy/diff.shape[0]*100)       
        
    def cross_entropy_loss_derivative(self,yhat,y):
        diff=yhat-y
        return diff
        
    def fit(self,X,y):
        X_original=X
        y_original=y
        m=X.shape[0]   
        w1=np.random.randn(X.shape[1],512)
        b1=np.zeros((1,512))
        w2=np.random.randn(512,512)
        b2=np.zeros((1,512))
        w3=np.random.randn(512,y.shape[1])
        b3=np.zeros((1,y.shape[1]))
        dropout=0.2
        keep_probability=1-dropout
        for i in range(self.epochs):
            print('epoch ',i+1)

            sdw3=sdw2=sdw1=0            
            sdb3=sdb2=sdb1=0
            length=X_original.shape[0]
            step_size=5000
            iterations=np.ceil(length/step_size)
            iterations=int(iterations)
            for j in range(iterations):
                X=X_original[j*step_size:(j+1)*step_size]
                y=y_original[j*step_size:(j+1)*step_size]
                m=X.shape[0]
                o1=self.compute(X, w1, b1)
                r1=self.relu(o1)
                mask1=np.random.rand(r1.shape[0],r1.shape[1])<keep_probability
                d1=r1*mask1
                d1/=keep_probability
                o2=self.compute(d1, w2, b2)
                r2=self.relu(o2)
                mask2=np.random.rand(r2.shape[0],r2.shape[1])<keep_probability
                d2=r2*mask2
                d2/=keep_probability
                o3=self.compute(d2, w3, b3)
                s3=self.softmax(o3)
                l=self.cross_entropy_loss(s3,y)
                gw3=(y-s3)*self.cross_entropy_loss_derivative(o3,y)
                dw3=np.dot(d2.T,gw3)/m
                db3=np.sum(gw3,axis=0)
                gw2=np.dot(gw3,w3.T)*self.relu_derivative(d2)*mask2
                dw2=np.dot(d1.T,gw2)/m
                db2=np.sum(gw2,axis=0)
                gw1=np.dot(gw2,w2.T)*self.relu_derivative(d1)*mask1
                dw1=np.dot(X.T,gw1)/m
                db1=np.sum(gw1,axis=0)
                
#Backpropagation 
#                w3+=self.learning_rate*dw3.clip(min=0.00000001)
#                w2+=self.learning_rate*dw2.clip(min=0.00000001)
#                w1+=self.learning_rate*dw1.clip(min=0.00000001)
#                
#                b3+=self.learning_rate*db3.clip(min=0.00000001)
#                b2+=self.learning_rate*db2.clip(min=0.00000001)
#                b1+=self.learning_rate*db1.clip(min=0.00000001)     

#RMSProp Start                    
                sdw3=self.rmsprop(sdw3,dw3)
                sdw2=self.rmsprop(sdw2,dw2)
                sdw1=self.rmsprop(sdw1,dw1)
                sdb3=self.rmsprop(sdb3,db3)
                sdb2=self.rmsprop(sdb2,db2)
                sdb1=self.rmsprop(sdb1,db1)
                w3+=self.learning_rate*dw3/np.sqrt(sdw3.clip(min=0.00000001))
                w2+=self.learning_rate*dw2/np.sqrt(sdw2.clip(min=0.00000001))
                w1+=self.learning_rate*dw1/np.sqrt(sdw1.clip(min=0.00000001))
                b3+=self.learning_rate*db3/np.sqrt(sdb3.clip(min=0.00000001))
                b2+=self.learning_rate*db2/np.sqrt(sdb2.clip(min=0.00000001))
                b1+=self.learning_rate*db1/np.sqrt(sdb1.clip(min=0.00000001))

#RMSProp End
        self.weight1=w1
        self.weight2=w2
        self.weight3=w3
        self.bias1=b1
        self.bias2=b2
        self.bias3=b3
        return(w1,w2,w3,b1,b2,b3)
    
#    def evaluate(self,X):
#      output1=X@self.weight1+self.bias1
#      relu1=self.relu(output1)
#      output2=relu1@self.weight2+self.bias2
#      relu2=self.relu(output2)
#      output3=relu2@self.weight3+self.bias3
#      soft3=self.softmax(output3)
#      zero_one=(soft3 == soft3.max(axis=1)[:,None]).astype(int)
#      return(zero_one)

    def predict(self,X,w1,w2,w3,b1,b2,b3):
      output1=X@w1+b1
      relu1=self.relu(output1)

      output2=relu1@w2+b2
      relu2=self.relu(output2)

      output3=relu2@w3+b3
      soft3=self.softmax(output3)

      zero_one=(soft3 == soft3.max(axis=1)[:,None]).astype(int)
      return(zero_one)

# cross validation starts
#The 5 Fold Cross validation code starts here.
#Please uncomment this and the upper part also. To split the indexes, we have taken help from sklearn.
#from sklearn.model_selection import KFold
#kf = KFold(n_splits=5)
#c=kf.get_n_splits(x_train)
#a=NeuralNetwork(10,0.001,0.9)
#best_accuracy=0
#cv=1
#for train_index, test_index in kf.split(x_train):
#    print('K Fold Cross Validation: ',cv)
#    cv+=1
#    x_tr=x_train[train_index]
#    y_tr=y_train[train_index]
#    (w1,w2,w3,b1,b2,b3)=a.fit(x_tr,y_tr)
#    x_valid=x_train[test_index]
#    y_valid=y_train[test_index]
#    y_predicted=a.evaluate(x_valid)
#    v_accuracy=accuracy_score(y_valid, y_predicted,normalize=True)
#    print('validation accuracy ',v_accuracy)
#    if v_accuracy>best_accuracy:
#        (w1f,w2f,w3f,b1f,b2f,b3f)=(w1,w2,w3,b1,b2,b3)
#        best_accuracy=v_accuracy
#    y_training_predicted=a.evaluate(x_tr)    
#    train_accuracy=accuracy_score(y_tr, y_training_predicted,normalize=True)
#    print('testing accuracy ',train_accuracy)       
#y_test_predicted=a.predict(x_test,w1f,w2f,w3f,b1f,b2f,b3f)
#accuracy_test=accuracy_score(y_test, y_test_predicted,normalize=True)
#print('best weights and bias ',w1f,w2f,w3f,b1f,b2f,b3f)
#print('best validation accuracy ',best_accuracy)
#print('test accuracy ',accuracy_test)



