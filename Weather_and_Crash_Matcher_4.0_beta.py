import csv 

########### This file can load data from a PREPARED a) weather data file######
########### AND b) a PREPARED crash data file ################################
########### and find corresponding weather entries for all crash days ########


##############Import Crash Data################################################

def crashDataReader (filename):
        #columns in crash data file
        crashKey= ['Trauma Number', 'incident location', 'GEOCODE', 'NearestAirport', 
                   'Injury_Year', 'Injury_Month', 'Injury_Day', 'Injury_Hour']
        
        crashData = []
        
        #import accident data 
        with open(filename, 'rb') as csvfile:
                cData = csv.reader(csvfile, delimiter=',', quotechar='|')
                
                #create list with weather data
                for row in cData:
                        #print row 
                        crashData.append(row)    
        
        return crashData

###############################################################################

############ Importing Amalgamated Weather Data File for all stations ###########

def importStationData (stationID):
        
        weatherData = {}
        weatherIndex = {}
        maxIndex = 0
        lastDate = 0
        
        with open('Aggregated Station Data/' + stationID + '/' + stationID + ' - aggregate' + '.csv', 'rb') as csvfile:
                wData = csv.reader(csvfile, delimiter=',', quotechar='|')
            
        #create dictionary with weather data
                for row in wData:
                        
                        #creating weather data dictionary
                        weatherData [row[0]] = row[1:]
                        
                        #populate dictionary for indexing 
                        weatherIndex [row[-1]] = row[0]
                        
                        #print row[-1]
                        
                        #get the last timepoint index from weather data file
                        if str(row[-1])!='':
                                maxIndex = row[-1]
                        
                        #print maxIndex
                                
        #convert max index to integer
        #print stationID
        #print maxIndex
        maxIndex = int(maxIndex)
        lastDate = weatherIndex[str(maxIndex)].split(';')
        #print maxIndex
        #print lastDate
        return (weatherData, weatherIndex, maxIndex, lastDate)
        
        

def allStationDictionary(weatherStationArray):
        
        allStationsDict = {}
        
        for station in weatherStationArray:
                
                stationID = str(station[-1])
                #feed stationID into station loading function 
                weatherData, weatherIndex, maxIndex, lastDate =   importStationData (stationID)
                
                allStationsDict[stationID] = [weatherData, weatherIndex, maxIndex, lastDate]
                
        return allStationsDict


#returns list with weather station data without header 
def weatherStationReader (filename):
            
        #weather station data
        weatherStationArray = []
        
        with open(filename, 'rb') as csvfile:
                wData = csv.reader(csvfile, delimiter=',', quotechar='|')
            
                #create dictionary with weather data
                for row in wData:
                        weatherStationArray.append(row)
                        #print row
                weatherStationArray.pop(0) #removes header   
                    
        return weatherStationArray 

###############################################################################


