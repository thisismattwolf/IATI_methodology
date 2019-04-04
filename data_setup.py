# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 10:22:31 2019

@author: Matthew Wolf
"""
import pandas as pd

def data_setup():
    
    """======================================
    This function loads and cleans IATI data from eight donors in preparation for 
    ANDE Methodology testing. This includes renaming the donors in the data, 
    deleting some incomplete rows of WBG data, and filling in blanks
    ======================================"""
    
    import pandas as pd
    
    # list of fields we to keep
    iati_fields = ['iati-identifier','reporting-org','default-language', 'title','description','start-planned','end-planned',\
                   'start-actual', 'end-actual','recipient-country-code','recipient-country', 'recipient-country-percentage',\
                   'sector','sector-code', 'sector-percentage','sector-vocabulary','sector-vocabulary-code', 'default-currency',\
                   'total-Commitment','total-Disbursement','total-Expenditure']
    
    # list of fields to import as datetimes
    date_fields = ['start-planned','end-planned','start-actual','end-actual']
    
    # dictionary of default NaN values for each of these columns
    field_nas =   {'iati-identifier':"",'reporting-org':"",'default-language':"", 'title':"",'description':"",'start-planned':"",'end-planned':"",\
                   'start-actual':"", 'end-actual':"",'recipient-country-code':"",'recipient-country':"", 'recipient-country-percentage':"",\
                   'sector':"",'sector-code':"", 'sector-percentage':"",'sector-vocabulary':"",'sector-vocabulary-code':"", 'default-currency':"",\
                   'total-Commitment':0,'total-Disbursement':0,'total-Expenditure':0}
    
    # locally saved CSV files for each of the eight donors
    #TODO - convert these read_csv calls to one or several IATI API call(s)
    wbg_raw = pd.read_csv('WBG_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields, parse_dates=date_fields)
    dfid_raw = pd.read_csv('DFID_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields, parse_dates=date_fields)
    sida_raw = pd.read_csv('SIDA_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields, parse_dates=date_fields)
    bmgf_raw = pd.read_csv('BMGF_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields, parse_dates=date_fields)
    devco_raw = pd.read_csv('DEVCO_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields, parse_dates=date_fields)
    gac_raw = pd.read_csv('GAC_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields, parse_dates=date_fields)
    gf_raw = pd.read_csv('Global_Fund_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields, parse_dates=date_fields)
    MFANe_raw = pd.read_csv('MFA_Netherlands_IATI_Activities_20190315.csv', low_memory=False, usecols=iati_fields, parse_dates=date_fields)
    
    #concatenate the data from each donor
    dfs = [wbg_raw, dfid_raw, sida_raw, bmgf_raw, devco_raw, dfid_raw, gac_raw, gf_raw, MFANe_raw]
    data = pd.concat(dfs, ignore_index=True, sort=False)
    
    #Change names of reporting-orgs to donor shortnames for simplicity
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
    
    data = data.reset_index()
    del data['index']
    
    return data
    
def data_sectors(data, sectors):
    
    """======================================
    This function takes a list of strings, each representing a IATI sector-code
    from any sector vocabulary. It filters the data and keeps any rows that are
    tagged with these sectors
    ======================================"""
    
    import pandas as pd
    results = pd.DataFrame()
    for sector in sectors:
        #for i in data.index:
         #   print(sector + " in " + str(data.at[i,'sector-code']) + " ?")
          #  print(sector in str(data.at[i,'sector-code']))
        temp = data[data['sector-code'].astype('str').str.contains(sector, na=False)]
        results = pd.concat([results, temp], ignore_index=True, sort=False)

    return results
    
def data_keywords(data, keywords):   
    
    """======================================
    This function takes a list of strings, each representing a text keyword in
    ALL LOWERCASE text. It filters the data by checking the title and description
    of each row for each keyword, keeping any rows where are least one keyword.
    ======================================"""
    
    import pandas as pd
    results = pd.DataFrame()
    for keyword in keywords:
        temp = data[(data['title'].str.lower().str.contains(keyword, na=False)) &\
                    (data['description'].str.lower().str.contains(keyword, na=False))]
        results = pd.concat([results, temp], ignore_index=True, sort=False)
        
    return results

def data_dates(data, startdate, enddate):
    pass

    

# =============================================================================
# def data_psa_tag(data, psa_dict):
#     
#     import pandas as pd
#     results = pd.DataFrame
# =============================================================================

def data_investigate(data, sectors, keywords):
    
    """======================================
    This function runs some diagnostic tests, for certain data, sectors, and
    keywords inputs. It shows how large the original dataset is, and its 
    breakdown by # of rows and sum of total funding commitments by donor, and
    shows this same breakdown again for the data after:
        1. Applying just the sector filter
        2. Applying just the keyword filter
        3. Inner joining the sector-filtered and keyword-filtered data
        4. Outer joining the sector-filtered and keyword-filtered data
    ======================================"""
    
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
    
    print("1. FOR FULL DATA SET:")
    print_stats(data)
    print("2. FOR SECTOR-FILTERED DATA:")
    print_stats(sectors_data)
    print("3. FOR KEYWORD-FILTERED DATA:")
    print_stats(keywords_data)
    print("4. FOR INNER JOIN OF SECTOR/KEYWORD-FILTERED DATA:")
    print_stats(inner)
    print("5. FOR OUTER JOIN OF SECTOR/KEYWORD-FILTERED DATA:")
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
