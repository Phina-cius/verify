
# the auther name :phinacius wafula simiyu
# the auther email:phinaciussimiyu143@gmail.com
# the auther phonenumber:+254798681812



from django.urls import path
from barcodereader import views

urlpatterns = [
    path("", views.detect, name="index"),
    path("admin_dashboard/",views.dashboard,name="admin_dashboard"),
    path("camera_feed/", views.camera_feed, name="camera_feed"),
    path("get_latest_barcode/", views.get_latest_barcode, name="get_latest_barcode"),
    path("admin_manufacturer",views.admin_manufacturer, name="admin_manufacturer"),
    path("admin_feedback",views.admin_feedback, name="admin_feedback"),
    path("admin_verification",views.admin_verification, name="admin_verification"),
    path("admin-reports",views.admin_report,name="admin_report"),
    path('approve/<int:id>',views.approve_manufacturer),
    path('disapprove/<int:id>',views.disapprove_manufacturer),
    path('register_company/',views.register_company,name="register_company"),
    path('my_company/',views.my_company,name="my_company"),
    path('upload_product/<int:id>',views.upload_product,name='upload_product'),
    path('delete_company/<int:id>',views.delete_company),
    path('delete_products/<int:id>',views.delete_products),
    path('user_feedback_page/',views.user_feedback_page,name="user_feedback_page"),
    path('admin/manufacturers/<int:manufacturer_id>/approve/', views.approve_manufacturer, name='approve_manufacturer'),
    path('admin/manufacturers/<int:manufacturer_id>/reject/', views.reject_manufacturer, name='reject_manufacturer'),
    path('admin/manufacturers/<int:manufacturer_id>/', views.manufacturer_detail, name='manufacturer_detail'),
]
