# PM25 Average Calculation Across Sampled Stations 

## Description
This repository is to showcase the program for calculating the average of air pollutant PM2.5 over n minutes, of
all the stations map bound by two pairs of latitudes and longitudes.


  ### Assumption Made
  * For a sampled period of 5 minutes, the program start to fetch station data from minute zero so 6 iteration for 5 minutes with the rate of fetch rate of once per minute.
  * Station like uid 4220 in Burnaby doesn't have a pm25 value in the iaqi json obj therefore the station pm25 wasn't calculated into the total average
  



### Executing the program

1. Clone the repository on Github
2. Open VsCode with the repository file folder
3. The application can be compiled and run using VScode or other IDEs
4. Execute the following structured statement in terminal to run the program python3 pm25calAverage.py <latitude_1> <longitude_1> <latitude_2> <longitude_2> <samplingPeriod> <samplingRate> <br />
    * Sample: ```python3 pm25calAverage.py 49.292545628912194 -123.31372270597726 49.188150682588535 -122.78044889229854 5 1```
      * Sample data latitude_1,longitude_1 --> upper left ubc random coordinate 1 (lat/long): 49.292545628912194,-123.31372270597726
      * Sample data latitude_2,longitude_2 --> random coordinate 2 in north side of Surrey (lat/long): 49.188150682588535,-122.78044889229854
      * Sample data --> samplingPeriod = 5 (definite 5)
      * Sample data --> samplingRate = 1 (definite 1 )
  
