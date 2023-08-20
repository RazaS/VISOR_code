import csv 
import os, sys

#############################################################################
## This file will load data from monthly data flies and combine them into  ##
## one large .csv file.                                                    ##
#############################################################################

#######################Variables#############################################

#Columns in weather file
weatherKey =  ['Date;Time', 'Year', 'Month', 'Day', 'Time', 'Data Quality', 'Temp (\xb0C)', 'Temp Flag', 'Dew Point Temp (\xb0C)', 'Dew Point Temp Flag', 'Rel Hum (%)', 'Rel Hum Flag', 'Wind Dir (10s deg)', 'Wind Dir Flag', 'Wind Spd (km/h)', 'Wind Spd Flag', 'Visibility (km)', 'Visibility Flag', 'Stn Press (kPa)', 'Stn Press Flag', 'Hmdx', 'Hmdx Flag', 'Wind Chill', 'Wind Chill Flag', 'Weather']
         
#lists for looping
tempList = []
listFinal = []
outputList = []

#Timepoint Index, crucial in post-processing
weatherIndex = 1

#Station information to iterate through; station ID, month and year of files
stationID = ['5097']
month = ['01','02','03','04','05','06','07','08','09','10','11','12']
year = ['1993','1994','1995','1996','1997','1998','1999',
        '2000','2001','2002','2003','2004','2005','2006','2007','2008','2009',
        '2010','2011','2012']




for s in stationID:
          
          #OutputCSV for each station 
          out = open('Aggregated Station Data' + '/' + s + '/' + s + ' - aggregate.csv', 'wb')
          output = csv.writer(out)
          output.writerow(weatherKey)
          
          
          for y in year:
                    
                    for m in month:
                              
                              with open( 'Aggregated Station Data/' + s + '/' + y+ '/'+ m +'01' + y +'.csv', 'rb') as csvfile:
                                   
                                        wData = csv.reader(csvfile, delimiter=',', quotechar='|')
                                       
                                        for row in wData:
                                                  #print row
                                                  tempList.append(row)
                            
                              listFinal.append(tempList[17:])

                              tempList = []




          
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
                              temp = temp[0:4]+ ";"+str(int(temp[5:7])) +";"+ str(int(temp[8:10]))+";"+ str(int(temp[10:12].replace(":","")))
                              #print temp
                              rowy[0] = temp
                              
                              rowy.append(str(weatherIndex))
                              weatherIndex+=1   
   
                              outputList.append(rowy)
                              
          
                              output.writerow(rowy)
                    
          out.close()




               
          

