import cv2
import numpy as np

class CameraFeedManager:
    """Manages webcam capture with synthetic frame generation for headless cloud servers."""
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.has_hardware = self.cap.isOpened()

    def read_frame(self):
        if self.has_hardware:
            ret, frame = self.cap.read()
            if ret:
                return frame
        
        # Headless Cloud Fallback: generate synthetic test pattern with a mock face circle
        mock_canvas = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(mock_canvas, "SNAPDRAGON NPU SENTINEL (CLOUD DEMO)", (40, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 180), 2)
        
        # Draw mock face silhouette
        cv2.circle(mock_canvas, (320, 240), 90, (200, 200, 200), -1)
        cv2.circle(mock_canvas, (290, 210), 12, (50, 50, 50), -1)
        cv2.circle(mock_canvas, (350, 210), 12, (50, 50, 50), -1)
        cv2.ellipse(mock_canvas, (320, 270), (40, 20), 0, 0, 180, (50, 50, 50), 3)
        return mock_canvas

    def release(self):
        if self.has_hardware:
            self.cap.release()
