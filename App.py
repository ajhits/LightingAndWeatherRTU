from flask import Flask, Response,jsonify
import cv2
import numpy as np
import imutils
from tracker.centroidtracker import CentroidTracker
from tracker.trackableobject import TrackableObject
import datetime
from imutils.video import FPS


app = Flask(__name__)

# Use your camera device index (0 for default camera)
camera = cv2.VideoCapture(0)

# Load the object detection model
prototxt = "detector/MobileNetSSD_deploy.prototxt"
model = "detector/MobileNetSSD_deploy.caffemodel"
net = cv2.dnn.readNetFromCaffe(prototxt, model)


trackableObjects = {}

# initialize the total number of frames processed thus far, along
# with the total number of objects that have moved either up or down
totalFrames = 0
totalDown = 0
totalUp = 0

# initialize empty lists to store the counting data
total = []
move_out = []
move_in =[]
out_time = []
in_time = []

# *********************** PERSON TRACKING TIME IN AND OUT
def generate_frames():

    global totalDown,totalUp,move_out,move_in,total
    
    # Initialize variables
    totalFrames = 0

	# start the frames per second throughput estimator
    fps = FPS().start()
 
    # Initialize the frame dimensions (we'll set them as soon as we read
    #  the first frame from the video)
    W = None
    H = None

    # Initialize the centroid tracker
    ct = CentroidTracker()

    # Define class labels
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]

    while True:
    
        success, frame = camera.read()
        frame = cv2.flip(frame, 1)
        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        if not success:
            break
        
        
        # if the frame dimensions are empty, set them
        if W is None or H is None:
            (H, W) = frame.shape[:2]

        # Check to see if we should run object detection
        if totalFrames % 30 == 0:
            # Initialize the list of people's centroids
            rects = []
            
            
            # set the status and initialize our new set of object trackers
            status = "Detecting"
            trackers = []


            # Convert the frame to a blob and pass it through the network
            blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
            net.setInput(blob)
            detections = net.forward()

            # Inside the loop where you process detections
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                
                
                # get minum threshold value
                if confidence > 0.4:
                    class_id = int(detections[0, 0, i, 1])

                    # detect it is person first
                    if CLASSES[class_id] == "person":
                    
                        # Extract the bounding box coordinates
                        box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                        (startX, startY, endX, endY) = box.astype("int")

                        # # Draw bounding boxes
                        # cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

                        # Compute the centroid of the bounding box
                        centroid_x = int((startX + endX) / 2)
                        centroid_y = int((startY + endY) / 2)

                        # Store the bounding box coordinates in 'rects'
                        rects.append((startX, startY, endX, endY))
                        
                        
        else:
            
    		# loop over the trackers
            for tracker in trackers:
                
				# set the status of our system to be 'tracking' rather
				# than 'waiting' or 'detecting'
                status = "Tracking"

				# update the tracker and grab the updated position
                tracker.update(rgb)
                pos = tracker.get_position()

				# unpack the position object
                startX = int(pos.left())
                startY = int(pos.top())
                endX = int(pos.right())
                endY = int(pos.bottom())

				# add the bounding box coordinates to the rectangles list
                rects.append((startX, startY, endX, endY))
                
                
# ********** THRESHOLD LINE 
		# draw a horizontal line in the center of the frame -- once an
		# object crosses this line we will determine whether they were
		# moving 'up' or 'down'
        cv2.line(frame, (0, H // 2), (W, H // 2), (0, 0, 0), 3)
        cv2.putText(frame, "-Prediction border - Entrance-", (10, H - ((i * 20) + 200)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

		# use the centroid tracker to associate the (1) old object
		# centroids with (2) the newly computed object centroids
        objects = ct.update(rects)

		# loop over the tracked objects
        for (objectID, centroid) in objects.items():
			# check to see if a trackable object exists for the current
			# object ID
            to = trackableObjects.get(objectID, None)

			# if there is no existing trackable object, create one
            if to is None:
                to = TrackableObject(objectID, centroid)

			# otherwise, there is a trackable object so we can utilize it
			# to determine direction
            else:
				# the difference between the y-coordinate of the *current*
				# centroid and the mean of *previous* centroids will tell
				# us in which direction the object is moving (negative for
				# 'up' and positive for 'down')
                y = [c[1] for c in to.centroids]
                direction = centroid[1] - np.mean(y)
                to.centroids.append(centroid)

				# check to see if the object has been counted or not
                if not to.counted:
        
 # ******************* EXIT   
					# if the direction is negative (indicating the object
					# is moving up) AND the centroid is above the center
					# line, count the object
                    if direction < 0 and centroid[1] < H // 2:
                        totalUp += 1
                        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        move_out.append(totalUp)
                        out_time.append(date_time)
                        to.counted = True

# ******************* ENTRY )
					# if the direction is positive (indicating the object
					# is moving down) AND the centroid is below the
					# center line, count the object
                    elif direction > 0 and centroid[1] > H // 2:
                        totalDown += 1
                        # date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        move_in.append(totalDown)
                        # in_time.append(date_time)
						# if the people limit exceeds over threshold, send an email alert
                        if sum(total) >= 30:
                            cv2.putText(frame, "-ALERT: People limit exceeded-", (10, frame.shape[0] - 80),
								cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 2)
			
                        to.counted = True
						# compute the sum of total people inside
                        total = []
                        total.append(len(move_in) - len(move_out))

			# store the trackable object in our dictionary
            trackableObjects[objectID] = to

			# draw both the ID of the object and the centroid of the
			# object on the output frame
            text = "ID {}".format(objectID)
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4, (255, 255, 255), -1)

        # ****** NOTE: display the output info_status

        info_status = [
		    ("Exit", totalUp),
		    ("Enter", totalDown),
		    ("Status", status),
		]
  
        for (i, (k, v)) in enumerate(info_status):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (153, 255, 255), 2)

            info_total = [
		        ("Total people inside", ', '.join(map(str, total))),
		    ]
            
        # info_total
        for (i, (k, v)) in enumerate(info_total):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (265, H - ((i * 20) + 60)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)



# ****** NOTE show the output frame
        cv2.imshow("Real-Time Monitoring/Analysis Window", frame)
        key = cv2.waitKey(1) & 0xFF
        

		# increment the total number of frames processed thus far and
		# then update the FPS counter
        totalFrames += 1
        fps.update()
     
            
        _, frame_encoded  = cv2.imencode('.png', frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded.tobytes() + b'\r\n')

@app.route('/video', methods=['GET'])
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=3000)
