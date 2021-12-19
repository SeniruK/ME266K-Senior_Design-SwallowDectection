from __future__ import print_function
import sys
import cv2
from random import randint
import pickle


# Set video to load
# manually change videoNumber to correspond with the video to be processed
videoNumber = "1"
videoName = "video"+videoNumber+".MOV"
videoPath = videoName

# Create a video capture object to read videos
cap = cv2.VideoCapture(videoPath)

# Read first frame
success, frame = cap.read()
firstframe = frame
down_width = 1920
down_height = 1080
down_points = (down_width, down_height)
resized_down = cv2.resize(frame, down_points, interpolation= cv2.INTER_LINEAR)
# quit if unable to read the video file
if not success:
  print('Failed to read video')
  sys.exit(1)
 
# ----------------------------------------------------------------------------
  
# Step 3: Locate Objects in the First Frame

## Select boxes
smallbboxes = []
colors = [] 

# OpenCV's selectROI function doesn't work for selecting multiple objects in Python
# So we will call this function in a loop till we are done selecting all objects
while True:
  # draw bounding boxes over objects
  # selectROI's default behaviour is to draw box starting from the center
  # when fromCenter is set to false, you can draw box starting from top left corner
  bbox = cv2.selectROI('MultiTracker', resized_down)
  smallbboxes.append(bbox)
  colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
  print("Press q to quit selecting boxes and start tracking")
  print("Press any other key to select next object")
  k = cv2.waitKey(0) & 0xFF
  if (k == 113):  # q is pressed
    break

print('Video' + videoNumber + ' Selected bounding boxes {}'.format(smallbboxes),'\n')
print('Number of selected markers for video' + videoNumber + ': ' + str(len(smallbboxes)))

bboxes = []
for i in range(len(smallbboxes)):
    fourKcoords = (2*smallbboxes[i][0], 2*smallbboxes[i][1], 2*smallbboxes[i][2], 2*smallbboxes[i][3])
    bboxes.append(fourKcoords)

bboxesName = "bboxes"+videoNumber+".pckl"
f = open(bboxesName, 'wb')
pickle.dump(bboxes, f)
f.close()

colorsName = "colors"+videoNumber+".pckl"
f = open(colorsName, 'wb')
pickle.dump(colors, f)
f.close()
