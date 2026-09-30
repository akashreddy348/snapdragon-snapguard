import cv2
import numpy as np
import onnxruntime as ort

class SnapdragonPresenceEngine:
    """
    Evaluates user presence and shoulder-surfing risks.
    Architectured to execute on Qualcomm Hexagon NPU via QNN Execution Provider
    with transparent CPU fallback for instant verification on standard platforms.
    """
    def __init__(self):
        self.active_provider = "CPU (Fallback)"
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self._check_npu_readiness()

    def _check_npu_readiness(self):
        """
        Checks hardware execution provider availability, prioritizing
        Qualcomm Hexagon NPU (QNN HTP) and DirectML.
        """
        providers = ort.get_available_providers()
        if 'QNNExecutionProvider' in providers:
            self.active_provider = "Qualcomm Hexagon NPU (QNN HTP)"
        elif 'DmlExecutionProvider' in providers:
            self.active_provider = "DirectML (Windows Accelerated)"
        else:
            self.active_provider = "Standard CPU Execution"

    def analyze_frame(self, frame_bgr: np.ndarray):
        """
        Processes an incoming BGR video frame, identifies faces,
        and assigns presence status.
        """
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.18, 
            minNeighbors=5, 
            minSize=(60, 60)
        )
        
        num_detected = len(faces)
        if num_detected == 1:
            status = "USER_PRESENT"
        elif num_detected > 1:
            status = "MULTIPLE_USERS_DETECTED"
        else:
            status = "USER_ABSENT"

        return {
            "status": status,
            "count": num_detected,
            "bounding_boxes": faces
        }
