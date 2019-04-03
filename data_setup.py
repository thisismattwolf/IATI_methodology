# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 10:22:31 2019

@author: Matthew Wolf
"""
import pandas as pd

def data_setup():
    import pandas as pd
    
    iati_fields = ['iati-identifier','reporting-org','default-language', 'title','description','start-planned','end-planned',\
                   'start-actual', 'end-actual','recipient-country-code','recipient-country', 'recipient-country-percentage',\
                   'sector','sector-code', 'sector-percentage','sector-vocabulary','sector-vocabulary-code', 'default-currency',\
                   'total-Commitment','total-Disbursement','total-Expenditure']
    field_nas =   {'iati-identifier':"",'reporting-org':"",'default-language':"", 'title':"",'description':"",'start-planned':"",'end-planned':"",\
                   'start-actual':"", 'end-actual':"",'recipient-country-code':"",'recipient-country':"", 'recipient-country-percentage':"",\
                   'sector':"",'sector-code':"", 'sector-percentage':"",'sector-vocabulary':"",'sector-vocabulary-code':"", 'default-currency':"",\
                   'total-Commitment':0,'total-Disbursement':0,'total-Expenditure':0}
    
    wbg_raw = pd.read_csv('WBG_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields)
    dfid_raw = pd.read_csv('DFID_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields)
    sida_raw = pd.read_csv('SIDA_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields)
    bmgf_raw = pd.read_csv('BMGF_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields)
    devco_raw = pd.read_csv('DEVCO_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields)
    gac_raw = pd.read_csv('GAC_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields)
    gf_raw = pd.read_csv('Global_Fund_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields)
    MFANe_raw = pd.read_csv('MFA_Netherlands_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields)
    
    dfs = [wbg_raw, dfid_raw, sida_raw, bmgf_raw, devco_raw, dfid_raw, gac_raw, gf_raw, MFANe_raw]
    
    data = pd.concat(dfs, ignore_index=True, sort=False)
    
    #Change names of reporting-orgs to abbreviations for simplicity
    data.loc[data['reporting-org'] == 'Sweden', 'reporting-org'] = 'Sida'
    data.loc[data['reporting-org'] == 'Department for International Development', 'reporting-org'] = 'DFID'
    data.loc[data['reporting-org'] == 'European Commission - Development and Cooperation-EuropeAid', 'reporting-org'] = 'DEVCO'
    data.loc[data['reporting-org'] == 'Foreign Affairs, Trade and Development Canada (DFATD)', 'reporting-org'] = 'GAC'
    data.loc[data['reporting-org'] == 'Ministry of Foreign Affairs (DGIS)', 'reporting-org'] = 'MFA Netherlands'
    data.loc[data['reporting-org'] == 'The Global Fund to Fight AIDS, Tuberculosis and Malaria', 'reporting-org'] = 'Global Fund'
    data.loc[data['reporting-org'] == 'Bill and Melinda Gates Foundation', 'reporting-org'] = 'B&MGF'
    
    #WB IATI data contains 30 random rows with incomplete data and a 'World Bank Group' reporting-org
    data.drop(data[data['reporting-org'] == 'World Bank Group'].index, inplace=True)
    
    # if there's no sector-vocabulary and no sector-vocabulary-code, drop the row
    #TODO - keep all dropped rows for later analysis in a dictionary {drop-logic: dropped df}
    #data.drop(data[(data['sector-vocabulary'].isnull()) & (data['sector-vocabulary-code'].isnull())].index, inplace=True)
    
    #fill in using the dict specified above
    data.fillna(value=field_nas)
    
    return data
    
def data_sectors(data, sectors):
    
    import pandas as pd
    results = pd.DataFrame()
    for sector in sectors:
        temp = data[data['sector-code'].str.contains(sector, na=False)]
        results = pd.concat([results, temp], ignore_index=True, sort=False)

    return results
    
def data_keywords(data, keywords):   
    
    import pandas as pd
    results = pd.DataFrame()
    for keyword in keywords:
        temp = data[(data['title'].str.lower().str.contains(keyword, na=False)) &\
                    (data['description'].str.lower().str.contains(keyword, na=False))]
        results = pd.concat([results, temp], ignore_index=True, sort=False)
        
    return results
    
# =============================================================================
# def data_psa_tag(data, psa_dict):
#     
#     import pandas as pd
#     results = pd.DataFrame
# =============================================================================

def data_investigate(data, sectors, keywords):
    
    sectors_data = data_sectors(data, sectors)
    keywords_data = data_keywords(data, keywords)
    inner = pd.merge(sectors_data, keywords_data, how="inner")
    outer = pd.merge(sectors_data, keywords_data, how="outer")
    
    def print_stats(df):
        print("Rows   : " + str(df.shape[0]))
        print("Columns: " + str(df.shape[1]) + "\n")
        print("Rows per donor: ")
        print(df.groupby(['reporting-org'])['iati-identifier'].count())
        print()
        print("Commitments per donor: ")
        print(df.groupby(['reporting-org'])['total-Commitment'].sum())
        print()
    
    print("For full data set:")
    print_stats(data)
    print("For data filtered by sectors:")
    print_stats(sectors_data)
    print("For data filtered by keywords:")
    print_stats(keywords_data)
    print("For inner join of sector-filtered data and keyword-filtered data:")
    print_stats(inner)
    print("For outer join of sector-filtered data and keyword-filtered data:")
    print_stats(outer)
    

sectors = ['13010', '13020', '13030', '13040', '13081']    
keywords = ["reproductive", "family planning", "contraceptive", "abortion", \
            "pregnancy", "sexual", "gender-based violence", "domestic violence",\
            "female genital mutilation", "fgm", "population census", "hiv", "std",\
            "aids", "obstetric", "antenatal", "perinatal","neonatal", "postnatal",\
            "newborn", "health personnel", "childhood", "immunization", "polio",\
            "measles", "tetanus", "congenital","disabilities", "breastfeeding"\
            "infant feeding", "doctor", "nurse", "midwive", "pharmacist", \
            "community health worker", "health specialists", "medical device",\
            "m-Health", "e-Health", "mobile health","health data", "medical products"\
            "health products", "medical services", "health services", "clinical studies"\
            "clinical trials", "medicine", "vaccine"]
data = data_setup()

data_investigate(data, sectors, keywords)