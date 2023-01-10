import os
import json

save_dir = "../data/raw/edinet/taxonomy/"

def get_context_ref(types, additional_word=""):
    context_ref = [f"Prior{i}Year{types}{additional_word}" for i in reversed(range(1,5))]
    context_ref.append(f"CurrentYear{types}{additional_word}")
    return context_ref


def japan_gaap_taxonomy(edinet_code="E00000"):
    file_name = "Taxonomy_Japan GAAP_有価証券報告書_Consolidated.json"
    taxonomy = {
        "売上高":{
            "key":[
                "jpcrp_cor:NetSalesSummaryOfBusinessResults",
                "jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults",
                "jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults",
                "jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults",
                f"jpcrp030000-asr_{edinet_code}-000:IncomeIFRSKeyFinancialData",
                f"jpcrp030000-asr_{edinet_code}-000:BusinessRevenueSummaryOfBusinessResults",
                f"jpcrp030000-asr_{edinet_code}-000:OperatingRevenueSummaryOfBusinessResults",
                f"jpcrp030000-asr_{edinet_code}-000:NetSalesAndOperatingRevenueSummaryOfBusinessResults",
                f"jpcrp030000-asr_{edinet_code}-000:NetSalesAndOperatingRevenue2SummaryOfBusinessResults",
                f"jpcrp030000-asr_{edinet_code}-000:NetSalesAndOtherOperatingRevenueSummaryOfBusinessResults",
                f"jpcrp030000-asr_{edinet_code}-000:NetSalesOfCompletedConstructionContractsSummaryOfBusinessResults"
            ],
            "context_ref":get_context_ref("Duration")
        },
        "経常利益":{
            "key":"jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "当期純利益":{
            "key":"jpcrp_cor:ProfitLossAttributableToOwnersOfParentSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "純資産額":{
            "key":"jpcrp_cor:NetAssetsSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant")
        },
        "総資産額":{
            "key":"jpcrp_cor:TotalAssetsSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant")
        },
        "BPS（１株当たり純資産額）":{
            "key":"jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant")
        },
        "EPS（１株当たり当期純利益）":{
            "key":"jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "自己資本比率":{
            "key":"jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant")
        },
        "ROE（自己資本利益率）":{
            "key":"jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "PER（株価収益率）":{
            "key":"jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "営業CF":{
            "key":"jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "投資CF":{
            "key":"jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "財務CF":{
            "key":"jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "期末残高":{
            "key":"jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant")
        },
        "従業員数":{
            "key":"jpcrp_cor:NumberOfEmployees",
            "context_ref":get_context_ref("Instant")
        },
        "発行済株式総数":{
            "key":"jpcrp_cor:TotalNumberOfIssuedSharesSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        }
    }
    return file_name, taxonomy
    

