import cv2
import mediapipe as mp


# Initialize MediaPipe
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(min_detection_confidence=0.3, min_tracking_confidence=0.5)

# Initialize OpenCV for capturing video
cap = cv2.VideoCapture(1)

# Initialize variables to track previous dot position and entry/exit
prev_chest_x, prev_chest_y = None, None
entry_count, exit_count = 0, 0

# Define the threshold for leftmost edge
leftmost_threshold = 50  # Adjust this value as needed
vertical_line_x = 640  # X-coordinate of the vertical line

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    if not ret:
        continue
    
    
    rects = []
    
    # Initialize the frame dimensions (we'll set them as soon as we read
    #  the first frame from the video)
    W = None
    H = None
    
    # if the frame dimensions are empty, set them
    if W is None or H is None:
        (H, W) = frame.shape[:2]
        print(W)



    # Convert the BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame using MediaPipe
    results = holistic.process(frame_rgb)

    if results.pose_landmarks:
        # If pose landmarks are detected, it's a person
        # Get the bounding box around the person
        bbox_cords = results.pose_landmarks.landmark
        min_x, max_x, min_y, max_y = 1, -1, 1, -1

        for landmark in bbox_cords:
            x, y, _ = landmark.x, landmark.y, landmark.z
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        min_x, max_x, min_y, max_y = int(min_x * frame.shape[1]), int(max_x * frame.shape[1]), int(min_y * frame.shape[0]), int(max_y * frame.shape[0])

        # Store the bounding box coordinates in 'rects'
        rects.append((min_x, max_x, min_y, max_y))
                        
        # Calculate the chest level coordinates
        chest_x = (min_x + max_x) // 2
        chest_y = (min_y + min_y) // 2  # You can modify this to fine-tune the chest level

        # Draw the bounding box
        cv2.rectangle(frame, (min_x + 10, min_y - 70), (max_x + 10, max_y - 70), (0, 255, 0), 2)

        # Draw the chest-level dot as a red circle
        cv2.circle(frame, (chest_x, chest_y), 5, (0, 0, 255), -1)

        # Track movement
        if prev_chest_x is not None:
            movement_x = chest_x - prev_chest_x


            # Check if the person is crossing the threshold (vertical line)
            if movement_x < -leftmost_threshold and chest_x < vertical_line_x:
                entry_count += 1
            elif movement_x > leftmost_threshold and chest_x > vertical_line_x:
                exit_count += 1

 
        prev_chest_x = chest_x
        
        cv2.putText(frame, f"Movement: {chest_x}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        

        
    cv2.putText(frame, f"Entry: {entry_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Exit: {exit_count}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
           
    # Draw the vertical line
    cv2.line(frame, (W // 2, 0), (W // 2, H), (0, 0, 0), 3)

    # Display the frame with the bounding box, chest-level dot, movement information, entry/exit counts, and leftmost edge indication
    cv2.imshow('Person Detection', frame)
    

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
