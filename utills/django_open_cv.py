
# the auther name :phinacius wafula simiyu
# the auther email:phinaciussimiyu143@gmail.com
# the auther phonenumber:+254798681812




import os
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from datetime import datetime

class CameraStreamingWidget:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)  # Open camera
        self.latest_barcode = None  # Store last detected barcode
        self.latest_type = None  # Store last barcode type

    def get_frames(self):
        while True:
            success, frame = self.camera.read()
            if not success:
                break

            # Convert frame to grayscale (improves detection)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect barcodes
            barcodes = decode(gray_frame)

            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")  # Extract barcode text
                barcode_type = barcode.type
                pts = np.array(barcode.polygon, np.int32).reshape((-1, 1, 2))

                # Draw bounding box
                cv2.polylines(frame, [pts], True, (0, 255, 0), 3)  # Green rectangle
                x, y, w, h = barcode.rect
                cv2.putText(frame, f"{barcode_type}: {barcode_data}", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                # Store latest barcode (fast access)
                self.latest_barcode = barcode_data
                self.latest_type = barcode_type

            # Encode frame
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Return frame with barcode boxes
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
