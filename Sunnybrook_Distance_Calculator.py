import csv 

#function returns 1) list with crash location data, and 2) sequence for it  
def crashFileReader(filename): 
          
            lData = []
            crashLocationArray = []
            coordinateSequence = {} # keeps track of order in original file 
            counter = 0            
            
            with open(filename, 'rb') as csvfile:
                        
                        lData = csv.reader(csvfile, delimiter=',', quotechar='|')
                    
                        #create dictionary with weather data
                        for row in lData:
                                    
                                    #key order sequence
                                    if counter!=0: #skip header 
                                                crashLocationArray.append(row)                                                
                                                coordinateSequence [str(counter)] = row[0]
                                                #print str(counter) + ' ' + coordinateSequence [str(counter)]
                                    
                                    counter+=1
                                    
                                               
            return (crashLocationArray, coordinateSequence) 


#converts list with crashes to dictionary with crashes and cleans data
def crashCleaner(crashLocationArray): 

            coordinates = {} #latitude, then longitude
            
            counter = 0
            
            #this loop cleans data and converts into a dictionary for easy searching
            for x in crashLocationArray:
                        
                        #this deals with duplicates 
                        #if x[0] in coordinates:
                                    #x[0]=  x[0]+'x'                        
                        #print x 
                        if x[1]: #if lon/lat not empty
                                                                     

                                    temp1 = x[1].replace('"', '')
                                    temp1.replace(' ','')
                                    #print float(temp1)
                                    
                                    temp2 = x[2].replace('"', '')
                                    temp2.replace(' ','')        
                                    #print float(temp2)
                                    
                                    temp3 = x[3].replace('"', '')
                                    temp3.replace(' ','')  
                             
                                    temp4 = x[4].replace('"', '')
                                    temp4.replace(' ','')         
                                    
                                    temp5 = x[5].replace('"', '')
                                    temp5.replace(' ','')  
                             
                                    temp6 = x[6].replace('"', '')
                                    temp6.replace(' ','')   
                                    
                                    
                                    if temp3 == '#VALUE!' or temp4 == '#VALUE!' or temp5 == '#VALUE!' or temp6 == '#VALUE!': #for missing dates
                                                                                                            
                                                coordinates[x[0]]= ['empty' , 'empty', 'skip', 'skip', 'skip', 'skip']
                                        
                                    else:    
                                                                                                  
                                                coordinates[x[0]]= [float(temp1),float(temp2), temp3,temp4, temp5, temp6 ] #convert strs to decimals
                        
                        #this condition keeps the date/time even if longitude/latitude is missing, for imputation purposes later    
                        elif  not(x[1]) and len(x) >4:
                                    
                                    print x
                                    temp3 = x[2].replace('"', '')
                                    temp3.replace(' ','')  
                             
                                    temp4 = x[3].replace('"', '')
                                    temp4.replace(' ','')         
                                    
                                    temp5 = x[4].replace('"', '')
                                    temp5.replace(' ','')  
                             
                                    temp6 = x[5].replace('"', '')
                                    temp6.replace(' ','')                                     
                                    
                                    if temp3 == '#VALUE!' or temp4 == '#VALUE!' or temp5 == '#VALUE!' or temp6 == '#VALUE!': #for missing dates
                                                                                                            
                                                coordinates[x[0]]= ['empty' , 'empty', 'skip', 'skip', 'skip', 'skip']
                                                
                                    else:    
                                                                                                  
                                                coordinates[x[0]]= ['empty','empty', temp3,temp4, temp5, temp6 ] #convert strs to decimals  
  
                        else:    
                                                                                      
                                    coordinates[x[0]]= ['empty' , 'empty', 'skip', 'skip', 'skip', 'skip'] #convert strs to decimals                         
                       
            return coordinates


# calculates distance between two coordinates in km 
def distanceCalculator(crashLat,crashLon,stationLat,stationLon):
            
            #each degree of latitude is 111 km, each degree of longitude is about 96 km
            #applying distance formula ## the -96 is to change the sign of longitude for simplicity    
            print 'lat' + str((float(stationLat) - crashLat)*111)
            print 'lon' + str((float(stationLon) - (-1*crashLon))*96  )
            
            distance = pow( (pow( (float(stationLat) - crashLat)*111  , 2) + pow( (float(stationLon) - (-1*crashLon))*96  ,2)) , 0.5)

            return distance           
            

#takes list with crashes matched with stations and outputs it 
def printFinalListToCSV(outputList, fileName):
            
            out = open(fileName, 'wb')
            output = csv.writer(out)
            
            #header
            output.writerow(['Case', 'Distance to Sunnybrook', 'Imputed'])       
            
            #prints a list into a CSV, but commas put in manually 
            for row in outputList:
                        output.writerow(row)
                      
            out.close()

############################################################################################################

outputList = []

#load crash list 

rawCrashArray, rawCrashSequence = crashFileReader('LocationListingUpdate-w-locations.csv') 

#convert crash list to dictionary 

crashDictionary = crashCleaner(rawCrashArray)

#loop through crash sequence and pull crashDictionary data
for n in range(1,len(rawCrashSequence)+1):

            caseIndex = rawCrashSequence[str(n)]
            
            clatitude = crashDictionary [str(caseIndex)][0]
            clongitude = crashDictionary [str(caseIndex)][1]

            #if data not missing 
            if clongitude != 'empty' and clatitude !='empty':
                        
                        sunnybrookLon = 79.38132
                        sunnybrookLat  = 43.66683
                                
                                                                        
                        tempDist = distanceCalculator(clatitude,clongitude,sunnybrookLat,sunnybrookLon)
                        
                        #print tempDist
                                                                        
                                                            
                        
                        #write to output list 
                        outputList.append([caseIndex, tempDist, 'No'])
                        
                        
                        
                        
            #if missing data            
            else:

                        sunnybrookLon = 79.38132
                        sunnybrookLat  = 43.66683
                        
                        standInLon = -79.36538
                        standInLat = 43.78878
                        
            
                        tempDist = distanceCalculator(standInLat,standInLon,sunnybrookLat,sunnybrookLon)
            
            
                        #print str(tempDist) + ' i '
            
                        #write to output list 
                        outputList.append([caseIndex, tempDist, 'Yes'])                        



#print output list to CSV (outputList, fileName)
printFinalListToCSV(outputList, 'Distance to Sunnybrook.csv')
 
print len(rawCrashArray)
print len (crashDictionary)
print len(outputList)