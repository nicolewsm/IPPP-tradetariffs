#!/usr/bin/env python

import pandas as pd
import numpy as np

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

g7 = ['Canada', 'Germany', 'France', 'Italy', 'United Kingdom', 'United States', 'Japan']
df_g7 = pd.DataFrame(np.array(g7), columns = ['Country Name'])
df_g7.set_index('Country Name')


#creating gdp master dataframe

mastergdp7 = pd.DataFrame()
for country in g7:
    temp = df_allgdp.loc[(df_allgdp.index == country)]
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

    mastergdp7 = mastergdp7.append(joined)

mastergdp7["ctryyear"] = mastergdp7["ctry"].map(str) + mastergdp7["year"]

#creating labor force master dataframe

masterlforce7 = pd.DataFrame()
for country in g7:
    temp = df_alllforce.loc[(df_alllforce.index == country)]
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

    masterlforce7 = masterlforce7.append(joined)

masterlforce7["ctryyear"] = masterlforce7["ctry"].map(str) + masterlforce7["year"]

# creating unemp master dataframe

masterunemp7 = pd.DataFrame()
for country in g7:
    temp = df_allunemp.loc[(df_allunemp.index == country)]
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

    masterunemp7 = masterunemp7.append(joined)

masterunemp7["ctryyear"] = masterunemp7["ctry"].map(str) + masterunemp7["year"]

#merging

master = mastergdp7.merge(masterlforce7).set_index('ctryyear')

master = master.merge(masterunemp7).set_index('ctryyear')

#creating multi index:
master.set_index(['ctry', 'year'], inplace=True)
master.to_csv('G7_master.csv')
