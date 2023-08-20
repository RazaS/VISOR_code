import requests
import csv
import time
import os, sys

def monthFix(m):
    
    temp = ''
    #reformat month data for file names                
    if int(m)<10:
        temp = '0'+str(m)
        return temp
    else:
        temp = str(m)
        return temp

######################################################
#populate lists of weather stations, years

#variables
startYear=0
endYear=0
listy = []
listFinal = []
weatherIndex = 1 #for timepoint serials
weatherKey =  ['Date;Time', 'Year', 'Month', 'Day', 'Time', 'Data Quality', 'Temp (\xb0C)', 'Temp Flag', 'Dew Point Temp (\xb0C)', 'Dew Point Temp Flag', 'Rel Hum (%)', 'Rel Hum Flag', 'Wind Dir (10s deg)', 'Wind Dir Flag', 'Wind Spd (km/h)', 'Wind Spd Flag', 'Visibility (km)', 'Visibility Flag', 'Stn Press (kPa)', 'Stn Press Flag', 'Hmdx', 'Hmdx Flag', 'Wind Chill', 'Wind Chill Flag', 'Weather']


#stations file loading
with open('StationDataReformatted.csv', 'rb') as csvfile:
    sData = csv.reader(csvfile, delimiter=',', quotechar='|')
    
    #create dictionary with station data, each el is one weather station!
    for el in sData:
        
        #ignore header            
        if el[0] != 'Station Name':  
            
            #station
            s = str(el[1])
            
            #assign start (year, month) for data availability
            startYear= int(el[4])
            startMonth = int(el[5])
            
            #start of study data period
            if startYear<1993:
                startYear=1993
            
            #assign end (year,month)
            endYear = int(el[6])
            endMonth = int(el[7])  
            

            if endYear>2016:
                endYear=2016
                

            #day is always 01 for this website 
            d = '01'
              
            #main loop                          
            for y in range(startYear,endYear+1):
                
                #dealing with cases where data ends halfway between a year
                if startYear==y or endYear == y:
                    
                    if startYear ==y:
                    
                        for m in range(startMonth,13):

                            with open('Aggregated Station Data/' + s + '/' + str(y)+ '/'+ monthFix(m) +'01' + str(y) +'.csv', 'rb') as csvfile:
                                   
                                        wData = csv.reader(csvfile, delimiter=',', quotechar='|')
                                       
                                        for row in wData:
                                                  #print row
                                                listy.append(row)
                            
                            #for row1 in listy[16:]:
                                      #print row1
                            
                            #print "----------------------"
                            listFinal.append(listy[17:])
                            
                            #print listy [16:17]
                            #print listy [17:18]
                            
                            listy = []
                
                    if endYear==y:
                                                
                        for m in range(1,endMonth+1): #+1 ensures that the very last month gets included too!
                            
                            with open('Aggregated Station Data/' + s + '/' + str(y)+ '/'+ monthFix(m) +'01' + str(y) +'.csv', 'rb') as csvfile:
                                   
                                        wData = csv.reader(csvfile, delimiter=',', quotechar='|')
                                       
                                        for row in wData:
                                                  #print row
                                                listy.append(row)
                            
                            #for row1 in listy[16:]:
                                      #print row1
                            
                            #print "----------------------"
                            listFinal.append(listy[17:])
                            
                            #print listy [16:17]
                            #print listy [17:18]
                            
                            listy = []
                                            
                #when data is available throughout the year 
                else:
                
                    for m in range(1,13):
                           
                        with open('Aggregated Station Data/' + s + '/' + str(y)+ '/'+ monthFix(m) +'01' + str(y) +'.csv', 'rb') as csvfile:
                                   
                                        wData = csv.reader(csvfile, delimiter=',', quotechar='|')
                                       
                                        for row in wData:
                                                  #print row
                                                listy.append(row)
                            
                        #for row1 in listy[16:]:
                                  #print row1
                        
                        #print "----------------------"
                        listFinal.append(listy[17:])
                        
                        #print listy [16:17]
                        #print listy [17:18]
                        
                        listy = []


