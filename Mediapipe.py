import cv2
import mediapipe as mp

# Initialize MediaPipe
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(min_detection_confidence=0.3, min_tracking_confidence=0.5)

# Initialize OpenCV for capturing video
cap = cv2.VideoCapture(0)

ENTRY = 0
FINAL_ENTRY = 0
EXIT = 0
previous_chest_x = None  # Variable to store the previous chest X-coordinate
person_counted = False  # Flag to track if a person has been counted

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        continue

    # Initialize the frame dimensions (we'll set them as soon as we read
    # the first frame from the video)
    W = None
    H = None

    # if the frame dimensions are empty, set them
    if W is None or H is None:
        (H, W) = frame.shape[:2]

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

        # Calculate the chest level coordinates
        chest_x = (min_x + max_x) // 2
        chest_y = (min_y)  # You can modify this to fine-tune the chest level

        # Draw the bounding box
        cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)

        # Draw the chest-level dot as a red circle
        cv2.circle(frame, (chest_x, chest_y), 5, (0, 0, 255), -1)
        
        if previous_chest_x is not None:
            movement = chest_x - previous_chest_x
            
            if movement > 10 and chest_x >= 320 and not person_counted:
                movement_text = "Moving Right"
                ENTRY = 1
 
        previous_chest_x = chest_x
    
        FINAL_ENTRY = FINAL_ENTRY + ENTRY
       
    cv2.putText(frame, f"Entry: {FINAL_ENTRY} | Exit: {EXIT}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
    # Draw the vertical line
    cv2.line(frame, (W // 2, 0), (W // 2, H), (0, 0, 0), 3)
    cv2.line(frame, (315, 0), (315, H), (255, 0, 0), 1)
    cv2.line(frame, (640 - 315, 0), (640 - 315, H), (0, 0, 255), 1)

    # Display the frame with the bounding box, chest-level dot, and movement information
    cv2.imshow('Person Detection', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
