import requests
import sys
import json
import time

# pm25_checker function is for getting the pm25 value of a single station given the input parameter of the stationID (fetched from the coordinates),
# missingValueCount (counter for the number of station that doesn't have the pm25 value in the station json obj), and apiKey
def pm25_checker(stationID,missingValueCount,apiKey):

    url = f"https://api.waqi.info/feed/{stationID}/?token={apiKey}"

    response = requests.get(url)
    jsonData = response.json()
    pm25 = 0
    # print(response)
    

    # check if pm25 value exist in the iaqi section of the json
    # if it doesn't increase missingValueCount by 1 for a station that doesn't have the pm25 value
    # Also, setting the pm25 to None
    if 'pm25' not in jsonData['data']['iaqi']:

        missingValueCount = missingValueCount + 1
        pm25 = None
        # print(f"the missingstationcount is {missingValueCount}")
    else:
        pm25 = jsonData['data']['iaqi']['pm25']['v']

    # printing the pm25 value of each specific station
    print(f"PM2.5 value: {pm25} {stationID} station")

    # return the station's pm25 value and the counter value to track if the station doesn't have any pm25 value
    return pm25, missingValueCount



def calculateSampledStationPm25Average (latitude_1, longitude_1, latitude_2, longitude_2,samplingPeriod,samplingRate):


    apiKey = "166c8ba47f70b0af804d481d47fa5dc8dbfb04f1"
    theLatLong = f"{latitude_1},{longitude_1},{latitude_2},{longitude_2}"
    missingValueCount = 0
    listOfPm25Value = []
    samplingCount = 0


    # structure for get request for stations based on coordinate bound <</map/bounds?token=:token&latlng=:latlng>>

    url = f"https://api.waqi.info/map/bounds?token={apiKey}&latlng={theLatLong}"


    response = requests.get(url)

    # print(response)

    json_data = response.json()

    # list to store all of the fetched station uid from the given coordinates input
    stationIdList = [] 

    # loop through each station's data and get its uid to place into a station list
    for varX in json_data['data']:
        # print("there are these stations")
        # print(varX['uid']) 
        stationIdList.append(varX['uid'])


    samplingPeriodInSecond = int(samplingPeriod) * 60
    # 5 * 60 = 300 seconds
    # samplingRateInSecond is 60 second divided by the rate so we get the rate of execution for the pm25_checker function
    samplingRateInSecond = int(60 / int(samplingRate))
    
    # looping through the sampled period with the indicated rate to get all stations' pm2.5
    for seconds in range(0, samplingPeriodInSecond+samplingRateInSecond,samplingRateInSecond):

        # looping through the list of station to get each of their pm25 value
        for station in stationIdList:
            pm25Value,missingValueCount = pm25_checker(f"@{station}",missingValueCount,apiKey)
            samplingCount = samplingCount + 1

            if pm25Value is not None:
            # dont add to list if pm25 is none value
                listOfPm25Value.append(pm25Value)

        # sleep function for spacing out each execution within the sampling period
        if seconds < samplingPeriodInSecond:
            time.sleep(samplingRateInSecond)


    # some testing values
    # print(f"the missingvalue count is {missingValueCount}")
    # print(f"samplingCount is {samplingCount}")
    # print(f"the list of pm25 looks like this {listOfPm25Value}")

    # Since some station doesn't have the pm25 value in the iaqi section of the station json, 
    # we take those out of the sample to prevent uncertainty in the final calculated average of all stations pm2.5 values
    totalSampledCount = samplingCount - missingValueCount

    # final average pm25 across all sampled stations
    finalAverage = sum(listOfPm25Value)/totalSampledCount

    print(f"Overall PM2.5 average of all stations over {samplingPeriod} minutes of sampling: {finalAverage}")


# MAIN SECTION

# Some testing values:

# samplingPeriod = 5
# samplingRate = 1

# upper left ubc random spot 1 (lat/long): 49.292545628912194,-123.31372270597726
# surrey random spot 2 (lat/long): 49.188150682588535,-122.78044889229854
# latitude_1 = "49.292545628912194"
# longitude_1 = "-123.31372270597726"
# latitude_2 = "49.188150682588535"
# longitude_2 = "-122.78044889229854"

# command line values for coordinates and sampled period and rate
latitude_1 = sys.argv[1]
longitude_1 = sys.argv[2]
latitude_2 = sys.argv[3]
longitude_2 = sys.argv[4]
samplingPeriod = sys.argv[5]
samplingRate = sys.argv[6]

# print(sys.argv)

theLatLong = f"{latitude_1},{longitude_1},{latitude_2},{longitude_2}"
# executing the function to calculate the average of all sampled station pm25 value
calculateSampledStationPm25Average(latitude_1, longitude_1, latitude_2, longitude_2,samplingPeriod,samplingRate)

# to test execution of the function from terminal: TRY <<python3 pm25calAverage.py 49.292545628912194 -123.31372270597726 49.188150682588535 -122.78044889229854 5 1>>