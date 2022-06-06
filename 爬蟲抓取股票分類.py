# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 17:09:51 2022

@author: mjl
"""

import requests
from bs4 import BeautifulSoup
sectors = ['communicationservices','consumercyclical','consumerdefensive','energy','financial','healthcare','industrials','realestate','technology','utilities']
#函數返回該sector下所有公司代號的list ，get_namelist
def get_namelist(sector):
    print('start')
    url = "https://finviz.com/screener.ashx?v=111&f=sec_"+sector+"&r="
    #不加header會抓不全
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    last_get_list = []
    res_list = []
    i = 1
    # epoch = 1
    while 1:
        # print('epoch:',epoch)
        temp_url = url+str(i)
        # print(temp_url)
        response = requests.get(temp_url,headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        name_box = soup.find_all('a',attrs={'class':'screener-link-primary'})
        cur_get_list = [ele.text for ele in name_box]
        # print("cur_get_list:",cur_get_list)
        # print("last_get_list:",last_get_list)
        if len(cur_get_list) == 20:
            res_list += cur_get_list
        else:
            last_get_list = set(last_get_list)
            for name in cur_get_list:
                if name not in last_get_list:
                    res_list.append(name)
            print('end')
            return res_list
        last_get_list = cur_get_list
        i += 20
        # epoch += 1   
#生成每個公司對應產業的dict
def gen_dict_of_stock_to_cate():
    category = dict()
    for sector in sectors:
        name_list = get_namelist(sector)
        for  name in name_list:
            category[name] = sector
    return category
#生成每個產業對應公司list的dict
def gen_dict_of_cate_to_stockslist():
    category = gen_dict_of_stock_to_cate()
    f = open('NASDAQ.txt')
    symbols = [line.split()[0] for line in f.readlines()]
    f.close()
    result = dict()
    for sector in  sectors:
        result[sector] = []
    for name in symbols:
        if category.get(name) == None:
            print(name)
        else:
            result[category[name]].append(name)   
    return result
#寫個txt記錄保存
def gen_txt():
    result = gen_dict_of_cate_to_stockslist()
    for sector in sectors:
        f = open(sector+'.txt','w')
        for name in result[sector]:
            print(name)
            f.write(name+'\n')
gen_txt()