#'row' here in the parameters is from crash data, always ignore first row for this 
def WeatherAndCrashRowMatcher (stationID, row, timepoint):
        
        #return (weatherData, weatherIndex, maxIndex, lastDate)
        weatherData, weatherIndex, maxIndex, lastDate = importStationData (stationID)
        
        #preparing dictionary key code FOR weather data file, FROM crash data file
        temp = year+";"+month+";"+day+";"+hour      #crashData/year/month/day/hour
             
        row = row[:8] #concatenating crash data rows 

                
        #elements to pull from file, with year specified because data not avaialable past that
        if int(year)< int(lastDate[0]):
                 
                ##Conditional takes crash date, gets TimePoint index, uses it to calculate
                ##a timepoint a week later, and then changes temp variable to that for
                ##feeding into dictionary, which then gets the matching values from weather file
                ##+168 is how many hours in 7 days, for 1 week before/after matching
                
                #1 Week After
                if timepoint == 1:
                        if (int(weatherData[temp][-1])+168) < int(maxIndex):
                                temp =  weatherIndex[str(int(weatherData[temp][-1])+168)]
                
                #1 Week Before 
                if timepoint == -1:
                        temp =  weatherIndex[str(int(weatherData[temp][-1])-168)]
               

                #the 25 is crucial due to the added index
                if len (weatherData[temp])==25:
                        
                        #this adds the columns we want from the weather data file, to the final data file
                        for n in [1,2,3,4,6,10,14,16,18,24, 25]:
                                row.append(weatherData[temp][n-1])
                        #print row
                        
                #this else deals with cases where weather data is missing, finds closest time and uses that
                else:
                        
                        #program to find nearest time
                        currentIndex = int(weatherData[temp][-1])
                        newIndex = 0
                        #print currentIndex
                        #print weatherIndex [str(currentIndex)]
                        for i in range (currentIndex, 0, -1):
                                newIndex = str(i)
                                newTemp = weatherIndex[newIndex]
                                if len (weatherData[newTemp])==25: #loop backwards starting at index until found
                                        
                                        #this adds the columns we want from the weather data file, to the final data file row. the row already had accident data and this tacks on weather data. This way of doing it allows us to add weather data from any timepoint, which ended up being very helpful for tracking back closest time!
                                        for n in [1,2,3,4,6,10,14,16,18,24, 25]:
                                                row.append(weatherData[newTemp][n-1])
                                        
                                        row[5:9] = []                                                
                                        cmwData.append(row)
                                        break
                                        #print row                                                        
        else:
                #the other case, for *some* but not all years in last year of availble data
                # format here, month AND year +1
                #consider changing month to month +1
                
                if int(month)<(int(lastDate[1])+1) and int(year)<(int(lastDate[0])+1): 
                        ##Conditional takes crash date, gets TimePoint index, uses it to calculate
                        ##a timepoint a week later, and then changes temp variable to that for
                        ##feeding into dictionary, which then gets the matching values from weather file
                        ##+168 is how many hours in 7 days, for 1 week before/after matching
                        
                        #1 Week After
                        if timepoint == 1:
                                
                                if str(int(weatherData[temp][-1])+168) in weatherIndex: #to avoid key error during last year
                                        if (int(weatherData[temp][-1])+168) < int(maxIndex):
                                                temp =  weatherIndex[str(int(weatherData[temp][-1])+168)]

                        #1 Week Before 
                        if timepoint == -1:
                                temp =  weatherIndex[str(int(weatherData[temp][-1])-168)]
                       
        
                        #the 25 is crucial due to the added time sequence index
                        if len (weatherData[temp])==25:
                                
                                #this adds the columns we want from the weather data file, to the final data file
                                for n in [1,2,3,4,6,10,14,16,18,24, 25]:
                                        row.append(weatherData[temp][n-1])

        return row


###################Variables#################
#takes station id and runs program

