#!/usr/bin/env python
import pandas as pd

tariffcols = ['ctryyear', 'All Products_tariff', 'All Products_delta', 'All Products_%change', 'Capital goods_tariff', 'Capital goods_delta',
              'Capital goods_%change', 'Consumer goods_tariff', 'Consumer goods_delta', 'Consumer goods_%change',
              'Intermediate goods_tariff', 'Intermediate goods_delta', 'Intermediate goods_%change',
              'Raw materials_tariff', 'Raw materials_delta', 'Raw materials_%change']
latam_economic = pd.read_csv("LatAm_master.csv")
latam_tariffs = pd.read_csv("latam_tariffs.csv", usecols = tariffcols)
latam = latam_economic.merge(latam_tariffs)
#note that Haiti automatically gets dropped from the merge
#because it is not in df_tariffs.

#dropping all years = 1996  --> this is because we are looking at y-o-y deltas.
#since we started at 1996, the first set of deltas would be 1997
# e.g. GDP1997 - GDP1996
latam = latam[~(latam['year'] == 1996)]

latam_tariffs = latam_tariffs.dropna()
latam = latam_economic.merge(latam_tariffs)
latam.to_csv("clean_latam.csv")


g7_economic = pd.read_csv("G7_master.csv")
g7_tariffs = pd.read_csv("g7_tariffs.csv", usecols = tariffcols)
g7 = g7_economic.merge(g7_tariffs)

g7 = g7[~(g7['year'] == 1996)]
g7_tariffs = g7_tariffs.dropna()
g7_clean = g7_economic.merge(g7_tariffs)
g7_clean.to_csv("clean_g7.csv")
