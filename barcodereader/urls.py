
# the auther name :phinacius wafula simiyu
# the auther email:phinaciussimiyu143@gmail.com
# the auther phonenumber:+254798681812



from django.urls import path
from barcodereader import views

urlpatterns = [
    path("", views.detect, name="index"),
    path("camera_feed/", views.camera_feed, name="camera_feed"),
    path("get_latest_barcode/", views.get_latest_barcode, name="get_latest_barcode"),  # New fast barcode API
]
