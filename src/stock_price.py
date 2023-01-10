import os
import glob
import time
import json
import numpy as np
import pandas as pd
from datetime import datetime
from pandas_datareader import data
from utils import read_ticker


SAVE_DIR = '../data/raw/stock_price/latest'
ERROR_PATH = '../data/raw/stock_price/error_ticker.json'


def download_stock_price():
    tickers = glob.glob(os.path.join(SAVE_DIR,'*.csv'))
    obtained_tickers = [int(ticker.split('/')[-1].split('_')[0]) for ticker in tickers]
    if os.path.exists(ERROR_PATH):
        with open(ERROR_PATH, 'r') as fp:
            error_tickers = json.load(fp)
    else:
        error_tickers = {}
    obtained_tickers.extend([ec for ec in error_tickers.values()])
    df_ticker = read_ticker()
    start_time = time.time()
    print(f'total records: {df_ticker.shape[0]}')
    for i in df_ticker.index:
        ticker = df_ticker.loc[i,'コード']
        if ticker in obtained_tickers:
            continue
        name = df_ticker.loc[i,'銘柄名']
        if i!=0 and i%10==0:
            elapsed_time = round(time.time()-start_time,2)
            print(f'{i}[rec]: {elapsed_time}[sec]')
            start_time = time.time()
        try:
            df = data.DataReader(f"{ticker}.T","yahoo")
            df.to_csv(os.path.join(SAVE_DIR,f'{ticker}_{name}.csv'))
        except:
            print(f"{ticker}:{name} couldn't be getting")
            error_tickers[name] = int(ticker)
            with open(ERROR_PATH, 'w') as fp:
                json.dump(error_tickers, fp, indent=4, ensure_ascii=False)


def create_stock_price_summary():
    save_dir = '../data/preprocess/stock_price'
    os.makedirs(save_dir, exist_ok=True)
    df_ticker = read_ticker()
    prices = {}
    years = [i for i in range(2018,2023)]
    files = glob.glob(os.path.join('../data/raw/stock_price/2017_2021/*.csv'))
    start_time = time.time()
    print(f'total files: {len(files)}')
    for c,file in enumerate(files):
        if c!=0 and c%1000==0:
            elapsed_time = round(time.time()-start_time,2)
            print(f'{c}[files]: {elapsed_time}[sec]')
            start_time = time.time()
        ticker = file.split('/')[-1].split('_')[0]
        name = file.split('/')[-1].split('_')[1].split('.')[0]
        df = pd.read_csv(file, index_col='Date', parse_dates=True)
        price = {'name':name}
        check_num = 0
        max_price = 0
        for i,year in enumerate(years):
            if i == 0:
                df_tmp = df[df.index < datetime(year,1,1)]
            else:
                df_tmp = df[(df.index < datetime(year,1,1)) & (df.index > datetime(years[i-1],1,1))]
            price[f'{year-1}_min'] = df_tmp['Low'].min()
            price[f'{year-1}_max'] = df_tmp['High'].max()

            if max_price < price[f'{year-1}_max']:
                max_price = price[f'{year-1}_max']

            if check_num==0 and not np.isnan(price[f'{year-1}_min']):
                min_price = price[f'{year-1}_min']
                check_num += 1

            if len(df_tmp) > 0:
                open_price = df_tmp['Open'].values[0]
                close_price = df_tmp['Close'].values[-1]
            else:
                open_price = np.nan
                close_price = np.nan
            price[f'{year-1}_open'] = open_price
            price[f'{year-1}_close'] = close_price
            price[f'rate_of_increase_{year-1}'] = round((close_price-open_price)/open_price*100,2)


        price['min_price'] = round(min_price)
        price['max_price'] = round(max_price)
        price['rate_of_increase_whole_period'] = round((max_price-min_price)/min_price*100,2)
        price['rate_of_increase_2017_min_2021_max'] = round((price['2021_max']-price['2017_min'])/price['2017_min']*100,2)
        price['rate_of_increase_2018_min_2021_max'] = round((price['2021_max']-price['2018_min'])/price['2018_min']*100,2)
        price['rate_of_increase_2019_min_2021_max'] = round((price['2021_max']-price['2019_min'])/price['2019_min']*100,2)
        price['rate_of_increase_2020_min_2021_max'] = round((price['2021_max']-price['2020_min'])/price['2020_min']*100,2)

        price['rate_of_increase_2017_open_2021_close'] = round((price['2021_close']-price['2017_open'])/price['2017_open']*100,2)
        price['rate_of_increase_2018_open_2021_close'] = round((price['2021_close']-price['2018_open'])/price['2018_open']*100,2)
        price['rate_of_increase_2019_open_2021_close'] = round((price['2021_close']-price['2019_open'])/price['2019_open']*100,2)
        price['rate_of_increase_2020_open_2021_close'] = round((price['2021_close']-price['2020_open'])/price['2020_open']*100,2)

        price['rate_of_increase_2017_open_2020_close'] = round((price['2020_close']-price['2017_open'])/price['2017_open']*100,2)
        price['rate_of_increase_2018_open_2020_close'] = round((price['2020_close']-price['2018_open'])/price['2018_open']*100,2)
        price['rate_of_increase_2019_open_2020_close'] = round((price['2020_close']-price['2019_open'])/price['2019_open']*100,2)

        price['rate_of_increase_2017_open_2019_close'] = round((price['2019_close']-price['2017_open'])/price['2017_open']*100,2)
        price['rate_of_increase_2018_open_2019_close'] = round((price['2019_close']-price['2018_open'])/price['2018_open']*100,2)

        price['rate_of_increase_2017_open_2018_close'] = round((price['2018_close']-price['2017_open'])/price['2020_open']*100,2)

        prices[ticker] = price
    df_price = pd.DataFrame(prices).T
    df_price.to_csv(os.path.join(save_dir, 'stock_price_summary.csv'))


def run():
    # print("download stock price")
    # download_stock_price()
    print("create stock price summary")
    create_stock_price_summary()


if __name__ == '__main__':
    run()