def japan_gaap_nonconsolidated_taxonomy(edinet_code="E00000"):
    file_name = "Taxonomy_Japan GAAP_有価証券報告書_NonConsolidated.json"
    taxonomy = {
        "売上高":{
            "key":[
                "jpcrp_cor:NetSalesSummaryOfBusinessResults",
                "jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults",
                "jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults",
                "jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults",
                f"jpcrp030000-asr_{edinet_code}-000:IncomeIFRSKeyFinancialData",
                f"jpcrp030000-asr_{edinet_code}-000:BusinessRevenueSummaryOfBusinessResults",
                f"jpcrp030000-asr_{edinet_code}-000:OperatingRevenueSummaryOfBusinessResults",
                f"jpcrp030000-asr_{edinet_code}-000:NetSalesAndOperatingRevenueSummaryOfBusinessResults",
                f"jpcrp030000-asr_{edinet_code}-000:NetSalesAndOperatingRevenue2SummaryOfBusinessResults",
                f"jpcrp030000-asr_{edinet_code}-000:NetSalesAndOtherOperatingRevenueSummaryOfBusinessResults",
                f"jpcrp030000-asr_{edinet_code}-000:NetSalesOfCompletedConstructionContractsSummaryOfBusinessResults"
            ],
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "経常利益":{
            "key":"jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "当期純利益":{
            "key":"jpcrp_cor:NetIncomeLossSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "純資産額":{
            "key":"jpcrp_cor:NetAssetsSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "総資産額":{
            "key":"jpcrp_cor:TotalAssetsSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "BPS（１株当たり純資産額）":{
            "key":"jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "EPS（１株当たり当期純利益）":{
            "key":"jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "自己資本比率":{
            "key":"jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "ROE（自己資本利益率）":{
            "key":"jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "PER（株価収益率）":{
            "key":"jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "営業CF":{
            "key":"jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "投資CF":{
            "key":"jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "財務CF":{
            "key":"jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "期末残高":{
            "key":"jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "従業員数":{
            "key":"jpcrp_cor:NumberOfEmployees",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "発行済株式総数":{
            "key":"jpcrp_cor:TotalNumberOfIssuedSharesSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        }
    }
    return file_name, taxonomy


def ifrs_taxonomy(edinet_code="E00000"):
    file_name = "Taxonomy_IFRS_有価証券報告書_Consolidated.json"
    taxonomy = {
        "売上高":{
            "key":[
                "jpcrp_cor:RevenueIFRSSummaryOfBusinessResults",
                "NetSalesIFRSSummaryOfBusinessResults",
                "ifrs-full:Revenue",
                f"jpcrp030000-asr_{edinet_code}-000:NetSalesIFRSSummaryOfBusinessResults"
                
            ],
            "context_ref":get_context_ref("Duration")
        },
        "経常利益":{
            "key":"jpcrp_cor:ProfitLossBeforeTaxIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "当期純利益":{
            "key":"jpcrp_cor:ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "純資産額":{
            "key":"jpcrp_cor:EquityAttributableToOwnersOfParentIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant")
        },
        "総資産額":{
            "key":[
                "jpcrp_cor:TotalAssetsIFRSSummaryOfBusinessResults",
                "jpcrp_cor:TotalEquityIFRSSummaryOfBusinessResults"
            ],
            "context_ref":get_context_ref("Instant")
        },
        "BPS（１株当たり純資産額）":{
            "key":"jpcrp_cor:EquityToAssetRatioIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant")
        },
        "EPS（１株当たり当期純利益）":{
            "key":"jpcrp_cor:DilutedEarningsLossPerShareIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "自己資本比率":{
            "key":"jpcrp_cor:RatioOfOwnersEquityToGrossAssetsIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant")
        },
        "ROE（自己資本利益率）":{
            "key":"jpcrp_cor:RateOfReturnOnEquityIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "PER（株価収益率）":{
            "key":"jpcrp_cor:PriceEarningsRatioIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "営業CF":{
            "key":"jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "投資CF":{
            "key":"jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "財務CF":{
            "key":"jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "期末残高":{
            "key":"jpcrp_cor:CashAndCashEquivalentsIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant")
        },
        "従業員数":{
            "key":"jpcrp_cor:NumberOfEmployeesIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant")
        },
        "発行済株式総数":{
            "key":"jpcrp_cor:TotalNumberOfIssuedSharesSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        }
    }
    return file_name, taxonomy


