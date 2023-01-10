import os
import glob
import pickle
import pandas as pd
from arelle import Cntlr
from xbrl_to_csv import *



def get_data_from_xbrl(xbrl_file, save_path):
    ctrl = Cntlr.Cntlr(logFileName='logToPrint')
    try:
        model_xbrl = ctrl.modelManager.load(xbrl_file)
        try:
            head = [
                '名前空間',
                '日本語', '英語',
                '接頭辞', 'タグ', 'ファクトID',
                '値', '単位', '貸借',
                '開始日', '終了日', '時点(期末日)',
                'コンテキストID', 'シナリオ',
                ]
            fact_datas = [head]

            for fact in model_xbrl.facts:
                label_ja = fact.concept.label(preferredLabel=None, lang='ja', linkroleHint=None)
                label_en = fact.concept.label(preferredLabel=None, lang='en', linkroleHint=None)
                x_value = fact.xValue
                if fact.unit is None:
                    unit = None
                else:
                    unit = fact.unit.value
                if fact.context.startDatetime:
                    start_date = fact.context.startDatetime
                else:
                    start_date = None
                if fact.context.endDatetime:
                    end_date = fact.context.endDatetime
                else:
                    end_date = None
                if fact.context.endDatetime:
                    instant_date = fact.context.instantDatetime
                else:
                    instant_date = None
                scenario_datas = []
                for (dimension, dim_value) in fact.context.scenDimValues.items():
                    scenario_datas.append([
                                    dimension.label(preferredLabel=None, lang='ja', linkroleHint=None),
                                    dimension.id,
                                    dim_value.member.label(preferredLabel=None, lang='ja', linkroleHint=None),
                                    dim_value.member.id,
                                    ])
                if len(scenario_datas) == 0:
                    scenario_datas = None
                fact_datas.append([
                                fact.namespaceURI,
                                label_ja,
                                label_en,
                                fact.prefix,
                                fact.localName,
                                fact.id,
                                x_value,
                                unit,
                                fact.concept.balance,
                                start_date,
                                end_date,
                                instant_date,
                                fact.contextID,
                                scenario_datas
                                ])
                
            df = pd.DataFrame(fact_datas[1:],columns=fact_datas[0])
            df.to_csv(save_path)
        finally:
            ctrl.modelManager.close()
    finally:
        ctrl.close()


def write_html_files_path(xbrl_paths):
    save_path = '../data/preprocess/edinet/etc/open_html_files.txt'
    if os.path.exists(save_path):
        os.remove(save_path)
    for xbrl_path in xbrl_paths:
        html_paths = glob.glob(os.path.join(*xbrl_path.split('/')[:-1], '0101010_honbun_*.htm'))
        for html_path in html_paths:
            path = f"file://{os.path.abspath(html_path).replace('root',root_path)}"
            with open(save_path,'a') as f:
                print(path, file=f)


def check_null_files(label="売上高"):
    paths = glob.glob("../data/preprocess/edinet/有価証券報告書/Consolidated/*.csv")
    unfound_files_list = []
    unfound_codes_list = []
    skip_wors = ["銀行", "金庫", "保険"]
    print(f"total files: {len(paths)}")
    for i,path in enumerate(paths):
        if i != 0 and i%1000==0:
            print(i)
        flag = False
        for sw in skip_wors:
            if sw in path:
                flag = True
                break
        if flag:
            continue
        df = pd.read_csv(path, index_col=0).T
        if df.isnull().sum()[label]==len(df):
            path = path.replace("Consolidated","NonConsolidated")
            df = pd.read_csv(path, index_col=0).T
            if df.isnull().sum()[label]==len(df):
                file_name = path.split('/')[-1]
                ticker = file_name.split('_')[0]
                unfound_files_list.append(file_name)
                unfound_codes_list.append(ticker)
    print(f"unfound files: {len(unfound_files_list)}")
    with open(f"../data/preprocess/edinet/etc/unfound_{label}_files_list.pkl", "wb") as fp:
        pickle.dump(unfound_files_list, fp)
    with open(f"../data/preprocess/edinet/etc/unfound_{label}_codes_list.txt", "w") as f:
        print(unfound_codes_list, file=f)
    
    print("Done")


def delete_files(label="売上高"):
    load_path = f"../data/preprocess/edinet/etc/unfound_{label}_files_list.pkl"
    with open(load_path, "rb") as f:
        unfound_files_list = pickle.load(f)
        
    for file_name in unfound_files_list:
        paths = glob.glob(f"../data/preprocess/edinet/有価証券報告書/*/{file_name}")
        for path in paths:
            os.remove(path)


def create_xbrl_summary(sec_codes=None, doc_type_code=120, label="売上高"):
    save_dir = f'../data/preprocess/edinet/etc//xbrl_summary/'
    os.makedirs(save_dir, exist_ok=True)
    df_doc_all_summary = pd.read_csv('../data/preprocess/edinet/doc_all_summary.csv')
    if not sec_codes:
        load_path = f"../data/preprocess/edinet/etc/unfound_{label}_files_list.pkl"
        with open(load_path, "rb") as f:
            unfound_files_list = pickle.load(f)
        sec_codes = [int(file_name.split('_')[0]) for file_name in unfound_files_list]
    for sec_code in sec_codes:
        df_doc_summary = select_doc_summary(df_doc_all_summary, doc_type_code, sec_code)
        doc_id = df_doc_summary['docID'].values[0]
        xbrl_paths = get_xbrl_paths(df_doc_summary)
        if len(xbrl_paths) > 0:
            xbrl_path = xbrl_paths[0]
            save_path = os.path.join(save_dir,f'{sec_code}_{doc_id}.csv')
            if os.path.exists(save_path):
                continue
            else:
                get_data_from_xbrl(xbrl_path, save_path)
                print(f"create xbrl summary in {sec_code}_{doc_id}")
        else:
            print(f"no xbrl file in {sec_code}")

def run():
    check_null_files()
    create_xbrl_summary()
    # delete_files()
    # write_html_files_path(xbrl_paths)


if __name__ == '__main__':
    run()