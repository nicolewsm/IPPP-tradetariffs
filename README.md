#IPPP-tradetariffs

Index of files created:

downloaded from WorldBank:
- gdp2.csv
- inflation.csv
- lforce.csv  
- unemp.csv
- region.csv
  -- region.csv contains the region classification & IncomeGroup for ALL countries.
  -- We merge region with each of the preceding economic indicator csv's
  -- Then from there, we .loc the LatAm countries.  

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
