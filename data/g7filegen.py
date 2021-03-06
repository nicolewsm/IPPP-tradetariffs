#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

#Generating List of G7 countries CSV

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

g7 = ['Canada', 'Germany', 'France', 'Italy', 'United Kingdom', 'United States', 'Japan']
df_g7 = pd.DataFrame(np.array(g7), columns = ['ctryname'])
df_g7.set_index('ctryname')

df_gdp = pd.read_csv("gdp2.csv", index_col = "Country Name", usecols = ["Country Name", "Country Code"])
df_gdp.rename(columns = {'Country Name':'ctryname', "Country Code":'ctrycode' }, inplace = True)
df_gdp.index.names = ['ctryname']
df_gdp

masterctrycodeg7 = pd.DataFrame()
for country in g7:
    temp = df_gdp.loc[(df_gdp.index == country)]

    masterctrycodeg7 = masterctrycodeg7.append(temp)

#g7 Countries and Country Code
masterctrycodeg7.index.names = ['ctryname']

#country name and code for tariffs (European Union)
g7_fulllist = pd.DataFrame()
g7_fulllist['ctrycode'] = masterctrycodeg7['ctrycode'].replace({'DEU': 'EUN', 'FRA':'EUN', 'ITA':'EUN', 'GBR':'EUN'})
g7_fulllist.rename(columns = {'ctrycode': 'tariffcode'}, inplace = True)
g7_fulllist.index.names = ['ctryname']

#meging
df_g7ctrycode = masterctrycodeg7.merge(g7_fulllist, left_index=True, right_index=True, how='outer')

df_g7ctrycode.to_csv('g7ctrycodes_list.csv')

#Generating economic indicators G7 CSV

files = ["gdp2.csv", "lforce.csv", "unemp.csv", "inflation.csv"]
indicators = ["gdp", "lforce", "unemp", "inflation"]
indicators_lookup = dict(zip(files, indicators))

years = [str(i) for i in range(1996,2017)]
file_cols = ["Country Name"] + years
index_col = "Country Name"


df_g7 = pd.read_csv("g7ctrycodes_list.csv", index_col = "ctryname", usecols = ["tariffcode","ctryname","ctrycode"])


master = pd.DataFrame()
ctry = []
ctrycode = []
for file in files:
        df_current = pd.read_csv(file, index_col=index_col, usecols=file_cols)
        g7 = list(df_g7.index.values)

        df_current_master = pd.DataFrame()

        for country in g7:
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
            joined['ctrycode'] = df_g7.loc[country, 'ctrycode']
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
master.to_csv('G7_master.csv')

#Generating G7 tariffs CSV
years = [str(i) for i in range(1996,2017)]

file_cols = ["Product Group"] + years
index_col = "Product Group"

products = ["All Products", "Capital goods", "Consumer goods",
        "Intermediate goods", "Raw materials", "Animal", "Chemicals", "Food Products",
        "Footwear", "Fuels", "Hides and Skins", "Mach and Elec", "Metals", "Minerals",
        "Miscellaneous", "Plastic or Rubber", "Stone and Glass", "Textiles and Clothing",
        "Transportation", "Vegetable", "Wood"]

df_g7 = pd.read_csv("g7ctrycodes_list.csv", index_col = "tariffcode", usecols = ["tariffcode","ctryname","ctrycode"])

g7 = list(df_g7.index.values)


master = pd.DataFrame()

ctrytariffs = pd.DataFrame
ctrytariffs = ctrytariffs({'year': years})

for countrycode in g7:
    df_prep = pd.read_html("https://wits.worldbank.org/en/Widget/Country/"+countrycode+"/StartYear/1996/EndYear/2016/TradeFlow/Import/Partner/WLD/Product/all-groups/Indicator/MFN-WGHTD-AVRG/Show/1996;1997;1998;1999;2000;2001;2002;2003;2004;2005;2006;2007;2008;2009;2010;2011;2012;2013;2014;2015;2016/Sort/1996;desc/Metadata/Yes")
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
        ctrytariffs['countrycode'] = countrycode
        ctrytariffs[product + '_tariff'] = temp[product]
        ctrytariffs[product + '_delta']= delta['delta']
        ctrytariffs[product + '_%change']= percent['%change']

    master = master.append(ctrytariffs)
master.to_csv("g7_tariffs.csv")


df = pd.read_csv("g7_tariffs.csv")

europe = ['FRA', 'DEU', 'ITA', 'GBR']
 # to replace EUN with country codes of G7 nations.
x = 21
for ctry in europe:
     y = x + 20
     df.loc[x:y,'countrycode'] = ctry
     x += 21

df['year'] = df['year'].astype(str)
df["ctryyear"] = df["countrycode"].map(str) + df["year"]
df.to_csv("g7_tariffs.csv")
