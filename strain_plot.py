# Compare strain plots between swallow, cough, and vocalization

from matplotlib import pyplot as plt
import numpy as np
import csv
import ast

swallowVideo = 465
coughVideo = 584
vocalizationVideo = 598

swallowDistancesName = "swallowDistances"+str(swallowVideo)+".csv"
with open(swallowDistancesName, 'r') as f:
    rd = csv.reader(f)
    swallowDistancesList = list(rd)
    swallowDistances = []
    for i in swallowDistancesList:
        rowList = []
        for j in i:
             res = ast.literal_eval(j)
             rowList.append(res)
        swallowDistances.append(rowList)
    f.close()

coughDistancesName = "coughDistances"+str(coughVideo)+".csv"
with open(coughDistancesName, 'r') as f:
    rd = csv.reader(f)
    coughDistancesList = list(rd)
    coughDistances =[]
    for i in coughDistancesList:
        rowList = []
        for j in i:
             res = ast.literal_eval(j)
             rowList.append(res)
        coughDistances.append(rowList)
    f.close()

vocalizationDistancesName = "vocalizationDistances"+str(vocalizationVideo)+".csv"
with open(vocalizationDistancesName, 'r') as f:
    rd = csv.reader(f)
    vocalizationDistancesList = list(rd)
    vocalizationDistances =[]
    for i in vocalizationDistancesList:
        rowList = []
        for j in i:
             res = ast.literal_eval(j)
             rowList.append(res)
        vocalizationDistances.append(rowList)
    f.close()

swallowMarkersName = "swallowMarkers"+str(swallowVideo)+".csv"
with open(swallowMarkersName, 'r') as f:
    rd = csv.reader(f)
    swallowMarkersList = list(rd)
    swallowMarkers = []
    for i in swallowMarkersList:
        rowList = []
        for j in i:
             res = ast.literal_eval(j)
             rowList.append(res)
        swallowMarkers.append(rowList)
    f.close()

coughMarkersName = "coughMarkers"+str(coughVideo)+".csv"
with open(coughMarkersName, 'r') as f:
    rd = csv.reader(f)
    coughMarkersList = list(rd)
    coughMarkers = []
    for i in coughMarkersList:
        rowList = []
        for j in i:
             res = ast.literal_eval(j)
             rowList.append(res)
        coughMarkers.append(rowList)
    f.close()

vocalizationMarkersName = "vocalizationMarkers"+str(vocalizationVideo)+".csv"
with open(vocalizationMarkersName, 'r') as f:
    rd = csv.reader(f)
    vocalizationMarkersList = list(rd)
    vocalizationMarkers = []
    for i in vocalizationMarkersList:
        rowList = []
        for j in i:
             res = ast.literal_eval(j)
             rowList.append(res)
        vocalizationMarkers.append(rowList)
    f.close()

print('Selected Markers:', swallowMarkers[0])

fps = 60
frameLength = 1/fps

swallowTime = np.linspace(0,len(swallowDistances)/fps,len(swallowDistances))
coughTime = np.linspace(0,len(coughDistances)/fps,len(coughDistances))
vocalizationTime = np.linspace(0,len(vocalizationDistances)/fps,len(vocalizationDistances))

marker1swallow = swallowMarkers[0][0] 
marker2swallow = swallowMarkers[0][1]

marker1cough = swallowMarkers[0][0]
marker2cough = swallowMarkers[0][1]

marker1vocalization = swallowMarkers[0][0]
marker2vocalization = swallowMarkers[0][1]

swallowDistance0 = swallowDistances[0]
coughDistance0 = coughDistances[0]
vocalizationDistance0 = vocalizationDistances[0]

swallowStrains = [abs(swallowDistances[frame][marker1swallow-1][marker2swallow-marker1swallow-1] - swallowDistance0[marker1swallow-1][marker2swallow-marker1swallow-1])/swallowDistance0[marker1swallow-1][marker2swallow-marker1swallow-1] for frame in swallowDistances]
coughStrains = [abs(coughDistances[frame][marker1cough-1][marker2cough-marker1cough-1] - coughDistance0[marker1cough-1][marker2cough-marker1cough-1])/coughDistance0[marker1cough-1][marker2cough-marker1cough-1] for frame in coughDistances]
vocalizationStrains = [abs(vocalizationDistances[frame][marker1vocalization-1][marker2vocalization-marker1vocalization-1] - vocalizationDistance0[marker1vocalization-1][marker2vocalization-marker1vocalization-1])/vocalizationDistance0[marker1vocalization-1][marker2vocalization-marker1vocalization-1] for frame in vocalizationDistances]

fig, axs = plt.subplots(3,1, sharex=True)
axs[0].plot(swallowTime, swallowStrains)
axs[0].set_title('Swallow Strains')
axs[0].set_ylabel('Strain')
axs[0].grid(True)
axs[1].plot(coughTime, coughStrains)
axs[1].set_title('Cough Strains')
axs[1].set_ylabel('Strain')
axs[1].grid(True)
axs[2].plot(vocalizationTime, vocalizationStrains)
axs[2].set_title('Vocalization Strains')
axs[2].set_ylabel('Strain')
axs[2].set_xlabel('Time [s]')
axs[2].grid(True)

fig.tight_layout(pad=3.0)
plt.show()
plt.savefig('strainPlot_subject5_leaned.png')