def ifrs_nonconsolidated_taxonomy(edinet_code="E00000"):
    file_name = "Taxonomy_IFRS_有価証券報告書_NonConsolidated.json"
    taxonomy = {
        "売上高":{
            "key":"jpcrp_cor:RevenueIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "経常利益":{
            "key":"jpcrp_cor:ProfitLossBeforeTaxIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "当期純利益":{
            "key":"jpcrp_cor:ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "純資産額":{
            "key":[
                "jpcrp_cor:EquityAttributableToOwnersOfParentIFRSSummaryOfBusinessResults",
                "jpcrp_cor:NetAssetsSummaryOfBusinessResults"
            ],
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "総資産額":{
            "key":"jpcrp_cor:TotalAssetsIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "BPS（１株当たり純資産額）":{
            "key":"jpcrp_cor:EquityToAssetRatioIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "EPS（１株当たり当期純利益）":{
            "key":"jpcrp_cor:DilutedEarningsLossPerShareIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "自己資本比率":{
            "key":"jpcrp_cor:RatioOfOwnersEquityToGrossAssetsIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "ROE（自己資本利益率）":{
            "key":"jpcrp_cor:RateOfReturnOnEquityIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "PER（株価収益率）":{
            "key":"jpcrp_cor:PriceEarningsRatioIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "営業CF":{
            "key":"jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "投資CF":{
            "key":"jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "財務CF":{
            "key":"jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "期末残高":{
            "key":"jpcrp_cor:CashAndCashEquivalentsIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "従業員数":{
            "key":"jpcrp_cor:NumberOfEmployeesIFRSSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "発行済株式総数":{
            "key":"jpcrp_cor:TotalNumberOfIssuedSharesSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        }
    }
    return file_name, taxonomy


def us_gaap_taxonomy(edinet_code="E00000"):
    file_name = "Taxonomy_US GAAP_有価証券報告書_Consolidated.json"
    taxonomy = {
        "売上高":{
            "key":"jpcrp_cor:RevenuesUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "経常利益":{
            "key":"jpcrp_cor:ProfitLossBeforeTaxUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "当期純利益":{
            "key":"jpcrp_cor:NetIncomeLossAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "純資産額":{
            "key":"jpcrp_cor:EquityAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant")
        },
        "総資産額":{
            "key":"jpcrp_cor:TotalAssetsUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant")
        },
        "BPS（１株当たり純資産額）":{
            "key":"jpcrp_cor:EquityAttributableToOwnersOfParentPerShareUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant")
        },
        "EPS（１株当たり当期純利益）":{
            "key":"jpcrp_cor:DilutedEarningsLossPerShareUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "自己資本比率":{
            "key":"jpcrp_cor:EquityToAssetRatioUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant")
        },
        "ROE（自己資本利益率）":{
            "key":"jpcrp_cor:RateOfReturnOnEquityUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "PER（株価収益率）":{
            "key":"jpcrp_cor:PriceEarningsRatioUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "営業CF":{
            "key":"jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "投資CF":{
            "key":"jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "財務CF":{
            "key":"jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration")
        },
        "期末残高":{
            "key":"jpcrp_cor:CashAndCashEquivalentsUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant")
        },
        "従業員数":{
            "key":"jpcrp_cor:NumberOfEmployees",
            "context_ref":get_context_ref("Instant")
        },
        "発行済株式総数":{
            "key":"jpcrp_cor:TotalNumberOfIssuedSharesSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        }
    }
    return file_name, taxonomy


def us_gaap_nonconsolidated_taxonomy(edinet_code="E00000"):
    file_name = "Taxonomy_US GAAP_有価証券報告書_NonConsolidated.json"
    taxonomy = {
        "売上高":{
            "key":"jpcrp_cor:NetSalesSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "経常利益":{
            "key":"jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "当期純利益":{
            "key":"jpcrp_cor:NetIncomeLossSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "純資産額":{
            "key":"jpcrp_cor:NetAssetsSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "総資産額":{
            "key":"jpcrp_cor:TotalAssetsSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "BPS（１株当たり純資産額）":{
            "key":"jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "EPS（１株当たり当期純利益）":{
            "key":"jpcrp_cor:DilutedEarningsPerShareSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "自己資本比率":{
            "key":"jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "ROE（自己資本利益率）":{
            "key":"jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "PER（株価収益率）":{
            "key":"jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "営業CF":{
            "key":"jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "投資CF":{
            "key":"jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "財務CF":{
            "key":"jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Duration","_NonConsolidatedMember")
        },
        "期末残高":{
            "key":"jpcrp_cor:CashAndCashEquivalentsUSGAAPSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "従業員数":{
            "key":"jpcrp_cor:NumberOfEmployees",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        },
        "発行済株式総数":{
            "key":"jpcrp_cor:TotalNumberOfIssuedSharesSummaryOfBusinessResults",
            "context_ref":get_context_ref("Instant","_NonConsolidatedMember")
        }
    }
    return file_name, taxonomy


def run():
    taxonomy_functions = [
        japan_gaap_taxonomy,
        japan_gaap_nonconsolidated_taxonomy,
        ifrs_taxonomy,
        ifrs_nonconsolidated_taxonomy,
        us_gaap_taxonomy,
        us_gaap_nonconsolidated_taxonomy,
    ]
    for taxonomy_function in taxonomy_functions:
        file_name, taxonomy = taxonomy_function()
        save_path = os.path.join(save_dir, file_name)
        with open(save_path, mode="w" ,encoding="utf-8") as f:
            json.dump(taxonomy, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    run()