#-*- encoding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import pandas as pd


def get_decision(data,definition):
    index=0
    subj=definition['subj'][0]
    mode=definition['mode'][0]
    
    if mode==1:#그룹 및 지수
        if subj==1: ##한종목 
            base_data=pd.DataFrame()
            base_data['index']=definition['index']
            base_data['value']=definition['dir'] 
            delta=float(data['drate'])*3
            index=get_index(base_data,delta)
            
            fact_data=pd.Series()
            fact_data['subj']=data['subj']
            fact_data['delta']=abs(data['delta'])
            fact_data['drate']=data['drate']
            fact_data['finalvalue']=abs(data['finalvalue'])
        elif subj>1: ##여러종목
            up=1
            down=1
            delta=0
            fact_data=pd.Series()
            for d in data:
                if d['value']>=0:
                    fact_data['u_name'+str(up)]=d['sub']
                    fact_data['u_value'+str(up)]=abs(d['value'])
                    up+=1
                    delta+=5
                else:
                    fact_data['d_name'+str(down)]=d['sub']
                    fact_data['d_value'+str(down)]=abs(d['value'])
                    down+=1                    
                    delta-=5
            base_data=pd.DataFrame()
            base_data['index']=definition['index']
            base_data['value']=definition['dir']                 

            index=get_index(base_data,delta) 
    elif mode==2: #개별주식들&업종
        if subj==1:
            return
        elif subj>1:
            up=1
            down=1
            delta=0
            fact_data=pd.Series()
            for d in data:
                if d['drate']>=0:
                    fact_data['u_name'+str(up)]=d['name']
                    fact_data['u_value'+str(up)]=d['close']
                    fact_data['u_rate'+str(up)]=d['drate']
                    #fact_data['u_diff'+str(up)]=d['diff']
                    up+=1
                    delta+=d['drate']*3
                else:
                    fact_data['d_name'+str(down)]=d['name']
                    fact_data['d_value'+str(down)]=d['close']
                    fact_data['d_rate'+str(down)]=d['drate']
                    #fact_data['d_diff'+str(down)]=d['diff']
                    down+=1                    
                    delta-=d['drate']*3
            base_data=pd.DataFrame()
            base_data['index']=definition['index']
            base_data['value']=definition['dir']      
            base_data['up']=definition['up'] 
            print "up:%s"%str(up-1)
            print "down:%s"%str(down-1)
            index=get_index(base_data,delta,up-1)                         
            
     
    ## arguments in sentence
    argument=[]
    arg=definition[definition['index']==index].iloc[0]['arg']
    arg=arg.split(',')
    #print arg
    for d in arg:
        argument.append(fact_data[d])
    
    
    frame=definition[definition['index']==index].iloc[0]['sentence'].encode('utf-8')
    
    return frame,argument
    

def get_index(data,point,up=-1): 

    if up>=0:
        data['up_diff']=abs(data['up']-up)
        index=data[data['up_diff']==min(data['up_diff'])].iloc[0]['index']
    else:
        data['value_diff']=abs(data['value']-point)
        index=data[data['value_diff']==min(data['value_diff'])].iloc[0]['index']
    print data
    print point 
    
    return index
    