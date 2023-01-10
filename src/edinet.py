import os
import glob
import time
import shutil
import zipfile
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from utils import read_code_to_company_name


EDINET_API_URL = "https://disclosure.edinet-fsa.go.jp/api/v1"
SUMMARY_TYPE = 2

doc_type_code_dict = {
    '120':'有価証券報告書',
    '130':'訂正有価証券報告書',
    '140':'四半期報告書',
    '150':'訂正四半期報告書',
    '160':'半期報告書',
    '170':'訂正半期報告書',
}


def get_submitted_summary(params):
    url = EDINET_API_URL + '/documents.json'
    response = requests.get(url, params=params)
     
    # responseが200でなければエラーを出力
    assert response.status_code==200
       
    return response.json()


def get_document(doc_id, params):
    url = EDINET_API_URL + '/documents/' + doc_id
    response = requests.get(url, params)
     
    return response


def download_document(doc_id, save_path):
    params = {'type': 1}
    doc = get_document(doc_id, params)
    if doc.status_code == 200:
        with open(os.path.join(save_path, doc_id + '.zip'), 'wb') as f:
            for chunk in doc.iter_content(chunk_size=1024):
                f.write(chunk)


def open_zip_file(doc_id, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path + doc_id)
    with zipfile.ZipFile(os.path.join(save_path, doc_id + '.zip')) as zip_f:
        zip_f.extractall(os.path.join(save_path, doc_id))


def download_all_documents(date, doc_type_codes=['120','130','140','150','160','170'], sec_codes=None):
    date = str(date)[:10]
    params = {'date': date, 'type': SUMMARY_TYPE}
    tmp_date = date.split('-')
    save_path = os.path.join(f'../data/raw/edinet/document/',tmp_date[0],tmp_date[1],tmp_date[2])
    error_path = '../data/raw/edinet/document/download_error_files.txt'
    # if not os.path.exists(os.path.join(save_path,'doc_summary.csv')):
    print(f'get submitted summary in {date}')
    doc_summary = get_submitted_summary(params)
    try:
        df_doc_summary = pd.DataFrame(doc_summary['results'])
        df_meta = pd.DataFrame(doc_summary['metadata'])
    except:
        print(f'No results in {date}')
        return None
    
    # 対象とする報告書のみ抽出
    if len(df_doc_summary) >= 1:
        df_doc_summary.dropna(subset=['secCode'], inplace=True)
        df_doc_summary = df_doc_summary.loc[df_doc_summary['docTypeCode'].isin(doc_type_codes)]
        # 一覧を保存
        if len(df_doc_summary) >= 1:
            os.makedirs(save_path, exist_ok=True)
            df_doc_summary.to_csv(os.path.join(save_path,'doc_summary.csv'), index=False)
            df_doc_summary.reset_index(drop=True, inplace=True)
    # else:
    #     print(f'doc_summary already exists in {date}')
    #     df_doc_summary = pd.read_csv(os.path.join(save_path,'doc_summary.csv'))

    if len(df_doc_summary) >= 1:
        print(f'total files: {len(df_doc_summary)}')
        if sec_codes:
            df_doc_summary = df_doc_summary.loc[df_doc_summary['secCode'].isin(sec_codes)]
        # 書類を保存
        start_time = time.time()
        for i, doc in df_doc_summary.iterrows():
            if os.path.exists(os.path.join(save_path,f"{doc['docID']}")):
                continue
            download_document(doc['docID'], save_path)
            try:
                open_zip_file(doc['docID'], save_path)
                os.remove(os.path.join(save_path,f"{doc['docID']}.zip"))
            except:
                print(f"{doc['docID']}.zip could not open")
                with open(error_path, 'a') as f:
                    print(f"{date,doc['docID']}",file=f)

            elapsed_time = round(time.time()-start_time,2)
            print(f"{i}. {doc['docID']} has downloaded: {elapsed_time}[sec]")
            start_time = time.time()
        print('')
    else:
        print(f'no record in df_doc_summary')


def date_range(start_date: datetime, end_date: datetime):
    diff = (end_date - start_date).days + 1
    return (start_date + timedelta(i) for i in range(diff))


def summarize_doc_summary():
    import_path = f'../data/raw/edinet/document/*/*/*/doc_summary.csv'
    files = glob.glob(import_path)
    for i,f in enumerate(files):
        if i == 0:
            df = pd.read_csv(f)
            cols = df.columns
            doc_summary = df.values
        else:
            doc_summary = np.vstack((doc_summary,pd.read_csv(f).values))
    df = pd.DataFrame(doc_summary, columns=cols)
    save_dir = f'../data/preprocess/edinet/'
    os.makedirs(save_dir, exist_ok=True)
    df.to_csv(os.path.join(save_dir,f'doc_all_summary.csv'), index=False)


def copy_xbrl():
    code_to_company_name = read_code_to_company_name()
    df_doc_summary = pd.read_csv("../data/preprocess/edinet/doc_all_summary.csv")
    df_doc_summary["secCode"] = df_doc_summary["secCode"]/10
    df_doc_summary["secCode"] = df_doc_summary["secCode"].astype(int)
    idx = df_doc_summary[df_doc_summary['secCode']<1000].index
    df_doc_summary.loc[idx,'secCode'] = df_doc_summary.loc[idx,'secCode'] * 10
    doc_type_codes=['120','130','140','150']

    for doc_type_code in doc_type_codes:
        doc_type_name = doc_type_code_dict[doc_type_code]
        print(doc_type_name)
        save_dir = f"../data/raw/edinet/xbrl/{doc_type_name}"
        df_doc = df_doc_summary[df_doc_summary["docTypeCode"]==int(doc_type_code)]
        sec_codes = list(set(df_doc["secCode"]))
        sec_codes.sort()
        for sec_code in sec_codes:
            if not sec_code in code_to_company_name.keys():
                print(f"skip {sec_code}")
                continue
            company_name = code_to_company_name[sec_code]
            start_time = time.time()
            save_path = os.path.join(save_dir,str(sec_code))
            os.makedirs(save_path, exist_ok=True)
            df_sec = df_doc[df_doc["secCode"]==sec_code]
            for i in df_sec.index:
                date = df_sec.loc[i,'submitDateTime'][:10].split('-')
                xbrl_path = f"../data/raw/edinet/document/{date[0]}/{date[1]}/{date[2]}/{df_sec.loc[i,'docID']}/XBRL/PublicDoc/*.xbrl"
                glob_path = glob.glob(xbrl_path)
                if len(glob_path) > 0:
                    xbrl_path = glob_path[0]
                    filename = xbrl_path.split('/')[-1]
                    save_file_path = os.path.join(save_path,filename)
                    if not os.path.exists(save_file_path):
                        shutil.copyfile(xbrl_path, save_file_path)
                else:
                    print(f"Np Found {xbrl_path}")
            elapsed_time = round(time.time()-start_time,2)
            print(f"Copied {sec_code}: {elapsed_time}[sec]")
        print("")


def run():
    # start_date = datetime(2017,1, 1)
    # end_date = datetime(2021, 12, 31)
    # doc_type_codes=['120','130','140','150']
    # for date in date_range(start_date, end_date):
    #     download_all_documents(date, doc_type_codes)
    # summarize_doc_summary()
    copy_xbrl()

if __name__ == '__main__':
    run()