def WeatherAndCrashMatcher (stationID, crashData):
        
        print "Station ID:" + stationID
        
        #columns in weather data file 
        weatherKey =  ['Date/Time', 'Year', 'Month', 'Day', 'Time', 'Data Quality',
                       'Temp (\xb0C)', 'Temp Flag', 'Dew Point Temp (\xb0C)', 'Dew Point Temp Flag',
                       'Rel Hum (%)', 'Rel Hum Flag', 'Wind Dir (10s deg)', 'Wind Dir Flag',
                       'Wind Spd (km/h)', 'Wind Spd Flag', 'Visibility (km)', 'Visibility Flag',
                       'Stn Press (kPa)', 'Stn Press Flag', 'Hmdx', 'Hmdx Flag', 'Wind Chill',
                       'Wind Chill Flag', 'Weather']
        
        #weather data Dictionary 
        weatherData = {'key':'store'}
        
        #indices for timepoints 
        weatherIndex = {'key':'store'}
        maxIndex = 0 #index used later to represent last timepoint available in weather data
        
        #Variable for before/crash/after
        #_Before = -1 #_Crash = 0 #_After = 1
        timepoints = [-1,0,1]
        
        #getting weather variables from function
        weatherData, weatherIndex, maxIndex, lastDate = importStationData (stationID)         

        #grand loop
        for timepoint in timepoints:
                #print 'Next'
                #CSV file header, picked based on timepoint
                
                #day of crash
                if timepoint ==0:
                        
                        timepointStr='Crash'
                        
                        header = ['Trauma Number','Injury_Year','Injury_Month', 
                'Injury_Day','Injury_Hour', 'Weather_Year', 'Weather_Month', 'Weather_Day', 'Weather_Hour', 'Temp_crash','Humidity_crash','Windspeed_crash','Visibility_crash','Barometric_Pressure_crash',
                'Weather_crash', 'TimePointIndex_crash']
                
                #1 week before crash
                elif timepoint ==-1:
                        
                        timepointStr='Before'
                        
                        header = ['Trauma Number','Injury_Year','Injury_Month', 
                'Injury_Day','Injury_Hour', 'Weather_Year', 'Weather_Month', 'Weather_Day', 'Weather_Hour', 'Temp_before','Humidity_before','Windspeed_before','Visibility_before','Barometric_Pressure_before',
                'Weather_before', 'TimePointIndex_before']
                
                #1 week after crash     
                elif timepoint ==1:
                        
                        timepointStr='After'
                        
                        header = ['Trauma Number','Injury_Year','Injury_Month', 
                'Injury_Day','Injury_Hour', 'Weather_Year', 'Weather_Month', 'Weather_Day', 'Weather_Hour', 'Temp_after','Humidity_after','Windspeed_after','Visibility_after','Barometric_Pressure_after',
                'Weather_after', 'TimePointIndex_after']
                
                ##############################################################################
                
                print timepointStr 
                

                
                #####Matching Crash Data and Weather Data######################################
                
                crashAndWeatherData = []#List with Crash data and weather data
                cmwData = [] #crash matched weather dat
                cmwData.append(header)#adding header to file
                
                for row in crashData[1:]: #this index is useful for testing fewer cases in crashData file
                        
                        if str(row[1]) != 'skip':
                        
                                year = row[1]
                                month= row[2]
                                day= row[3]
                                hour= row[4]
                                
                                #preparing dictionary key code FOR weather data file, FROM crash data file
                                temp = year+";"+month+";"+day+";"+hour      #crashData/year/month/day/hour
                                     
                                row = row[:9] #concatenating crash data rows 
                        
                                        
                                #elements to pull from file, with year specified because data not avaialable past that
                                if int(year)< int(lastDate[0]):
                                         
                                        ##Conditional takes crash date, gets TimePoint index, uses it to calculate
                                        ##a timepoint a week later, and then changes temp variable to that for
                                        ##feeding into dictionary, which then gets the matching values from weather file
                                        ##+168 is how many hours in 7 days, for 1 week before/after matching
                                        
                                        #1 Week After
                                        if timepoint == 1:
                                                if (int(weatherData[temp][-1])+168) < int(maxIndex):
                                                        temp =  weatherIndex[str(int(weatherData[temp][-1])+168)]
                                                
                                                else:
                                                        continue   #ignores data past the maxIndex date  
                                        
                                        #1 Week Before 
                                        if timepoint == -1:
                                                temp =  weatherIndex[str(int(weatherData[temp][-1])-168)]
                                       
                        
                                        #the 25 is crucial due to the added index
                                        if len (weatherData[temp])==25:
                                                
                                                #this adds the columns we want from the weather data file, to the final data file
                                                for n in [1,2,3,4,6,10,14,16,18,24, 25]:
                                                        row.append(weatherData[temp][n-1])
                                                
                                                row[5:9] = []        
                                                cmwData.append(row)
                                                #print row
                                                
                                        #this else deals with cases where weather data is missing, finds closest time and uses that
                                        else:
                                                
                                                #program to find nearest time
                                                currentIndex = int(weatherData[temp][-1])
                                                newIndex = 0
                                                #print currentIndex
                                                #print weatherIndex [str(currentIndex)]
                                                for i in range (currentIndex, 0, -1):
                                                        newIndex = str(i)
                                                        newTemp = weatherIndex[newIndex]
                                                        if len (weatherData[newTemp])==25: #loop backwards starting at index until found
                                                                
                                                                #this adds the columns we want from the weather data file, to the final data file row. the row already had accident data and this tacks on weather data. This way of doing it allows us to add weather data from any timepoint, which ended up being very helpful for tracking back closest time!
                                                                for n in [1,2,3,4,6,10,14,16,18,24, 25]:
                                                                        row.append(weatherData[newTemp][n-1])
                                                                
                                                                row[5:9] = []                                            
                                                                cmwData.append(row)
                                                                print row                                                                                                                
                                                                break
                                
                                else:
                                        #the other case, for *some* but not all years in last year of availble data
                                        # format here, month AND year +1
                                        #consider changing month to month +1
                                        
                                        if int(month)<(int(lastDate[1])+1) and int(year)<(int(lastDate[0])+1): 
                                                ##Conditional takes crash date, gets TimePoint index, uses it to calculate
                                                ##a timepoint a week later, and then changes temp variable to that for
                                                ##feeding into dictionary, which then gets the matching values from weather file
                                                ##+168 is how many hours in 7 days, for 1 week before/after matching
                                                
                                                #1 Week After
                                                if timepoint == 1:
                                                        
                                                        if str(int(weatherData[temp][-1])+168) in weatherIndex: #to avoid key error during last year
                                                                if (int(weatherData[temp][-1])+168) < int(maxIndex):
                                                                        temp =  weatherIndex[str(int(weatherData[temp][-1])+168)]
                                                                
                                                                else:
                                                                        continue   #ignores data past the maxIndex date  
                                                
                                                #1 Week Before 
                                                if timepoint == -1:
                                                        temp =  weatherIndex[str(int(weatherData[temp][-1])-168)]
                                               
                                
                                                #the 25 is crucial due to the added time sequence index
                                                if len (weatherData[temp])==25:
                                                        
                                                        #this adds the columns we want from the weather data file, to the final data file
                                                        for n in [1,2,3,4,6,10,14,16,18,24, 25]:
                                                                row.append(weatherData[temp][n-1])
                                                        
                                                        row[5:9] = []   
                                                        cmwData.append(row)
                        
                        else: 
                                
                                row = row[:9] #concatenating crash data rows 
                                
                                empty = ['999.999','999.999','999.999','999.999','999.999','999.999','999.999','999.999','999.999','999.999','999.999']
                                for e in empty:
                                        row.append(e)
                                
                                row[5:9] = []        
                                cmwData.append(row)
                                
                
                ################### Crash and Weather Data Output to CSV ####################
                 
                outputToCSV  (cmwData, stationID, timepointStr)
                
                #############################################################################

def outputToCSV (cmwData, stationID, timepointStr):            
        #write crash specific weather data to fill        
        out = open(stationID+'-'+timepointStr + '.csv', 'wb')
        output = csv.writer(out)
        
        #prints a list into a CSV, but commas put in manually 
        for row in cmwData:
                #print row
                output.writerow(row)
                  
        out.close()


weatherStationsArray = weatherStationReader ('StationLocations - Copy.csv')

#dictlol = allStationDictionary (weatherStationsArray)
                
#WeatherAndCrashMatcher('4589')

#crashData = crashDataReader ('LLCommaSep.csv')

crashData2 = crashDataReader ('Crash-WeatherStation-Matched.csv')

#WeatherAndCrashMatcher ('50974841', crashData2)

#ignore header 

weatherStationsArray = weatherStationReader ('StationLocations - Copy.csv')

for station in weatherStationsArray:
        
        WeatherAndCrashMatcher (str(station[-1]), crashData2)
