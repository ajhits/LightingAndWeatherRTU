import mediapipe as mp
import cv2
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class ObjectDetector:
    def __init__(self, model: str):
        self.model = model
        self.detector = None
        self.detection_result_list = []

    def visualize_callback(self, result: vision.ObjectDetectorResult,
                           output_image: mp.Image, timestamp_ms: int):
        
        try:
            result.timestamp_ms = timestamp_ms
            self.detection_result_list.append(result)
        except Exception as e:
            print("Object - visualize_callback(): ",e)

    def run(self):
        
        try:
            # Initialize the object detection model
            base_options = python.BaseOptions(model_asset_path=self.model)
            options = vision.ObjectDetectorOptions(base_options=base_options,
                                               running_mode=vision.RunningMode.LIVE_STREAM,
                                               score_threshold=0.7,
                                               result_callback=self.visualize_callback)
            self.detector = vision.ObjectDetector.create_from_options(options)
        except Exception as e:
            print("Object - run(): ",e)

    def visualize(self,image,detection_result):
        """Draws bounding boxes on the input image and return it.
        Args:
            image: The input RGB image.
            detection_result: The list of all "Detection" entities to be visualized.
        Returns:
            Image with bounding boxes.
        """
        
        
        MARGIN = 1  # pixels
        ROW_SIZE = 1  # pixels
        FONT_SIZE = 1
        FONT_THICKNESS = 1
        TEXT_COLOR = (255, 0, 0)  # red

        for detection in detection_result.detections:
            # Draw bounding_box
            bbox = detection.bounding_box
            start_point = bbox.origin_x, bbox.origin_y
            end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
            cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)

            # Draw label and score
            category = detection.categories[0]
            category_name = category.category_name
            probability = round(category.score, 2)
            result_text = category_name + ' (' + str(probability) + ')'
            text_location = (MARGIN + bbox.origin_x,
                     MARGIN + ROW_SIZE + bbox.origin_y)
            cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)

        return image

    def detect_objects(self, frame):
        
        try:
            # Convert the frame to an mp.Image object
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

            # Run object detection using the model
            timestamp_ms = int(time.time() * 1000)  # current timestamp in milliseconds
            self.detector.detect_async(mp_image, timestamp_ms=timestamp_ms)


            if self.detection_result_list:
            # Get the detection result and visualize it
                vis_image = self.visualize(frame, self.detection_result_list[0])
                self.detection_result_list.clear()
                return vis_image
        


            # If no objects detected, return the original frame
            return frame
        except Exception as e:
            print("Object - detect_objects(): ",e)
            return frame