#######################file printing#####################
            out = open('Aggregated Station Data' + '/' + s + '/' + s + ' - aggregate.csv', 'wb')
            output = csv.writer(out)
                      
            output.writerow(weatherKey)
                      
            #prints a list into a CSV, but commas put in manually 
            for row in listFinal:
                
                for rowy in row:
                                
                                #clean data
                                rowy = [w.replace('"', '') for w in rowy]
                                rowy = [w.replace(' ', '') for w in rowy]
                                
            
                                                 
                                #modify last rows to combine all descriptive weather variables
                                if len(rowy)>24:
                                        rowy[24] = ' '.join(rowy[24:])
                                        rowy = [w.replace(' ', ';') for w in rowy]
                                        rowy = rowy[:25]
                                
                                                    
                                #modify dictionary key variable, first one, for later matching
                                temp = rowy[0]
                                print temp
                                print el[0]
                                temp = temp[0:4]+ ";"+str(int(temp[5:7])) +";"+ str(int(temp[8:10]))+";"+ str(int(temp[10:12].replace(":","")))
                                #print temp
                                rowy[0] = temp
                                
                                rowy.append(str(weatherIndex))
                                weatherIndex+=1                              
                                #print rowy
                                
            
                                output.writerow(rowy)
            
            #clear list final for next weather station
            listFinal = []          
            out.close()



######################################################

#import csv 
#import os, sys

#weatherKey =  ['Date;Time', 'Year', 'Month', 'Day', 'Time', 'Data Quality', 'Temp (\xb0C)', 'Temp Flag', 'Dew Point Temp (\xb0C)', 'Dew Point Temp Flag', 'Rel Hum (%)', 'Rel Hum Flag', 'Wind Dir (10s deg)', 'Wind Dir Flag', 'Wind Spd (km/h)', 'Wind Spd Flag', 'Visibility (km)', 'Visibility Flag', 'Stn Press (kPa)', 'Stn Press Flag', 'Hmdx', 'Hmdx Flag', 'Wind Chill', 'Wind Chill Flag', 'Weather']
         

##variables list
#listy = []
#listFinal = []
#weatherIndex = 1 #for timepoint serials

#for s in stationID:

          #for y in year:
                    
                    #for m in month:
                              
                              #with open( 'Aggregated Station Data/' + s + '/' + y+ '/'+ m +'01' + y +'.csv', 'rb') as csvfile:
                                   
                                        #wData = csv.reader(csvfile, delimiter=',', quotechar='|')
                                       
                                        #for row in wData:
                                                  ##print row
                                                  #listy.append(row)
                            
                              ##for row1 in listy[16:]:
                                        ##print row1
                              
                              ##print "----------------------"
                              #listFinal.append(listy[17:])
                              
                              ##print listy [16:17]
                              ##print listy [17:18]
                              
                              #listy = []



          ##write a file


          #out = open('Aggregated Station Data' + '/' + s + '/' + s + ' - aggregate.csv', 'wb')
          #output = csv.writer(out)
          
          #output.writerow(weatherKey)
          
          ##prints a list into a CSV, but commas put in manually 
          #for row in listFinal:
                    #for rowy in row:
                              
                              ##clean data
                              #rowy = [w.replace('"', '') for w in rowy]
                              #rowy = [w.replace(' ', '') for w in rowy]
                              
          
                                               
                              ##modify last rows to combine all descriptive weather variables
                              #if len(rowy)>24:
                                        #rowy[24] = ' '.join(rowy[24:])
                                        #rowy = [w.replace(' ', ';') for w in rowy]
                                        #rowy = rowy[:25]
                              
                                                  
                              ##modify dictionary key variable, first one, for later matching
                              #temp = rowy[0]
                              #temp = temp[0:4]+ ";"+str(int(temp[5:7])) +";"+ str(int(temp[8:10]))+";"+ str(int(temp[10:12].replace(":","")))
                              ##print temp
                              #rowy[0] = temp
                              
                              #rowy.append(str(weatherIndex))
                              #weatherIndex+=1                              
                              ##print rowy
                              
          
                              #output.writerow(rowy)
                    
          #out.close()




               
          

