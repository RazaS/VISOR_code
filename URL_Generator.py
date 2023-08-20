import csv 

###########Variables###################
startYear=0
endYear=0

urlList = [['StationID', 'Year', 'Month']] #CSV header + output list

#######################################
    
    
###### Load information from StationDataReformatted  ###
###### and and add it to a urlList for CSV output  #####
##
## Program is complicated by the fact that not all #####
## data is available within certain years but only #####
## goes upto certain months                       ######

#open station data file reformatted 
with open('StationDataReformattedForDownload.csv', 'rb') as csvfile:
    wData = csv.reader(csvfile, delimiter=',', quotechar='|')

    #create dictionary with weather data
    for row in wData:
        
        if row[0] != 'Station Name': #ignore header 
            
            #assign start (year, month) for data availability
            startYear= int(row[4])
            startMonth = int(row[5])
            
            #start of data availability period
            if startYear<1993:
                startYear=1993
            
            #assign end (year,month)
            endYear = int(row[6])
            endMonth = int(row[7])  
            
            #end of data availability period            
            if endYear>2014:
                endYear=2014
                
            #day is always 01 for this website 
            d = '01'
                                       
            for y in range(startYear,endYear+1):
                
                #dealing with cases where data starts or ends somewhere in the middle of a year
                #this tends to be at the beginning or at the end of the data period
                #so the conditional below checks at these points specifically
                #this code can't deal with data missing somewhere between the start and end time-periods
                #it is assumed that data there would at least have empty files associated 
                if startYear==y or endYear == y: 
                    
                    if startYear ==y: 
                    
                        for m in range(startMonth,13): #iterate through months

                            urlList.append([str(row[1]), str(y), str(m)])
                
                    if endYear==y:
                                            
                                            #this +1 may prove problematic later but for the program is skipping the last month    
                        for m in range(1,endMonth+1):
                            
                            urlList.append([str(row[1]), str(y), str(m)])
                                            
                #when dealing with a year that isn't first or last year of data availability
                else:
                
                    for m in range(1,13):
                           
                        urlList.append([str(row[1]), str(y), str(m)])
                                       
#######################################


#####Output urlList to CSV#############
    
#write crash specific weather data to file

out = open('URL-List.csv', 'wb')
output = csv.writer(out)

                
#prints a list into a CSV, but commas put in manually 
for row in urlList:
        output.writerow(row)
          
out.close()

#######################################

####Reference#################

#url creator code
#url = 'http://climate.weather.gc.ca/climateData/hourlydata_e.html?timeframe=1&Prov=ON&StationID='+ str(row[1]) + '&hlyRange='+ str(row[8])+'&Year='+str(y)+'&Month='+str(m)+'&Day='+str(01)
#print url

