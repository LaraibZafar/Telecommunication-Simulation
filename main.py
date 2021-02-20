import matplotlib.pyplot as plot
import numpy as np
import pandas as pd
import statistics
from queue import PriorityQueue
import random


class Line:
    def __init__(self, name, createdAt, timeServed):
        self.name = name
        self.createdAt = createdAt
        self.timeServed = timeServed
    
    def updateTimeServed(latestServiceDuration):
        self.timeServed += latestServiceDuration

def lineIncrement(lineName):
    return lineName + "I"

def telecomSimulation(durationInHours, ProbabilityCallOrigin_A):
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
    minimumExitQueue = PriorityQueue()

    simulationData = pd.DataFrame(columns=['interCallTime', 'arrivalTime', 'callDuration', 'departureTime', "callOrigin", "lineTitle"])
    
    while(maxDepartureTime <= durationInSeconds):
        
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
        if(minimumExitQueue.empty()):
            createNewLine = True
        else:
            createNewLine = True if(minimumExitQueue.queue[0][0] > simulationData.at[i, 'arrivalTime']) else False
        
        if(createNewLine):
            lineName = "Line" + str(lineCount)
            newLine = Line(lineName,simulationData.at[i, 'arrivalTime'], simulationData.loc[i]['callDuration'])
            simulationData.at[i,'lineTitle'] = lineName
            lineCount += 1
        else:
            lineName = minimumExitQueue.get()
            simulationData.at[i,'lineTitle'] = lineName[1]

        minimumExitQueue.put((simulationData.at[i, 'departureTime'],lineName))
        maxDepartureTime = max(maxDepartureTime,simulationData.at[i, 'departureTime'])
        i += 1
    print(lineCount)
    simulationData.plot.line(y="callDuration");
    simulationData.plot.line(y="departureTime");
    plot.show()
    
telecomSimulation(12,0.5)
       



    
