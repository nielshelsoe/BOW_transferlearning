#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 11:12:24 2018

@author: benjamin
"""

from fastText import train_supervised, load_model


from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.multiclass import unique_labels


from tempfile import NamedTemporaryFile
import numpy as np
import pandas as pd

class sk_Fasttext(BaseEstimator, ClassifierMixin):
    '''
    This a scikit wrapper for fastText, and thus the attributes below are almost the same as in the original libary
    - Thus most of the text is ripped from: github.com/facebookresearch/fastText/
    
    - Since this is wrapper all line Breakes (\n) will be removed in the input data. 
    - Thus if you want those to count replace them with another character
    
    The following arguments are mandatory:
        - None as of now
        
    The following arguments are optional:
        -verbose         verbosity level [2]  - not implemented
        -mkTemp          use a tempoary file for trainning [True] -not implemented
        -train_file      filename of trainning file nb. only used id mkTemp == False
        
    The following arguments for the dictionary are optional:
        -minCount        minimal number of word occurences [1]
        -minCountLabel   minimal count of word occurences [0]
        -wordNgrams      max length of word ngram [1]
        -bucket          number of buckets [2000000]
        -minn            min length of char ngram[0]
        -maxn            max length of char ngram[0]
        -t               sampling threshold [0.0001]
        -label           labels prefix [__label__]
    
    The following arguments for the trainning are optional:
        - lr             learning rate[0.1]
        - lrUpdateRate   change the rate of updates for the learning rate [100]
        - dim            size of word vectors [100]
        - ws             size of the context window [5]
        - epoch          number of epochs [5]
        - neg            number of negatives sampled
        - loss           loss function {ns, hs, softmax} [softmax]
        - thread         number of threads [12]   
    '''
    
    def __init__(self, label = "__label__", verbose = 2, mkTemp = True,
                 train_file = "ft_temp", minCount = 1, minCountLabel = 0, wordNgrams = 1,
                 bucket = 2000000, minn = 0, maxn = 0,  t = 0.0001, lr = 0.1,
                 lrUpdateRate = 100, dim = 100, ws = 5, epoch = 5, neg = 5,
                 loss = "softmax", thread = 12
                 ):
        self.label = label
        self.verbose = verbose
        self.mkTemp = mkTemp
        self.train_file = train_file
        self.minCount = minCount 
        self.minCountLabel = minCountLabel
        self.wordNgrams = wordNgrams
        self.bucket = bucket
        self.minn = minn
        self.maxn = maxn
        self.t = t
        self.lr = lr
        self.lrUpdateRate = lrUpdateRate
        self.dim = dim
        self.ws = ws
        self.epoch = epoch
        self.neg = neg
        self.loss = loss
        self.thread = thread

        self.type = str
        
    def fit(self, X, y):
        # Checks that dimensions are correct
        if type(X) == type(pd.DataFrame()):
            X = X.values
        
        y = list(y)
        self.type = type(y[0])
        
        
        X = [x[0] for x in X]

        # initiated the class variables
        self.classes_ = unique_labels(y)
        
        ### First we need to create the tempoary file for trainning
        if self.mkTemp == True:
            f = NamedTemporaryFile(mode="w")
        else:
            f = open(self.train_file, "w")
            
        
        for i in range(len(X)):
            textToWrite = self.label + str(y[i]) + " " 
            textToWrite += X[i].replace("\n", " ")
            f.write(textToWrite + "\n")
        
        self.classifier = train_supervised(f.name, label=self.label, verbose=self.verbose,
                                           minCount = self.minCount, minCountLabel = self.minCountLabel,
                                           wordNgrams = self.wordNgrams, bucket = self.bucket,
                                           minn = self.minn, maxn = self.maxn, t = self.t,
                                           lr = self.lr, lrUpdateRate = self.lrUpdateRate,
                                           dim = self.dim, ws = self.ws, epoch = self.epoch,
                                           neg = self.neg, loss = self.loss, thread = self.thread)
        
        self.X_ = X
        self.y_ = y
        
        # Closes and destroys temp file
        f.close()
        
        # Return Classifier
        return self
    
    def predict(self, X):
        # transforms pandas til numpy
        if type(X) == type(pd.DataFrame()):
            X = X.values
        
        X = [x[0] for x in X]
        
        # Replaces all /n because else it will break
        X = [x.replace("\n", " ") for x in X]
        
        # Predicts using fasttext format
        labels, prop  = self.classifier.predict(X, k=1)
       
        # get class of predictions
        y = [self.type(x[0].replace(self.label, "")) for x in labels]
        
        return np.array(y)
    
    
    def predict_proba(self, X):
        # Transforms pandas to numpy
        if type(X) == type(pd.DataFrame()):
            X = X.values
            
        # Replaces all /n because else it will break
        X = [x[0] for x in X]
        X = [x.replace("\n", " ") for x in X]
        
        # Predicts using fasttext format
        labels, prop  = self.classifier.predict(X, k=len(self.classes_))
        
        
        # get probalities
        y = []
        for i in range(len(labels)):
            res_labels = [x.replace(self.label, "") for x in labels[i]]
            resultDict = dict(zip(res_labels,prop[i]))
            class_prop = []
            for x in self.classes_:
                class_prop.append(resultDict[x])
            y.append(class_prop)
            
        return y
        
    
    def save_model(self, path):
        self.classifier.save_model(path)
        
    def load_model_ft(self, path):
        self.classifier = load_model(path)
        self.classes_ = unique_labels([x.replace(self.label, "") for x in self.classifier.get_labels()])
