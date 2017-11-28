<h1> Trade Tariffs and Economic Development </h1>
<h2> Description and Scope </h2>
This project studies the consequences of trade policies on economic development, with the aim of determining if there were any differences between the experiences of developed countries and Latin American countries.  Given their different stages of development, we would expect that any changes in tariffs would impact Latin American countries more than developed countries.  Further, we also aim to identify if tariffs in different product classes (e.g. consumer goods or raw materials) would have different impact on economic development.  

<h2> Data </h2>
**Source**: 
<br>World Bank and World Integrated Trade Solution (WITS)

**Time Periods**: 
<br>1996 - 2016 (Reporting of tariff data to WTO started only in 1996) 
<br>

**Economic indicators**: 
<br>GDP-per-capita growth, unemployment, labor force participation, inflation
<br>- Downloaded directly from the World Bank as csv, treated to generate year-on-year deltas and % changes 
<br>- Merged to form master csv files for G7 and LatAm countries

**Tariffs**: 
<br>Most-favored-nations weighted average tariffs for all products, intermediate, capital and consumer goods, and raw materials 
<br>- Read directly from WITS using pandas, treated to generate year-on-year deltas and % changes
<br>- Merged to form tariff csv files for G7 and LatAm countries

**NOTE:  Run the following codes in order!**

listofreportingLatamCountries.py
- creates 'latamctrycodes_list.csv'
  - this should be our master list of all LatAm countries that report data to WITS
  - in concept, this is a subset of the LatAm countries we found from region.csv
- list of LatAm countries that report data to the WITS
- contains 'ctryname',	'ctrycode', 'isReporter'
- To create this, we had to make use of region.csv to get the region classifications as well.  

economicindicators.py
- For the LatAm countries:
- Creates a master file ('LatAm_master.csv') that sets out the following:
  - gdp-per-capita growth rates
  - labor force participation rates
  - unemployment rates
  - inflation rates
- contains the rates as mentioned, their y-o-y deltas and %pct_change

tariffs.py
**NOTE: Takes some 10-20seconds to run.***
- creates 'latam_tariffs.csv'
- Note that I should have used latamctrycodes_list.csv to get the ctrycodes.  
  - However, this was a problem, because HTI had zero data.  Using the csv would have caused errors.
  - Hence, there is a list called 'latam' which I used to generate the URLs.

**** need to clean to drop countries with *zero* data.  
