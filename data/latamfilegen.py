#!/usr/bin/env python

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

#Generating List of LatAm countries CSV

countrylist = requests.get("http://wits.worldbank.org/API/V1/wits/datasource/trn/country/ALL")

soup = bs(countrylist.content, "xml")

rows = soup.find_all("wits:country")
rows

d = {"ctrycode" : [], "ctryname" : [], "isReporter" : []}
for tag in rows:
    d["ctrycode"].append(tag.contents[1].contents[0])
    d["ctryname"].append(tag.contents[3].contents[0])
    d["isReporter"].append(tag.get('isreporter'))

df = pd.DataFrame
df = df.from_dict(d)
df2 = df.loc[df['isReporter'] == '1']

df_region = pd.read_csv("region.csv", index_col = "TableName", usecols = ["TableName", "Region", "IncomeGroup", "Country Code"])
df_region.index.names = ['ctryname']
df_region = df_region.loc[(df_region['Region'] == 'Latin America & Caribbean')]

latam_fulllist = pd.DataFrame()
latam_fulllist['ctryname'] = df_region.index.values
df_latam = latam_fulllist.merge(df2)
df_latam.to_csv('latamctrycodes_list.csv')

#Generating LatAm economic indicators CSV

files = ["gdp2.csv", "lforce.csv", "unemp.csv", "inflation.csv"]
indicators = ["gdp", "lforce", "unemp", "inflation"]
indicators_lookup = dict(zip(files, indicators))

years = [str(i) for i in range(1996,2017)]
file_cols = ["Country Name"] + years
index_col = "Country Name"

df_region = pd.read_csv("region.csv", index_col = "TableName", usecols = ["TableName", "Region", "IncomeGroup"])
df_region.index.names = ['Country Name']

df_latam = pd.read_csv("latamctrycodes_list.csv", index_col = 'ctryname', usecols = ['ctryname', 'ctrycode'])

master = pd.DataFrame()
ctry = []
ctrycode = []
for file in files:
        df_all = pd.read_csv(file, index_col=index_col, usecols=file_cols)
        df_current = df_region.join(df_all)
        df_current = df_current.loc[(df_current['Region'] == 'Latin America & Caribbean')]
        df_current = df_current.drop(["Region", "IncomeGroup"], axis = 1)

        latam = list(df_latam.index.values)

        df_current_master = pd.DataFrame()

        for country in latam:
            temp = df_current.loc[(df_current.index == country)]
            temp = temp.T.reset_index()
            temp.columns = ['year', indicators_lookup[file]]

            delta = temp.set_index('year').diff()
            delta.columns = [indicators_lookup[file] + 'delta']

            percent = temp.set_index('year').pct_change()
            percent.columns = [indicators_lookup[file] + '%change']

            temp = temp.set_index('year')

            joined = temp.join(delta)
            joined = joined.join(percent)

            joined['ctry'] = country
            joined['ctrycode'] = df_latam.loc[country, 'ctrycode']
            joined = joined.reset_index()

            df_current_master = df_current_master.append(joined)

        df_current_master["ctryyear"] = df_current_master["ctrycode"].map(str) + df_current_master["year"]

        if master.empty:
            master = df_current_master
        else:
            master = master.merge(df_current_master).set_index('ctryyear')

#rearranging columns
master = master[['ctry', 'ctrycode', 'year', 'gdp', 'gdpdelta', 'gdp%change', 'lforce', 'lforcedelta',
 'lforce%change', 'unemp', 'unempdelta', 'unemp%change', 'inflation', 'inflationdelta', 'inflation%change']]
# creating multi index:
master.to_csv('LatAm_master.csv')

#Generating Tariffs CSV

years = [str(i) for i in range(1996,2017)]

file_cols = ["Product Group"] + years
index_col = "Product Group"

products = ["All Products", "Capital goods", "Consumer goods",
        "Intermediate goods", "Raw materials", "Animal", "Chemicals", "Food Products",
        "Footwear", "Fuels", "Hides and Skins", "Mach and Elec", "Metals", "Minerals",
        "Miscellaneous", "Plastic or Rubber", "Stone and Glass", "Textiles and Clothing",
        "Transportation", "Vegetable", "Wood"]

latam = ['ABW','ARG', 'ATG', 'BHS', 'BLZ', 'BOL', 'BRA', 'BRB', 'CHL', 'COL', 'CRI', 'CUB', 'DMA', 'DOM', 'ECU', 'GRD', 'GTM', 'GUY',
 'HND',  'JAM', 'KNA', 'LCA', 'MEX', 'NIC', 'PAN', 'PER', 'PRY', 'SLV', 'SUR', 'TTO', 'URY', 'VCT']

master = pd.DataFrame()

ctrytariffs = pd.DataFrame
ctrytariffs = ctrytariffs({'year': years})

for ctrycode in latam:
    df_prep = pd.read_html("https://wits.worldbank.org/en/Widget/Country/"+ctrycode+"/StartYear/1996/EndYear/2016/TradeFlow/Import/Partner/WLD/Product/all-groups/Indicator/MFN-WGHTD-AVRG/Show/1996;1997;1998;1999;2000;2001;2002;2003;2004;2005;2006;2007;2008;2009;2010;2011;2012;2013;2014;2015;2016/Sort/1996;desc/Metadata/Yes")
    df_orig = pd.concat(df_prep)
    df_orig = df_orig.set_index('Product Group')

    for product in products:
        temp = df_orig.loc[(df_orig.index==product)]
        temp = temp.T.reset_index()
        temp.rename(columns={'index': 'year'}, inplace=True)

        delta = temp.set_index('year').diff()
        delta.rename(columns={product: 'delta'}, inplace=True)
        delta = delta.reset_index(drop=True)

        percent = temp.set_index('year').pct_change()
        percent.rename(columns={product: '%change'}, inplace=True)
        percent = percent.reset_index(drop=True)

        #the problem starts from here onwards.
        ctrytariffs['ctrycode'] = ctrycode
        ctrytariffs[product + '_tariff'] = temp[product]
        ctrytariffs[product + '_delta']= delta['delta']
        ctrytariffs[product + '_%change']= percent['%change']


    master = master.append(ctrytariffs)
master["ctryyear"] = master["ctrycode"].map(str) + master["year"]
master.to_csv("latam_tariffs.csv")
