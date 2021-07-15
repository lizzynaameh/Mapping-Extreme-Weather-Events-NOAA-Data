# data_engineering

NOAA Storm Events [data engineering pipeline]

### Project Proposal Template

#### Question/need:

- As people and governments continue to grapple with the effects of climate change, we are interested in monitoring the frequency and severity of extreme weather events. This information can be useful in anticipating extreme weather events such as wildifires and hurricanes, which in turn can aid evacuation efforts and mobilize relief organizations before too much damage is done. 

#### Data Description:

- I'm looking at the National Oceanic and Atmospheric Administration's [Storm Events Database](https://www.ncdc.noaa.gov/stormevents/ftp.jsp). Each row represents a weather event in a different location of the United States and contains information on the date, the number of direct and indirect deaths, crop damage and property damage associated with the event.  So, it's possible to observe the impact of climate events geographically and over time. 

#### Tools:

- I am using SQL to query in data, pandas for data analysis and manipiulation, matplotlib and seaborn for visualizations, geopandas for geospatial analysis, and dash for the deployment of a web application.

#### MVP Goal:

- We will produce a visualization that maps the amount of total damage (crop and property) caused by extreme weather by state based on data for the year 2021.  
