#!/usr/bin/env python
import pandas as pd

tariffcols = ['ctryyear', 'All Products_tariff', 'All Products_delta', 'All Products_%change', 'Capital goods_tariff', 'Capital goods_delta',
              'Capital goods_%change', 'Consumer goods_tariff', 'Consumer goods_delta', 'Consumer goods_%change',
              'Intermediate goods_tariff', 'Intermediate goods_delta', 'Intermediate goods_%change',
              'Raw materials_tariff', 'Raw materials_delta', 'Raw materials_%change']
df_economic = pd.read_csv("LatAm_master.csv")
df_tariffs = pd.read_csv("latam_tariffs.csv", usecols = tariffcols)
df = df_economic.merge(df_tariffs)
#note that Haiti automatically gets dropped from the merge
#because it is not in df_tariffs.

#dropping all years = 1996  --> this is because we are looking at y-o-y deltas.
#since we started at 1996, the first set of deltas would be 1997
# e.g. GDP1997 - GDP1996
df = df[~(df['year'] == 1996)]


### VERSION 2 - dropping ALL rows with NaN -- 374 observations remains.
df_tariffs3 = df_tariffs.dropna()
df3 = df_economic.merge(df_tariffs3)
df3.to_csv("clean_latam.csv")
