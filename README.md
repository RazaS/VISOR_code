# VISOR_code

This project focussed on downloading 20 years of weather reports from Climate Canada Website (>50 weather stations, hourly data) and matched the data with traffic crash incidents to study weather at the time of a traffic crash. 

Some interesting features included
1. Data Wrangling and handling exceptions
2. Populating the traffic crash database
3. Populating the weather database with webscraped data using a list of generated URLs
4. For each crash, finding the closest weather station to a traffic crash based on shortest distance (calculated via longitude and latitude)
5. For each crash, finding the weather one week before and one week after to perform a McNemar's test for self-matched design 

The study required me to program a series of separate functions (split over several files) which read the CSV and piped wrangled, processed data to subsequent 


![Publication 1](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5228668/)

![Publication 2](https://www.sciencedirect.com/science/article/abs/pii/S030698771731229X)

![](https://github.com/RazaS/VISOR_code/blob/master/Programming%20Plan_Page_1.jpg)

![](https://github.com/RazaS/VISOR_code/blob/master/Programming%20Plan_Page_2.jpg)
