import csv 

#####This file can pull weather data from a weather data file and#####
######load it into a list, which can then be searched with############
###### year month day time information################################
##
### Note: Data file with weather data must be cleaned *beforehand* w/#
### a set of procedures listed elsewhere##############################
######################################################################
#row index (subtract 1)
#0 Date/Time	
#1 Year	
#2 Month	
#3 Day	
#4 Time	
#5 Data Quality	
#6 Temp (°C)	
#7 Temp Flag	
#8 Dew Point Temp (°C)	
#9 Dew Point Temp Flag	
#10 Rel Hum (%)	
#11 Rel Hum Flag	
#12 Wind Dir (10s deg)	
#13 Wind Dir Flag	
#14 Wind Spd (km/h)	
#15 Wind Spd Flag	
#16 Visibility (km)	
#17 Visibility Flag	
#18 Stn Press (kPa)	
#19 Stn Press Flag	
#20 Hmdx	
#21 Hmdx Flag	
#22 Wind Chill	
#23 Wind Chill Flag	
#24 Weather


#define lists needed
weatherKey =  ['Date/Time', 'Year', 'Month', 'Day', 'Time', 'Data Quality', 'Temp (\xb0C)', 'Temp Flag', 'Dew Point Temp (\xb0C)', 'Dew Point Temp Flag', 'Rel Hum (%)', 'Rel Hum Flag', 'Wind Dir (10s deg)', 'Wind Dir Flag', 'Wind Spd (km/h)', 'Wind Spd Flag', 'Visibility (km)', 'Visibility Flag', 'Stn Press (kPa)', 'Stn Press Flag', 'Hmdx', 'Hmdx Flag', 'Wind Chill', 'Wind Chill Flag', 'Weather']

weatherData = {'key':'store'}

#indices
weatherIndex = {'key':'store'}


#import weather data into file
#with open('Pearson-Airport-1993-2012-v4' + '.csv', 'rb') as csvfile:
    #wData = csv.reader(csvfile, delimiter=',', quotechar='|')
    
with open('amalgamx' + '.csv', 'rb') as csvfile:
    wData = csv.reader(csvfile, delimiter=',', quotechar='|')
    
    
    #create dictionary with weather data
    for row in wData:

        weatherData [row[0]] = row[1:]
        #print weatherData [row[0]] 
        
        #populate list for indexing 
        weatherIndex [row[-1]] = row[0]
        #print weatherIndex [row[-1]]
        
        
        

        
for keys,values in weatherIndex.items():
    print(keys)
    print(values)

print '----'
print weatherIndex['138708']
print weatherIndex[str(int(138708)+168)]
print weatherIndex[str(int(138708)-168)]

#simple search input        
#year = input('Enter the year ')
#month  = input ('Enter the month ')
#day = input ('Enter the day ')
#hour = input ('Enter the time ')

year = 1994
month  = 2
day = 3
hour = 300

#simple search function
#for row in weatherData[1:]:
    #if (year == eval(row[1])) & (month == eval(row[2])) & (day == eval(row[3])) & (hour == eval((row[4].replace(':',"")))):
        #print row
        
