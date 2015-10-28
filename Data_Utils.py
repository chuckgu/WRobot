#-*- encoding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import pandas as pd

from urllib2 import urlopen
from collections import OrderedDict
import datetime
import json

api_url = "http://147.47.123.3:8080"

daily_api_start_date = datetime.datetime.strptime("2015-09-01", '%Y-%m-%d')

def Get_data(start_date,end_date,mode,kind='kospi'):
    
    if mode == 'total':

        json_response = urlopen(api_url + "/domestic/" + kind + "/daily?start=" + daily_api_start_date.strftime('%Y%m%d') + "&end=" + end_date)
        total_data = json.loads(json_response.read())['data'] 
        
        daily_data=total_data[-1]
        
        if kind=='kospi':daily_data['name']='코스피'
        else:daily_data['name']='코스닥'

        
    elif mode == 'subject': 

        json_response = urlopen(api_url + "/domestic/" + kind + "/daily?start=" + daily_api_start_date.strftime('%Y%m%d') + "&end=" + end_date)
        total_data = json.loads(json_response.read())['data'] 
        
        d_data=total_data[-1]
        name=['개인','외국인','기관']
        value=[d_data['individual'],d_data['foreign'],d_data['institution']]
        
        daily_data=[]
        for i in range(3):
            subj_data=pd.Series()      
            subj_data['name']=name[i]
            subj_data['value']=value[i]
            daily_data.append(subj_data)
        
        
    elif mode == 'top':   
        daily_data=[]
        list_json = urlopen(api_url + "/domestic/" + kind + "/topmarketcap?date=" + start_date)
        topmarket_list = json.loads(list_json.read())["data"]
	

        for topmarket in topmarket_list:
            topmarket_json  = urlopen(api_url + "/stock/" + topmarket["stock_code"] + "/daily?" + \
    	 		"start=" + start_date + "&end=" + end_date)
            topmarket_tday = json.loads(topmarket_json.read())["data"][-1]
            topmarket_tday['name']=topmarket['stock_name']
            subj_data=pd.Series()
            subj_data=topmarket_tday
            daily_data.append(subj_data)

    elif mode == 'industry':
        daily_data=[]
        list_json = urlopen(api_url + "/domestic/" + kind + "/upjongs")
        upjong_list = json.loads(list_json.read())["data"]
        
        upjong_list.remove(upjong_list[0]) # "종합" 제거
        upjong_list.remove(upjong_list[0]) # "대형주" 제거
        upjong_list.remove(upjong_list[0]) # "중형주" 제거
        upjong_list.remove(upjong_list[0]) # "소형주" 제거

        for upjong in upjong_list:
            upjong_json = urlopen(api_url + "/upjong/" + upjong["upjong_code"] + "/daily?" + \
        	 		"start=" + start_date + "&end=" + end_date)
            upjong_tday = json.loads(upjong_json.read())["data"][0]
            upjong_tday['name'] = upjong['upjong_name']
            subj_data=pd.Series()
            subj_data=upjong_tday
            daily_data.append(subj_data)



    
    return  daily_data  

    

if(__name__ == '__main__'):

    #data=OrderedDict()
    data=Get_data('20151006','20151006','industry')