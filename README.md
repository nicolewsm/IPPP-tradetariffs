<h1> Trade Tariffs and Economic Development </h1>
<h2> Description and Scope </h2>
This project studies the consequences of trade policies on economic development, with the aim of determining if there were any differences between the experiences of developed countries and Latin American countries.  Given their different stages of development, we would expect that any changes in tariffs would impact Latin American countries more than developed countries.  Further, we also aim to identify if tariffs in different product classes (e.g. consumer goods or raw materials) would have different impact on economic development.  
<p>
Detailed analysis can be found in **analysis_final.ipynb** while a high-level review of our findings is available at this link: https://nicolewsm.github.io/IPPP-tradetariffs/docs/index.html

<h2> Data </h2>

Datafiles and codes generating them are found in the data folder.  Codes for pulling, merging and treating data are in **G7filegen.py** and **latamfilegen.py**.  Codes for cleaning both G7 and LatAm data are in **cleaning.py**.

Below is a brief description of the data used, and treatment administered.  Since this is a panel dataset, first differences were applied.  

**Source**:
<br>World Bank and World Integrated Trade Solution (WITS)

**Time Periods**:
<br>1996 - 2016 (Reporting of tariff data to WTO started only in 1996)

**Economic indicators**:
<br>GDP-per-capita growth (gpd2.csv), unemployment (unemp.csv), labor force participation (lforce.csv), inflation (inflation.csv)
<br>- Downloaded directly from the World Bank as csv, treated to generate year-on-year deltas and % changes
<br>- Merged to form G7_master.csv and LatAm_master.csv

**Tariffs**:
<br>Most-favored-nations weighted average tariffs for all products, intermediate, capital and consumer goods, and raw materials
<br>- Read directly from WITS using pandas, treated to generate year-on-year deltas and % changes
<br>- Merged to form G7_tariffs.csv and LatAm_master.csv

**Data cleaning**:
<br>Since we are unable to assess effects of tariff changes if no tariffs were reported, all countries/years that did not have tariff data were dropped.
<br>As each economic indicator is separately assessed, we dropped rows for which no data for that indicator was available.

<h2> Methodology</h2>

Taking into account that the effects of tariff changes would take time to manifest, we shift economic indicators by 2 such that we are comparing Year 0 tariff changes against Year 2 economic indicators. Analysis was conducted on 2 levels.  First, an OLS regression is performed for each economic indicator against tariffs on all products, and a separate regression on all the sub-categories of tariffs.

As we observed many data points clustered around zero (i.e. little or no change in tariffs or gdp growth/inflation/unemployment rates), we conducted a second level analysis by considering only changes above a threshold and graphing the changes on a bar chart.  

<h2> Summary of Findings </h2>
Overall, we did not find significant relationships between the economic indicators and tariff changes.  Nonetheless, it does also imply that tariffs should not be touted as a fix to economic problems.  

