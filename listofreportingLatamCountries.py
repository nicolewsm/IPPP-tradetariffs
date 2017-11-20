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

df_allgdp = pd.read_csv("gdp2.csv", index_col = "Country Name",
                    usecols = ["Country Name", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003",
                              "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015",
                              "2016"])

df_region = pd.read_csv("region.csv", index_col = "TableName", usecols = ["TableName", "Region", "IncomeGroup"])
df_region.index.names = ['Country Name']

df_gdp = df_region.join(df_allgdp)
df_gdp = df_gdp.loc[(df_gdp['Region'] == 'Latin America & Caribbean')]
df_gdp = df_gdp.drop(["Region", "IncomeGroup"], axis = 1)

latam_fulllist = pd.DataFrame()
latam_fulllist['ctryname'] = df_gdp.index.values
df_latam = df2.merge(latam_fulllist)
latam = df_latam['ctryname'].tolist()
latam_codes = df_latam['ctrycode'].tolist()
