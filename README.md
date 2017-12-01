<h1> Trade Tariffs and Economic Development </h1>
<h2> Description and Scope </h2>
This project studies the consequences of trade policies on economic development, with the aim of determining if there were any differences between the experiences of developed countries and Latin American countries.  Given their different stages of development, we would expect that any changes in tariffs would impact Latin American countries more than developed countries.  Further, we also aim to identify if tariffs in different product classes (e.g. consumer goods or raw materials) would have different impact on economic development.  

Detailed analysis can be found in the... while a high-level review of our findings is available at this link: https://nicolewsm.github.io/IPPP-tradetariffs/docs/index.html

<h2> Data </h2>

Datafiles and codes generating them are found in the data folder.  Below is a brief description of the data used, and treatment administered.  Since this is a panel dataset, first differences were applied.  

**Source**:
<br>World Bank and World Integrated Trade Solution (WITS)

**Time Periods**:
<br>1996 - 2016 (Reporting of tariff data to WTO started only in 1996)

**Economic indicators**:
<br>GDP-per-capita growth (gpd2.csv), unemployment (unemp.csv), labor force participation (lforce.csv), inflation (inflation.csv)
<br>- Downloaded directly from the World Bank as csv, treated to generate year-on-year deltas and % changes
<br>- Merged to form G7_master.csv and LatAm_master.csv
<br>- Codes for merging data are at **G7filegen.py** and **latamfilegen.py**

**Tariffs**:
<br>Most-favored-nations weighted average tariffs for all products, intermediate, capital and consumer goods, and raw materials
<br>- Read directly from WITS using pandas, treated to generate year-on-year deltas and % changes
<br>- Merged to form G7_tariffs.csv and LatAm_master.csv
<br>- Codes for merging data are at G7filegen.py and latamfilegen.py

**Data cleaning**:
<br>Since we are unable to assess effects of tariff changes if no tariffs were reported, all countries/years that did not have tariff data were dropped.
<br>As each economic indicator is separately assessed, we dropped rows for which no data for that indicator was available.
<br>The resulting LatAm dataset has 419 observations for gdp, 385 for unemployment and labor force rates, and 408 for inflation.

<h2> Methodology</h2>

Taking into account that the effects of tariff changes would take time to manifest, we shift economic indicators by 2 such that we are comparing Year 0 tariff changes against Year 2 economic indicators. 


