from __future__ import print_function
import sys
import cv2
import numpy as np
import math
import pickle
import pandas as pd
import argparse


def main(args): 
    
    trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

    def createTrackerByName(trackerType):
      # Create a tracker based on tracker name
      if trackerType == trackerTypes[0]:
        tracker = cv2.legacy.TrackerBoosting_create()
      elif trackerType == trackerTypes[1]:
        tracker = cv2.legacy.TrackerMIL_create()
      elif trackerType == trackerTypes[2]:
        tracker = cv2.legacy.TrackerKCF_create()
      elif trackerType == trackerTypes[3]:
        tracker = cv2.legacy.TrackerTLD_create()
      elif trackerType == trackerTypes[4]:
        tracker = cv2.legacy.TrackerMedianFlow_create()
      elif trackerType == trackerTypes[5]:
        tracker = cv2.legacy.TrackerGOTURN_create()
      elif trackerType == trackerTypes[6]:
        tracker = cv2.legacy.TrackerMOSSE_create()
      elif trackerType == trackerTypes[7]:
        tracker = cv2.legacy.TrackerCSRT_create()
      else:
        tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in trackerTypes:
          print(t)
    
      return tracker
  
    # Set video to load
    videoNumber = str(args['videoNum'])
    # videoNumber = '1'
    videoName = "video"+videoNumber+".MOV"
    videoPath = videoName
        
    # Create a video capture object to read videos
    cap = cv2.VideoCapture(videoPath)

    # Read first frame
    success, frame = cap.read()
    firstframe = frame
    # quit if unable to read the video file
    if not success:
      print('Failed to read video')
      sys.exit(1)
        
    # Read pickles files saved from Dump.py
    bboxesName = "bboxes"+videoNumber+".pckl"
    f = open(bboxesName, 'rb')
    bboxes = pickle.load(f)
    f.close()
    
    colorsName = "colors"+videoNumber+".pckl"
    f = open(colorsName, 'rb')
    colors = pickle.load(f)
    f.close()

    # Specify the tracker type
    trackerType = "CSRT"  
    
    # Create MultiTracker object
    multiTracker = cv2.legacy.MultiTracker_create()
    
    # Initialize MultiTracker
    for bbox in bboxes:
      multiTracker.add(createTrackerByName(trackerType), frame, bbox)
      
    # Process video and track objects
    distances = []
    print("... Processing video " + videoNumber)
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
    
        # get updated location of objects in subsequent frames
        success, boxes = multiTracker.update(frame)
        
        # CALCULATIONS
        x_cords = []  # center x coordinate of each frame
        y_cords = []  # center y coordinate of each frame
      
        # get coordinates for center of each box since they are initially stored for the top left corner of the boxes
        for i in range(len(boxes)):
            x_m = boxes[i][0] + 0.5*boxes[i][2]
            y_m = boxes[i][1] + 0.5*boxes[i][3]
            x_cords.append(x_m)
            y_cords.append(y_m)
        
        
        
        # create 3D list of distances between every dot in every frame
        complist = []
        count = 0
        for i in range(len(boxes)-1):
            frameslist = []
            for j in range(count,len(boxes)-1):
                dist = np.sqrt((x_cords[i]-x_cords[j+1])**2 + (y_cords[i]-y_cords[j+1])**2)
                frameslist.append(dist)
            count += 1
            complist.append(frameslist)
        distances.append(complist)
      
        # draw tracked objects
        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
    
        # show frame
        # cv2.imshow('MultiTracker', frame)
      
        # # Get frame rate information
        # fps = int(cap.get(5))
        # print("Frame Rate : ",fps,"frames per second")	
    
        # # Get frame count
        # frame_count = cap.get(7)
        # print("Frame count : ", frame_count) 
    
        # quit on ESC button
        if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
            break

    # loop through the 3D list and collect all strains/locations above 10%
    ogpoint = 0                 # marker of interest
    comppoint = 0               # other marker of interest
    distance0 = distances[0]    # list of original distances to compare each frame to
    indicesset = set()          # set of j and k values to check to see if we already have them
    indiceslist = []            # list of markers and their strain 
    while True:    
        maximum = 0
        for i in range(1,len(distances)):
            for j in range(len(distances[i])):
                for k in range(len(distances[i][j])):
                    diff = abs(distances[i][j][k] - distance0[j][k])
                    strain = diff/distance0[j][k]
                    if strain > maximum and (j,k) not in indicesset:
                            maximum = strain
                            ogpoint = j
                            comppoint = k
                            indices = ogpoint, comppoint
        if len(indiceslist) == int(math.factorial(len(bboxes))/(2*(math.factorial(len(bboxes)-2)))):
            break
        if maximum < 0.1:
            break
        indicesset.add(indices)
        Target1 = ogpoint + 1                           # translate from python index to marker number
        Target2 = Target1 + comppoint + 1               # this is why it is important to select markers from left-right up-down
        indiceslist.append((Target1,Target2,maximum))   # marker numbers are stored from greatest to least strain
    
    # create lists of coordinates that will be used for drawing the lines on the heat map
    startcords = []
    endcords = []
    for i in range(len(indiceslist)):
        start = (int(bboxes[indiceslist[i][0] - 1][0] + 0.5*bboxes[indiceslist[i][0] - 1][2]), int(bboxes[indiceslist[i][0] - 1][1] + 0.5*bboxes[indiceslist[i][0] - 1][3]))
        startcords.append(start)
        end = (int(bboxes[indiceslist[i][1] - 1][0] + 0.5*bboxes[indiceslist[i][1] - 1][2]), int(bboxes[indiceslist[i][1] - 1][1] + 0.5*bboxes[indiceslist[i][1] - 1][3]))
        endcords.append(end)        
    
    # loop through list backwards so that strains are drawn from least to greatest (so larger strains are drawn on top and not covered up)
    # create list of strains and their associated color, used to create a scale below
    strainsandcolor = []
    i = len(startcords) - 1
    while i >= 0:
        cv2.line(firstframe, startcords[i], endcords[i], (0,int(255-255*indiceslist[i][2]/indiceslist[0][2]),255), 3) #Color: BGR
        strainswithcolor = (indiceslist[i][2],(0,int(255-255*indiceslist[i][2]/indiceslist[0][2]),255))
        strainsandcolor.append(strainswithcolor)
        i -= 1
    
    # create scale for strains
    indexchange = int(len(strainsandcolor)/5)       
    cv2.putText(firstframe, "{:.3f}".format(strainsandcolor[-1][0]), (5,65), cv2.FONT_HERSHEY_SIMPLEX, 2, strainsandcolor[-1][1], 3) 
    cv2.putText(firstframe, "{:.3f}".format(strainsandcolor[3*indexchange][0]), (5,115), cv2.FONT_HERSHEY_SIMPLEX, 2, strainsandcolor[3*indexchange][1], 3) 
    cv2.putText(firstframe, "{:.3f}".format(strainsandcolor[2*indexchange][0]), (5,165), cv2.FONT_HERSHEY_SIMPLEX, 2, strainsandcolor[2*indexchange][1], 3) 
    cv2.putText(firstframe, "{:.3f}".format(strainsandcolor[indexchange][0]), (5,215), cv2.FONT_HERSHEY_SIMPLEX, 2, strainsandcolor[indexchange][1], 3) 
    cv2.putText(firstframe, "{:.3f}".format(strainsandcolor[0][0]), (5,265), cv2.FONT_HERSHEY_SIMPLEX, 2, strainsandcolor[0][1], 3) 

    # store top 5 strains/locations
    strainsLittleList = []
    marker1LittleList = []
    marker2LittleList = []
    for i in range(5):
        strainsLittleList.append(indiceslist[i][2])
        marker1LittleList.append(indiceslist[i][0])
        marker2LittleList.append(indiceslist[i][1])
        print("Strain" + str(i+1) + " = " + "{:.3f}".format(indiceslist[i][2]) + " between markers " + str(indiceslist[i][0]) + " and " + str(indiceslist[i][1]))

    # cv2.imshow('Results', firstframe)
    
    imageName = "heatMap"+videoNumber+".jpg"
    cv2.imwrite(imageName, firstframe)
    
    # strainsLittleArray = np.array(strainsLittleList)

    df = pd.DataFrame({"Strain 1": [strainsLittleList[0]],
                   "S1: Marker 1": [marker1LittleList[0]],
                   "S1: Marker 2": [marker2LittleList[0]],
                   "Strain 2": [strainsLittleList[1]],
                   "S2: Marker 1": [marker1LittleList[1]],
                   "S2: Marker 2": [marker2LittleList[1]],
                   "Strain 3": [strainsLittleList[2]],
                   "S3: Marker 1": [marker1LittleList[2]],
                   "S3: Marker 2": [marker2LittleList[2]],
                   "Strain 4": [strainsLittleList[3]],
                   "S4: Marker 1": [marker1LittleList[3]],
                   "S4: Marker 2": [marker2LittleList[3]],
                   "Strain 5": [strainsLittleList[4]],
                   "S5: Marker 1": [marker1LittleList[4]],
                   "S5: Marker 2": [marker2LittleList[4]]})

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    excelName = "data"+videoNumber+".xlsx"
    writer = pd.ExcelWriter(excelName, engine='xlsxwriter')
    
    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Provide Video Number')
    parser.add_argument('--videoNum', required = True)
    
    args = vars(parser.parse_args())
    
    main(args)