#-*- encoding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import pandas as pd
from collections import OrderedDict
from Data_Utils import Get_data

from Modules import Module

filepath='templates/'

class Template(object):
    def __init__(self,target_date,index):
        self.index=index
        self.target_date=target_date
        self.modules=[]
        self.articles=[]
        
    def get_modules(self):
        if os.path.isfile(filepath+'template'+str(self.index)+'.txt'): 
            self.modules_id=pd.read_csv(filepath+'template'+str(self.index)+'.txt', header=0,sep='\t')
        
        
    def build(self):
        self.get_modules()
        for (mod,mar) in zip(self.modules_id['index'],self.modules_id['market']):
            self.modules.append(Module(self.target_date,mod,mar))
    
    def write(self):
        for module in self.modules:
            self.articles.append(module.write())          
        
        return self.articles
        