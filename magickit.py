import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd


def magic_list(mincap=50):
    # get magicformulainvesting list with minimum market cap of mincap default $50M
    url = "https://www.magicformulainvesting.com/Screening/StockScreening"
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
        'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '_fbp=fb.1.1633820068955.1421127812; .ASPXAUTH=C994B160274A2980F9299F2889995DE5D726F27A5C56010A94A0E4AC2387DD81E494263AE19BC05AB64CD00DFFC372392E6FC6695DB18323D1B7AD0E0CB44101C221B4C0921CC8E90270A5B5114FD6E8F49AC254D070A35F8C5759CA5416E77CF4843435C52DD72F96BD62FB553A5D07284BD55273303C3700E5C21BA8228A27B950BA9C8CCF6713EDA887B3F3F17BF2821821C1EFD1EA748481512397CE1268'
    }
    payload = {
        'MinimumMarketCap':mincap,
        'Select30':'false',
        'stocks': 'Get Stocks'

    }
    page = requests.post(url,headers=headers,data=payload)
    soup = bs4(page.content,features="html.parser")
    results = soup.find(id="tableform")
    lines = results.find("tbody").find_all("td")
    i=0
    company_list = []
    while i <len(lines):
        company = [lines[i].text,lines[i+1].text,float(lines[i+2].text.replace(",",""))*1000000,lines[i+3].text
                ,lines[i+4].text]
        company_list.append(company)
        i+=5
    columns = ['name','symbol','MktCap','date','MRQ']
    df_companies = pd.DataFrame(company_list,columns=columns)
    df_companies.set_index('symbol',inplace=True)
    return df_companies


if __name__ == '__main__':
    magic_list()