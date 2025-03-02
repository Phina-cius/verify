import os
from datetime import datetime
import cv2
import numpy as np
from pyzbar.pyzbar import decode


class CameraStreamingWidget:
    def __init__(self):
        # Access the camera
        self.camera = cv2.VideoCapture(int(os.environ.get('CAMERA', 0)))  # Default to 0 if CAMERA not set
        self.media_path = os.path.join(os.getcwd(), "media", "images")

        # Ensure "media/images" folder exists
        if not os.path.exists(self.media_path):
            os.makedirs(self.media_path)

    def get_frames(self):
        while True:
            # Capture frame-by-frame
            success, frame = self.camera.read()
            if not success:
                break

            # Convert frame to grayscale (better barcode detection)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect barcodes using pyzbar
            barcodes = decode(gray_frame)

            # Process each detected barcode
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")  # Get barcode data
                barcode_type = barcode.type  # Get barcode type
                pts = np.array(barcode.polygon, np.int32).reshape((-1, 1, 2))

                # Draw bounding box around barcode
                cv2.polylines(frame, [pts], True, (0, 255, 0), 3)  # Green bounding box

                # Display barcode text
                x, y, w, h = barcode.rect
                cv2.putText(
                    frame,
                    f"{barcode_type}: {barcode_data}",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 0, 255),  # Red text
                    2,
                )

                # Save image with detected barcode
                image_path = os.path.join(self.media_path, f"barcode_{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
                cv2.imwrite(image_path, frame)

            # Encode frame
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()

            # Yield frame with barcode bounding boxes
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")
