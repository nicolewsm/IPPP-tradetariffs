#!/usr/bin/env/python


import pandas as pd

years = ["1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004",
        "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013",
        "2014", "2015", "2016"]
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
        ctrytariffs['ctry'] = ctrycode
        ctrytariffs[product + '_tariff'] = temp[product]
        ctrytariffs[product + '_delta']= delta['delta']
        ctrytariffs[product + '_%change']= percent['%change']

    master = master.append(ctrytariffs)

master.to_csv("master_tariffs.csv")
