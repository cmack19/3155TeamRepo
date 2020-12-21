# =============================================================================
# Dataframe manipulation file. Takes raw source data to reformat and exclude 
# unneeded items
# =============================================================================

import pandas as pd

df_efficiency = pd.read_csv('../Datasets/aid_efficiency1.csv')
df_efficiency2 = pd.read_csv('../Datasets/aid_efficiency2.csv')
df_efficiency3 = pd.read_csv('../Datasets/aid_efficiency3.csv')
df_efficiency23 = pd.read_csv('../Datasets/aid_efficiency23.csv')



df_country = pd.read_csv('../Datasets/country_est.csv')
df_global = pd.read_csv('../Datasets/reg_glob_est.csv')
df_totalpop = pd.read_excel('../Datasets/totalpopulation.xls',sheet_name='ESTIMATES',
                                    skiprows=range(0,16))
df_aid = pd.read_csv('../Datasets/netdevelopment.csv',skiprows=range(0,4))


df_aid.drop(['Indicator Name','Indicator Code'], axis='columns', inplace=True)
df_aid = pd.melt(df_aid,id_vars=['Country Name','Country Code'],var_name="Year",value_name="Aid")
df_aid = df_aid[df_aid.Year != '2020']


#======= Altering the df_country dataframe ====================================
df_country = df_country[df_country.Uncertainty != 'Lower']
df_country = df_country[df_country.Uncertainty != 'Upper']
df_country.drop(['Uncertainty'], axis='columns', inplace=True)
df_country.dropna
df_country = df_country.rename(columns={'ISO.Code': 'ISOCode', 'Country.Name': 'CountryName'})
df_country.drop(df_country.tail(1).index,inplace=True)
df_country.drop(['1955','1956','1957','1958','1959'], axis='columns', inplace=True)
df_country1 = df_country.copy(deep=False)
df_country = pd.melt(df_country,id_vars=['ISOCode','CountryName'], var_name="Year", value_name="Deaths")
#==============================================================================

#======= Altering the df_totalpop dataframe ====================================
df_totalpop.drop(['Index','Variant','Notes','Country code','Parent code','1950','1951','1952','1953','1954','2020'], axis='columns', inplace=True)
df_totalpop = df_totalpop[df_totalpop.Type != 'World']
df_totalpop = df_totalpop[df_totalpop.Type != 'Region']
df_totalpop = df_totalpop[df_totalpop.Type != 'Label/Separator']
df_totalpop = df_totalpop[df_totalpop.Type != 'Subregion']
df_totalpop = df_totalpop[df_totalpop.Type != 'Income Group']
df_totalpop = df_totalpop[df_totalpop.Type != 'Development Group']
df_totalpop = df_totalpop[df_totalpop.Type != 'Special other']
df_totalpop = df_totalpop[df_totalpop.Type != 'SDG region']
df_totalpop.drop(['Type'], axis='columns', inplace=True)
df_totalpop = df_totalpop.rename(columns={'Region, subregion, country or area *': 'CountryName'})
df_totalpop = pd.melt(df_totalpop,id_vars=['CountryName'],var_name="Year",value_name="Population")
#==============================================================================

#======= Merged dataframe; cases per capita ===================================
merged_df = pd.merge(df_country, df_totalpop,  how='left', left_on=['CountryName','Year'], right_on = ['CountryName','Year'])
merged_df['Deaths'] = merged_df['Deaths'].astype(float)
merged_df['Population'] = merged_df['Population'].astype(float)
merged_df['DeathsC'] = merged_df['Deaths']/merged_df['Population']

merged_df1 = pd.merge(merged_df, df_aid,  how='left', left_on=['ISOCode','Year'], right_on = ['Country Code','Year'])
merged_df1.drop(['Country Name','Country Code'], axis='columns', inplace=True)
merged_df1['AidC'] = merged_df1['Aid']/merged_df1['Population']
#==============================================================================
df_country1 = df_country1.set_index(['CountryName'])
df_country1.drop(['ISOCode'], axis='columns', inplace=True)
df_country1 = df_country1.T
df_country1.iloc[0] = 0
#======= Aid efficiency dataframe =============================================
df_efficiency3 = df_efficiency3.set_index(['Year'])
df_efficiency.iloc[0] = 0
unique_countries = list(df_efficiency3.columns.values) 

df_efficiency2.iloc[0] = 0
#==============================================================================

