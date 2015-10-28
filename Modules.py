#-*- encoding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import pandas as pd

from Data_Utils import Get_data
from Linguistic_modules import make_sentence
from Decision import get_decision

filepath='modules/'

class Module(object):
    def __init__(self,target_date,index,market='None'):
        self.index=index   
        self.market=market
        self.target_date=target_date
        self.build()

    def get_modules(self):
        if os.path.isfile(filepath+'module'+str(self.index)+'.txt'): 
            self.definition=pd.read_csv(filepath+'module'+str(self.index)+'.txt',header=0,sep='\t')
        #print self.definition


    def build(self):
        if self.index>0:
            self.get_modules()
            ## get data from api
            self.base_data=Get_data(self.target_date,self.target_date,str(self.definition.iloc[0]['data']),self.market)

    def write(self):
        if self.index==0:
            self.sentence="\n"
        else:
            ## Get mode from engine
            frame,argument=get_decision(self.base_data,self.definition)
               
            self.sentence=make_sentence(frame,argument)
            
            #print self.sentence
        
        return self.sentence