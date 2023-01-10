import os
import json
import time
import pickle
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from utils import read_ticker

save_path = "../data/raw/etc/date_of_listing.json"


def get_date_of_listing(ticker):
    url = f"https://minkabu.jp/stock/{ticker}/fundamental"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        return soup.select(".md_dataList")[-1].select("dd")[1].text.replace("\xa0","")
    except:
        print(f"Do not get date_of_listing in {ticker}")
        return np.nan


def save_json(date_of_listing):
    with open(save_path, mode="w", encoding="utf-8") as f:
        json.dump(date_of_listing, f, ensure_ascii=False, indent=4)
    print('save json')


def scraping_date_of_listing():
    df_ticker = read_ticker()
    if os.path.exists(save_path):
        with open(save_path, mode="r", encoding="utf-8") as f:
            date_of_listing = json.load(f)
    else:
        date_of_listing = {}
    print(f"total tickers: {len(df_ticker)}")
    for i,ticker in enumerate(df_ticker['コード']):
        if str(ticker) in date_of_listing.keys():
            continue
        else:
            start_time = time.time()
            date_of_listing[str(ticker)] = get_date_of_listing(ticker)
            elapsed_time = round(time.time()-start_time,2)
            print(f"{i} Acquired {ticker}: {elapsed_time}[sec]")
            time.sleep(3)
        if i!=0 and i%10==0:
            save_json(date_of_listing)
    save_json(date_of_listing)
    print('Done')


def create_company_info():
    df_ticker = read_ticker()
    with open("../data/raw/etc/date_of_listing.json", mode="r", encoding="utf-8") as f:
        date_of_listing = json.load(f)
    df_date_of_listing = pd.DataFrame([date_of_listing]).T
    df_date_of_listing.reset_index(inplace=True)
    df_date_of_listing.columns = ['コード','上場日']
    df_date_of_listing['コード'] = df_date_of_listing['コード'].astype('int')

    df = pd.merge(df_ticker,df_date_of_listing, on='コード')
    df.to_csv('../data/preprocess/etc/company_info.csv', index=False)


def create_code_to_company_name():
    df_ticker = read_ticker()
    code_to_company_name = {}
    for i in df_ticker.index:
        code_to_company_name[df_ticker.loc[i,"コード"]] = df_ticker.loc[i,"銘柄名"]
    with open("../data/preprocess/etc/code_to_company_name.pkl", "wb") as f:
        pickle.dump(code_to_company_name, f)


def run():
    print("scraping date of listing")
    scraping_date_of_listing()
    print("create company info")
    create_company_info()
    print("create code to company_name")
    create_code_to_company_name()
    
    
if __name__ == '__main__':
    run()