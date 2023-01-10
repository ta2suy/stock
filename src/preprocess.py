import json
import time
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from utils import *


def calculate_rate_of_change(df):
    labels = [
        '売上高',
        '経常利益', 
        '当期純利益', 
        "純資産額", 
        "総資産額", 
        "ROE（自己資本利益率）", 
        "期末残高", 
        "従業員数"
    ]
    df_rate = pd.DataFrame(df[labels].values[1:]/df[labels].values[:-1]*100)
    df_rate.columns = [label+"_変化率(前年比)" for label in labels]
    df_rate.index = df.index[1:]
    return df_rate


def calculate_operating_cash_flow_margin(df):
    df["営業CFマージン"] = df["営業CF"]/df["売上高"]*100
    return df


def calculate_discount_evaluate_rate(equity_ratio):
    if equity_ratio>=0.8:
        return 0.8
    elif equity_ratio>=0.67:
        return 0.75
    elif equity_ratio>=0.5:
        return 0.7
    elif equity_ratio>=0.33:
        return 0.65
    elif equity_ratio>=0.1:
        return 0.6
    else:
        return 0.5


def calculate_asset_value(df):
    df["資産価値"] = np.nan
    for i in df.index:
        discount_evaluate_rate = calculate_discount_evaluate_rate(df.loc[i,"自己資本比率"])
        df.loc[i,"資産価値"] = df.loc[i,"BPS（１株当たり純資産額）"] * discount_evaluate_rate
    return df 


def calculate_financial_leverage_correction(equity_ratio):
    tmp_values = equity_ratio + 0.33
    if tmp_values < 0.66:
        tmp_values = 0.66
    elif tmp_values > 1:
        tmp_values = 1
    financial_leverage_correction = 1 / tmp_values
    return financial_leverage_correction


def calculate_enterprize_value(df):
    df["事業価値"] = np.nan
    for i in df.index:
        financial_leverage_correction = calculate_financial_leverage_correction(df.loc[i,"自己資本比率"])
        eps = df.loc[i,"EPS（１株当たり当期純利益）"]
        if eps > df.loc[i,"BPS（１株当たり純資産額）"]*0.6:
            eps = df.loc[i,"BPS（１株当たり純資産額）"]*0.6
        roa = df.loc[i,"当期純利益"] / df.loc[i,"総資産額"]
        df.loc[i,"事業価値"] = eps * roa * 150 * financial_leverage_correction
    return df 


def calculate_risk_assessment_rate(pbr):
    if pbr >= 0.5:
        return 1
    elif pbr >= 0.41:
        return 0.8
    elif pbr >= 0.34:
        return 0.66
    elif pbr >= 0.26:
        return 0.5
    elif pbr >= 0.21:
        return 0.33
    elif pbr >= 0.04:
        return (pbr/5 * 50) + 50
    else:
        return (pbr-1) * 10 + 5


def calculate_theoretical_value(df):
    if not "資産価値" in df.columns:
        df = calculate_asset_value(df)
    if not "事業価値" in df.columns:
        df = calculate_enterprize_value(df)
    df["理論株価"] = np.nan
    for i in df.index:
        pbr = df.loc[i,"PER（株価収益率）"] * df.loc[i,"ROE（自己資本利益率）"]
        risk_assessment_rate = calculate_risk_assessment_rate(pbr)
        df.loc[i,"理論株価"] = (df.loc[i,"資産価値"]+df.loc[i,"事業価値"]) * risk_assessment_rate
    df["上限理論株価"] = df["資産価値"] + (df["事業価値"] * 2)
    return df


def add_stock_price(df, ticker):
    df_stock_price = read_stock_price_by_ticker(ticker)
    df["株価"] = np.nan
    for date in df.index:
        year = int(date.split('_')[0])
        month = int(date.split('_')[1])
        df_stock_price_tmp = df_stock_price[df_stock_price.index <= datetime(year, month, 1) + timedelta(days=31)]
        if len(df_stock_price_tmp) > 0:
            df.loc[date, "株価"] = df_stock_price_tmp["Open"].values[-1]
    return df


def preprocess_financial_summary(df):
    df_rate = calculate_rate_of_change(df)
    df = df.iloc[1:].join(df_rate)
    df = calculate_operating_cash_flow_margin(df)
    df = calculate_theoretical_value(df)
    return df


def run():
    save_dir = "../data/preprocess/edinet/有価証券報告書/Summary/"
    os.makedirs(save_dir, exist_ok=True)
    df_ticker = read_ticker()
    code_to_company_name = read_code_to_company_name()
    print(f"total ticker: {len(df_ticker)}")
    for i,ticker in enumerate(df_ticker["コード"]):
        company_name = code_to_company_name[ticker]
        filename = f"{ticker}_{company_name}.csv"
        save_path = os.path.join(save_dir,filename)
        if os.path.exists(save_path):
            # print(f"{filename} already exists")
            continue
        try:
            start_time = time.time()
            df = read_and_select_financial_summary_by_ticker(ticker)
            df = preprocess_financial_summary(df)
            df = add_stock_price(df, ticker)
            df.to_csv(save_path)
            elapsed_time = round(time.time()-start_time,2)
            print(f"{i} preprocessed {filename}: {elapsed_time}[sec]")
        except:
            print(f"error {ticker}")


    
if __name__ == '__main__':
    run()