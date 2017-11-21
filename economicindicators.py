#!/usr/bin/env python

import pandas as pd 

files = ["gdp2.csv", "lforce.csv", "unemp.csv", "inflation.csv"]
indicators = ["gdp", "lforce", "unemp", "inflation"]
indicators_lookup = dict(zip(files, indicators))

file_cols = ["Country Name", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003",
          "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015",
          "2016"]
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
master = master[['ctry', 'ctrycode', 'year', 'gdp', 'gdpdelta', 'gdp%change','lforcedelta',
 'lforce%change', 'unemp', 'unempdelta', 'unemp%change', 'inflation', 'inflationdelta', 'inflation%change']]
# creating multi index:
# master.set_index(['ctry', 'year'], inplace=True)
master.to_csv('LatAm_master.csv')
