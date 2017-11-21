#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

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
 
