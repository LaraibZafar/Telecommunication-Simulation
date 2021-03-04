import matplotlib.pyplot as plot
import numpy as np
import pandas as pd
import statistics
from queue import PriorityQueue
import random
from scipy.stats import norm, uniform


class Line:
    def __init__(self, name, createdAt, timeServed):
        self.name = name
        self.createdAt = round(createdAt,2)
        self.timeServed = 0
    
    def updateTimeServed(self,latestServiceDuration):
        self.timeServed += latestServiceDuration
        self.timeServed = round(self.timeServed,2)
    
    def __str__(self):
        return self.name+"   "+str(self.createdAt)+"   "+ str(self.timeServed);

    def __lt__(self, other):
        return self.name < other.name

def lineIncrement(lineName):
    return lineName + "I"

def initalizeQueue(minimumExitQueue,lineData,numberOfLines):
    for lineCount in range(numberOfLines-1):
        lineName = "Line" + str(lineCount+1)
        newLine = Line(lineName,0, 0)
        minimumExitQueue.put((0,newLine))
        lineData.at[lineCount,'Line'] =newLine

def calculateNumberOfLinesBusy(numberOfLines,newArrivalTime,queue):
    numberOfFreeLines = 1 #Number of Lines = 1 + Line Number
    for i in range(0,queue.qsize()):
        if(newArrivalTime > queue.queue[i][0]):
            numberOfFreeLines+=1
    return numberOfLines-numberOfFreeLines

def calculateTotalTimeServed(lineData):
    totalTimeServed = 0
    for i in range(0,lineData.shape[0]):
        totalTimeServed += lineData.loc[i]['Line'].timeServed
    
    return totalTimeServed;

def telecomSimulation(numberOfLines,durationInHours, ProbabilityCallOrigin_A):
    durationInSeconds = durationInHours * 3600

    interCallTimeMinumum_A = 5
    interCallTimeMaximum_A = 15 

    interCallTimeMinumum_B = 6
    interCallTimeMaximum_B = 18

    callDurationMinimum = 120
    callDurationMaximum = 360

    i = 0
    lineCount = 1
    lineName = ''
    maxDepartureTime = 0
    callOrigin = ''
    blockedCalls=0
    totalCalls = 0
    minimumExitQueue = PriorityQueue()

    simulationData = pd.DataFrame(columns=['interCallTime', 'arrivalTime', 'callDuration', 'departureTime', "callOrigin", "lineTitle",'numberOfLinesBusy'])
    lineData = pd.DataFrame(columns=['Line','Efficiency'])

    initalizeQueue(minimumExitQueue,lineData,numberOfLines)
    
    while(maxDepartureTime <= durationInSeconds):
        totalCalls+=1
        callOriginProbability = random.uniform(0, 1)
        callOrigin = 'A' if(callOriginProbability <= ProbabilityCallOrigin_A) else 'B'
        simulationData.at[i, 'callOrigin'] = callOrigin

        if(callOrigin == 'A'):
            simulationData.at[i, 'interCallTime'] = round(np.random.uniform(interCallTimeMinumum_A, interCallTimeMaximum_A),2)
        elif(callOrigin == 'B'):
            simulationData.at[i, 'interCallTime'] = round(np.random.uniform(interCallTimeMinumum_B, interCallTimeMaximum_B),2)        

        simulationData.at[i, 'callDuration'] = round(np.random.uniform(callDurationMinimum, callDurationMaximum),2)

        if(i>0):
            simulationData.at[i, 'arrivalTime'] = simulationData.loc[i-1]['arrivalTime'] + simulationData.loc[i]['interCallTime']
        else:
            simulationData.at[i, 'arrivalTime'] = simulationData.loc[i]['interCallTime']

        simulationData.at[i, 'departureTime'] = simulationData.loc[i]['arrivalTime'] + simulationData.loc[i]['callDuration']
        createNewLine = True if(minimumExitQueue.queue[0][0] > simulationData.at[i, 'arrivalTime']) else False
        
        if(createNewLine):
            blockedCalls +=1
            simulationData.at[i,'numberOfLinesBusy'] =numberOfLines
        else:
            firstToExit = minimumExitQueue.get()
            line = firstToExit[1]
            simulationData.at[i,'lineTitle'] = line.name
            line.updateTimeServed(simulationData.loc[i]['callDuration'])
            minimumExitQueue.put((simulationData.loc[i]['departureTime'],line))
            simulationData.at[i,'numberOfLinesBusy'] = calculateNumberOfLinesBusy(numberOfLines,simulationData.loc[i]['arrivalTime'],minimumExitQueue)
        
        maxDepartureTime = max(maxDepartureTime,simulationData.at[i, 'departureTime'])
        i += 1
    
    for i in range(numberOfLines-1):
        lineData.at[i,'Efficiency'] = lineData.loc[i]['Line'].timeServed/(durationInHours*3600)
    
    lineData.plot.bar(y="Efficiency")
    print(simulationData)
    print(lineData)

    proportionBusyLines=calculateTotalTimeServed(lineData)/(durationInHours*3600)

    print("\nTotal Average Number of Lines Busy",simulationData['numberOfLinesBusy'].sum()/totalCalls)
    print("Proportions of Lines that are busy",proportionBusyLines)
    print("\nNumber of Total Calls : ",totalCalls)
    print("Number of Blocked Calls : ",blockedCalls)
    print("\nNumber Of Lines : ", numberOfLines)
    print("Percentage of Blocked Calls : ",blockedCalls/totalCalls)
    
    plot.show()


    
telecomSimulation(25,12,0.5)
    



    
