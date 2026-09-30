import os
import sys

# Ensure repository root is added to Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import time
import cv2
import streamlit as st
from src.camera_feed import CameraFeedManager
from src.presence_engine import SnapdragonPresenceEngine

st.set_page_config(page_title="SnapGuard - Snapdragon Presence Sentinel", layout="centered")

st.title("🛡️ SnapGuard: On-Device Presence Sentinel")
st.caption("Engineered for Snapdragon-Powered HP PCs | Qualcomm AI Hub Runtime")

col_info1, col_info2 = st.columns(2)
engine = SnapdragonPresenceEngine()

with col_info1:
    st.metric("Target Device", "Snapdragon X Elite (HP)")
with col_info2:
    st.metric("Hardware Engine", engine.active_provider)

st.divider()

timeout_sec = st.slider("Auto-Lock Inactivity Threshold (seconds)", min_value=2, max_value=12, value=4)
run_detection = st.toggle("Start Live Sentinel Monitoring", value=False)

status_box = st.empty()
video_box = st.empty()

if run_detection:
    feed = CameraFeedManager()
    last_detected_time = time.time()

    for _ in range(40):
        frame = feed.read_frame()
        result = engine.analyze_frame(frame)
        current_time = time.time()

        for (x, y, w, h) in result["bounding_boxes"]:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if result["status"] == "USER_PRESENT":
            last_detected_time = current_time
            status_box.success("✅ **User Present** — System Active & Secure")
        elif result["status"] == "MULTIPLE_USERS_DETECTED":
            last_detected_time = current_time
            status_box.warning(f"⚠️ **Privacy Alert:** {result['count']} Faces Detected! (Shoulder-Surfing Warning)")
        else:
            elapsed = int(current_time - last_detected_time)
            remaining = max(0, timeout_sec - elapsed)
            if remaining == 0:
                status_box.error("🔒 **USER ABSENT:** Triggering Windows Auto-Lock Protocol...")
            else:
                status_box.warning(f"⏳ **No User Detected** — Locking in {remaining}s...")

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_box.image(frame_rgb, channels="RGB", use_container_width=True)
        time.sleep(0.1)

    feed.release()
else:
    status_box.info("Toggle 'Start Live Sentinel Monitoring' above to begin.")
