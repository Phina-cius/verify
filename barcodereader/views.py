import os
import time
from datetime import datetime
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from PIL import Image
from pyzbar.pyzbar import decode
from utills.django_open_cv import CameraStreamingWidget


def camera_feed(request):
    stream = CameraStreamingWidget()
    frames = stream.get_frames()

    # Handle AJAX request for barcode data
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        print("AJAX request received")
        image_path = os.path.join(os.getcwd(), "media", "images")
        image_files = [f for f in os.listdir(image_path) if f.endswith(".png")]

        if image_files:
            latest_image = max(image_files, key=lambda f: os.path.getmtime(os.path.join(image_path, f)))
            image = os.path.join(image_path, latest_image)

            im = Image.open(image)
            decoded_objects = decode(im)

            if decoded_objects:
                barcode_data = decoded_objects[0].data.decode("utf-8")
                file_saved_at = time.ctime(os.path.getmtime(image))
                return JsonResponse(data={"barcode_data": barcode_data, "file_saved_at": file_saved_at})

        return JsonResponse(data={"barcode_data": None})

    return StreamingHttpResponse(frames, content_type="multipart/x-mixed-replace; boundary=frame")


def detect(request):
    stream = CameraStreamingWidget()
    success, _ = stream.camera.read()
    return render(request, "index.html", context={"cam_status": success})
