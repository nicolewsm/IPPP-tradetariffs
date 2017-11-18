#!/usr/bin/env python

import pandas as pd

df_allgdp = pd.read_csv("gdp2.csv", index_col = "Country Name",
                    usecols = ["Country Name", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003",
                              "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015",
                              "2016"])

df_alllforce = pd.read_csv("lforce.csv", index_col = "Country Name",
                    usecols = ["Country Name", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003",
                              "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015",
                              "2016"])

df_allunemp = pd.read_csv("unemp.csv", index_col = "Country Name",
                    usecols = ["Country Name", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003",
                              "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015",
                              "2016"])

df_region = pd.read_csv("region.csv", index_col = "TableName", usecols = ["TableName", "Region", "IncomeGroup"])
df_region.index.names = ['Country Name']


df_gdp = df_region.join(df_allgdp)
df_gdp = df_gdp.loc[(df_gdp['Region'] == 'Latin America & Caribbean')]
df_gdp = df_gdp.drop(["Region", "IncomeGroup"], axis = 1)

df_lforce = df_region.join(df_alllforce)
df_lforce = df_lforce.loc[(df_lforce['Region'] == 'Latin America & Caribbean')]
df_lforce = df_lforce.drop(["Region", "IncomeGroup"], axis = 1)

df_unemp = df_region.join(df_allunemp)
df_unemp = df_unemp.loc[df_unemp['Region'] == 'Latin America & Caribbean']
df_unemp = df_unemp.drop(["Region", "IncomeGroup"], axis = 1)


latam = list(df_gdp.index.values)

#creating gdp dataframe
mastergdp = pd.DataFrame()
for country in latam:
    temp = df_gdp.loc[(df_gdp.index == country)]
    temp = temp.T.reset_index()
    temp.columns = ['year', 'gdpgrowth']

    delta = temp.set_index('year').diff()
    delta.columns = ['gdpdelta']

    percent = temp.set_index('year').pct_change()
    percent.columns = ['gdp%change']

    temp = temp.set_index('year')

    joined = temp.join(delta)
    joined = joined.join(percent)

    joined['ctry'] = country
    joined = joined.reset_index()

    mastergdp = mastergdp.append(joined)

mastergdp["ctryyear"] = mastergdp["ctry"].map(str) + mastergdp["year"]



#creating lforce master dataframe
masterlforce = pd.DataFrame()
for country in latam:
    temp = df_lforce.loc[(df_lforce.index == country)]
    temp = temp.T.reset_index()
    temp.columns = ['year', 'lforce']

    delta = temp.set_index('year').diff()
    delta.columns = ['lforcedelta']

    percent = temp.set_index('year').pct_change()
    percent.columns = ['lforce%change']

    temp = temp.set_index('year')

    joined = temp.join(delta)
    joined = joined.join(percent)

    joined['ctry'] = country
    joined = joined.reset_index()

    masterlforce = masterlforce.append(joined)

masterlforce["ctryyear"] = masterlforce["ctry"].map(str) + masterlforce["year"]


#creating lforce master dataframe
masterunemp = pd.DataFrame()
for country in latam:
    temp = df_unemp.loc[(df_unemp.index == country)]
    temp = temp.T.reset_index()
    temp.columns = ['year', 'unemp']

    delta = temp.set_index('year').diff()
    delta.columns = ['unempdelta']

    percent = temp.set_index('year').pct_change()
    percent.columns = ['unemp%change']

    temp = temp.set_index('year')

    joined = temp.join(delta)
    joined = joined.join(percent)

    joined['ctry'] = country
    joined = joined.reset_index()

    masterunemp = masterunemp.append(joined)

masterunemp["ctryyear"] = masterunemp["ctry"].map(str) + masterunemp["year"]


# creating master economic indicators dataframe
master = mastergdp.merge(masterlforce).set_index('ctryyear')

master = master.merge(masterunemp).set_index('ctryyear')

#creating multi index:
master.set_index(['ctry', 'year'], inplace=True)
master.to_csv('LatAm_master.csv')

#to clean:
# master_clean = master.dropna(axis=0, how = 'all')  #dropping rows with zero values
# droppedrows = master[~master.index.isin(master_clean.index)] #the countries dropped.

#to see the countries dropped
# droppedrows = droppedrows.reset_index()
# droppedrows.ctry.unique()
