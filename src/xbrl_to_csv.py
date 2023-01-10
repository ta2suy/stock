import os
import glob
import json
import time
import numpy as np
import pandas as pd
from edinet_xbrl.edinet_xbrl_parser import EdinetXbrlParser
from utils import read_ticker
from taxonomy import *


doc_type_code_dict = {
    '120':'有価証券報告書',
    '130':'訂正有価証券報告書',
    '140':'四半期報告書',
    '150':'訂正四半期報告書',
    '160':'半期報告書',
    '170':'訂正半期報告書',
}

common_taxonomy = {
    '会計基準':{
        'key':'jpdei_cor:AccountingStandardsDEI',
        'context_ref':'FilingDateInstant'
    },
    '当会計期間終了日':{
        'key':'jpdei_cor:CurrentPeriodEndDateDEI',
        'context_ref':'FilingDateInstant'
    },
    '当会計期間の種類':{
        'key':'jpdei_cor:TypeOfCurrentPeriodDEI',
        'context_ref':'FilingDateInstant'
    },
    '自己保有株式数':{
        'key':'jpcrp_cor:DisposalsOrHoldingOfAcquiredTreasurySharesTextBlock',
        'context_ref':'FilingDateInstant'
    }
}

taxonomy_functions_dict = {
    "Japan GAAP_有価証券報告書_Consolidated":japan_gaap_taxonomy,
    "Japan GAAP_有価証券報告書_NonConsolidated":japan_gaap_nonconsolidated_taxonomy,
    "IFRS_有価証券報告書_Consolidated":ifrs_taxonomy,
    "IFRS_有価証券報告書_NonConsolidated":ifrs_nonconsolidated_taxonomy,
    "US GAAP_有価証券報告書_Consolidated":us_gaap_taxonomy,
    "US GAAP_有価証券報告書_NonConsolidated":us_gaap_nonconsolidated_taxonomy
}

        
def select_doc_summary(df_doc_summary, doc_type_code, sec_code):
    df_doc_summary = df_doc_summary[df_doc_summary['docTypeCode']==doc_type_code]
    df_doc_summary = df_doc_summary[df_doc_summary['secCode']==sec_code*10]
    return df_doc_summary


def get_xbrl_paths(df_doc_summary):
    xbrl_paths = []
    for doc_idx in df_doc_summary.index:
        doc_id = df_doc_summary.loc[doc_idx,'docID']
        date = df_doc_summary.loc[doc_idx,'submitDateTime'].split(' ')[0].split('-')
        xbrl_path = f"../data/raw/edinet/document/{date[0]}/{date[1]}/{date[2]}/{doc_id}/XBRL/PublicDoc/*.xbrl"
        xbrl_files = glob.glob(xbrl_path)
        if len(xbrl_files)==0:
            print(f'no xbrl file in {xbrl_path}')
            continue
        else:
            xbrl_paths.append(xbrl_files[0])
    return xbrl_paths


def get_accounting_data(edinet_xbrl_object, doc_type_code, sec_code):
    try:
        accounting_standards = edinet_xbrl_object.get_data_by_context_ref(common_taxonomy['会計基準']['key'],common_taxonomy['会計基準']['context_ref']).get_value() 
        current_period_end_date = edinet_xbrl_object.get_data_by_context_ref(common_taxonomy['当会計期間終了日']['key'],common_taxonomy['当会計期間終了日']['context_ref']).get_value()
        if doc_type_code in [140, 150]:
            type_of_current_period = edinet_xbrl_object.get_data_by_context_ref(common_taxonomy['当会計期間終了日']['key'],common_taxonomy['当会計期間終了日']['context_ref']).get_value() 
            type_of_current_period = f"[{type_of_current_period}]"
        else:
            type_of_current_period = ""
        return accounting_standards, current_period_end_date, type_of_current_period

    except:
        doc_type_name = doc_type_code_dict[str(doc_type_code)]
        error_path = f'../data/preprocess/edinet/{doc_type_name}/error_account_files.txt'
        print(f"no accounting data in {sec_code}")
        with open(error_path, 'a') as f:
            print(sec_code,file=f)
        return None, None, None


