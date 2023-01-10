import os
import glob
import math
import pickle
import pandas as pd
import japanize_matplotlib  
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm


def read_code_to_company_name():
    with open("../data/preprocess/etc/code_to_company_name.pkl", "rb") as f:
        code_to_company_name = pickle.load(f)
    return code_to_company_name

def read_ticker():
    df_ticker = pd.read_excel("../data/raw/etc/東証上場銘柄一覧_202111.xls")
    remove_category = ['ETF・ETN','PRO Market','REIT・ベンチャーファンド・カントリーファンド・インフラファンド','市場第一部（外国株）']
    for rc in remove_category:
        df_ticker = df_ticker[df_ticker['市場・商品区分']!=rc]
    del_idx  = [i for i in df_ticker.index if len(str(df_ticker.loc[i,'コード']))!=4]
    df_ticker.drop(del_idx, inplace=True)
    df_ticker.reset_index(drop=True, inplace=True)
    return df_ticker


def read_stock_price_by_ticker(ticker):
    path = glob.glob(f'../data/raw/stock_price/2017_2021/{ticker}_*.csv')
    if len(path) != 1:
        raise(f"{ticker} file not found")
    path = path[0]
    df = pd.read_csv(path, index_col='Date', parse_dates=True)
    return df


def read_financial_summary_by_ticker(ticker, dir_name="Summary"):
    path = glob.glob(f"../data/preprocess/edinet/有価証券報告書/{dir_name}/{ticker}_*.csv")
    if len(path)==0:
        raise(f"no {dir_name} file in {ticker}")
    df = pd.read_csv(path[0], index_col=0)
    return df


def read_and_select_financial_summary_by_ticker(ticker):
    df = read_financial_summary_by_ticker(ticker, dir_name="Consolidated")
    if df.isnull().sum()["売上高"]==len(df):
        df = read_financial_summary_by_ticker(ticker,"NonConsolidated")
    # nan_num = df.isnull().sum()["売上高"]
    # if nan_num > 0:
    #     df_tmp = read_financial_summary_by_ticker(ticker,"NonConsolidated")
    #     nan_num_tmp = df_tmp.isnull().sum()["売上高"]
    #     if nan_num > nan_num_tmp:
    #         df = df_tmp.copy()
    return df


def plot_stock_price(ticker, company_name, time_scale='month', save_dir=None):
    df = read_stock_price_by_ticker(ticker)
    d_ohlcv = {'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'}

    if time_scale=='month':
        df = df.resample('MS', closed='left', label='left').agg(d_ohlcv) # MONTH
    else:
        df = df.resample('W-MON', closed='left', label='left').agg(d_ohlcv) # WEEK

    cs = mpf.make_mpf_style(base_mpf_style='yahoo', rc={"font.family":'IPAexGothic'})
    if save_dir:
        save_path = os.path.join(save_dir,f'{ticker}_{company_name}.png')
        mpf.plot(df, type='candle', volume=True, figratio=(12,4), mav=(6,12,24), style=cs, title=f'{ticker}_{company_name}', savefig=save_path)
    else:
        mpf.plot(df, type='candle', volume=True, figratio=(12,4), mav=(6,12,24), style=cs, title=f'{ticker}_{company_name}')


def plot_financial_summary(df, title, labels=None, save_dir=None, plot_type="bar", color_map='tab20'):
    if not labels:
        labels = df.columns.values
    num = [i for i in range(1,10) if i*i >= len(labels)][0]
    left = [i for i in range(0, df.shape[0])]
    xticklabels = [i[2:4]+"/"+i[-2:] for i in df.index]
    usercmap = plt.get_cmap(color_map)
    cNorm  = colors.Normalize(vmin=0, vmax=len(labels))
    scalarMap = cm.ScalarMappable(norm=cNorm, cmap=usercmap)

    fig = plt.figure(figsize=(num*5,num*4), facecolor='w')
    for i,label in enumerate(labels):
        ax = fig.add_subplot(num, num, i+1)
        if plot_type == "bar":
            ax.bar(left, df[label].values, label=label, color=scalarMap.to_rgba(i))
        elif plot_type == "plot":
            ax.plot(df[label].values, label=label, color=scalarMap.to_rgba(i))
        ax.set_xticks(left)
        ax.set_xticklabels(xticklabels, rotation=45)
        ax.set_ylabel(label)
    fig.suptitle(title)
    if save_dir:
        fig.savefig(os.path.join(save_dir,f"{title}.png"))
        plt.close()
    else:
        plt.show()


def plot_financial_summary_by_ticker(ticker, lables=None, save_dir=None, plot_type="bar", color_map='tab20'):
    df = read_and_select_financial_summary_by_ticker(ticker)
    code_to_company_name = read_code_to_company_name()
    company_name = code_to_company_name[ticker]
    title = f"{ticker}_{company_name}"
    plot_financial_summary(df, title, lables=None, save_dir=None, plot_type="bar", color_map='tab20')
