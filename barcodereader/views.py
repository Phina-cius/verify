# the auther name: phinacius wafula simiyu
# the auther email:phinaciussimiyu143@gmail.com
# the auther phone number:0798681812




from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from utills.django_open_cv import CameraStreamingWidget
from utills.upcitemdb import BarcodeVerifier

# Start streaming camera
stream = CameraStreamingWidget()

def camera_feed(request):
    return StreamingHttpResponse(stream.get_frames(), content_type="multipart/x-mixed-replace; boundary=frame")

def detect(request):
    success, _ = stream.camera.read()
    return render(request, "index.html", {"cam_status": success})

def get_latest_barcode(request):
    """Return the last detected barcode instantly (no image processing)."""
    if stream.latest_barcode:
        barcode_verifier = BarcodeVerifier()
        product_info = barcode_verifier.verify_barcode(stream.latest_barcode)
        if product_info:
            return JsonResponse({
                "barcode_data": stream.latest_barcode,
                "barcode_type": stream.latest_type,
                "product_info": product_info  # Add the verified product details

            })
        else:
            return JsonResponse({
                "barcode_data": stream.latest_barcode,
                "barcode_type": stream.latest_type,
                "error": "No product found for this barcode"
            })

    return JsonResponse({"barcode_data": None})