def get_values_from_xbrl(edinet_xbrl_object, key, context_refs):
    values = []
    for context_ref in context_refs:
        data = edinet_xbrl_object.get_data_by_context_ref(key,context_ref)
        try:
            values.append(data.get_value())
        except:
            values.append(np.nan)
    return values


def get_values_from_xbrl_by_some_keys(edinet_xbrl_object, key, context_refs):
    if type(key)==list:
        for i,k in enumerate(key):
            tmp_values = get_values_from_xbrl(edinet_xbrl_object, k, context_refs)
            tmp_nan_num = pd.DataFrame(tmp_values).isnull().sum().values[0]
            if i==0:
                values = tmp_values
                nan_num = tmp_nan_num
                continue
            else:
                if nan_num > tmp_nan_num:
                    values = tmp_values
                    nan_num = tmp_nan_num
        return values
    else:
        return get_values_from_xbrl(edinet_xbrl_object, key, context_refs)

        
def ccreate_financial_summary(sec_code, company_name, df_doc_summary, doc_type_code=120):
    parser = EdinetXbrlParser()
    doc_type_name = doc_type_code_dict[str(doc_type_code)]
    save_dir = f'../data/preprocess/edinet/{doc_type_name}/'
    if len(glob.glob(os.path.join(save_dir,"*",f"{sec_code}_{company_name}.csv")))==2:
        print(f"{sec_code}_{company_name} already exists")
        return None
    else:
        df_doc_summary = select_doc_summary(df_doc_summary, doc_type_code, sec_code)
        if len(df_doc_summary) > 0:
            edinet_code = df_doc_summary['edinetCode'].values[0]
            xbrl_paths = get_xbrl_paths(df_doc_summary)

            if len(xbrl_paths) > 0:
                for consolidated_type in ["Consolidated","NonConsolidated"]:
                    cnt = 0
                    for xbrl_path in xbrl_paths:
                        edinet_xbrl_object = parser.parse_file(xbrl_path)
                        accounting_standards, current_period_end_date, type_of_current_period = get_accounting_data(edinet_xbrl_object, doc_type_code, sec_code)
                        if not accounting_standards or not current_period_end_date:
                            continue    
                        else:
                            year = int(current_period_end_date.split('-')[0])
                            month = current_period_end_date.split('-')[1]
                            _, taxonomy_dict = taxonomy_functions_dict[f"{accounting_standards}_{doc_type_name}_{consolidated_type}"](edinet_code)
                            financial_summary_dict = {}
                            for label in taxonomy_dict.keys():
                                key = taxonomy_dict[label]['key']
                                context_refs = taxonomy_dict[label]['context_ref']
                                financial_summary_dict[label] = get_values_from_xbrl_by_some_keys(edinet_xbrl_object, key, context_refs)
                            df_finance = pd.DataFrame(financial_summary_dict).T
                            cols = [f'{year-i}_{month}{type_of_current_period}' for i in reversed(range(0,5))]
                            df_finance.columns = cols
                        if cnt==0:
                            df_finances = df_finance
                            cnt += 1
                            continue
                        else:
                            delete_cols = [c for c in df_finances.columns if c in cols]
                            df_finances.drop(columns=delete_cols,inplace=True)
                            df_finances = df_finances.join(df_finance)
                    if cnt > 0:
                        save_path = os.path.join(save_dir,consolidated_type,f'{sec_code}_{company_name}.csv')
                        df_finances = df_finances.T
                        df_finances.to_csv(save_path)
                print(f"ccreate financial summary in {sec_code}_{company_name}")



def run():
    df_ticker = read_ticker()
    df_doc_all_summary = pd.read_csv('../data/preprocess/edinet/doc_all_summary.csv')
    for ticker_idx in df_ticker.index:
        sec_code = df_ticker.loc[ticker_idx,'コード']
        company_name = df_ticker.loc[ticker_idx,'銘柄名']
        ccreate_financial_summary(sec_code, company_name, df_doc_all_summary)

if __name__ == '__main__':
    run()