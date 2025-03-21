# the auther name: phinacius wafula simiyu
# the auther email:phinaciussimiyu143@gmail.com
# the auther phone number:0798681812

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404
from barcodereader.decorator import admin_only
from utills.django_open_cv import CameraStreamingWidget
from utills.upcitemdb import BarcodeVerifier
from barcodereader.models import ManufacturerProfile,Product,Feedback

# Start streaming camera
stream = CameraStreamingWidget()

def camera_feed(request):
    return StreamingHttpResponse(stream.get_frames(), content_type="multipart/x-mixed-replace; boundary=frame")


def detect(request):
    success, _ = stream.camera.read()
    user_has_company = False
    if request.user.is_authenticated:
        user_has_company = ManufacturerProfile.objects.filter(user=request.user).exists()

    context = {
        'user_has_company': user_has_company,
        "cam_status": success,
    }
    return render(request, "index.html", context)

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
                "error": "This product is not recognized. It may be fake."
            })

    return JsonResponse({"barcode_data": None})
#defining the dashboard for the admin
@admin_only
def dashboard(request):
    manufactures=ManufacturerProfile.objects.all()
    feedbacks=Feedback.objects.all()
    total_feedback=Feedback.objects.all().count()
    total_manufacturer=ManufacturerProfile.objects.all().count()
    total_products = Product.objects.count()
    pending_approvals = ManufacturerProfile.objects.filter(is_approved=False).count()
    context = {
        'total_feedback': total_feedback,
        'manufactures':manufactures,
        'feedbacks':feedbacks,
        'total_manufacturers': total_manufacturer,
        'total_products': total_products,
        'pending_approvals': pending_approvals,
    }

    return render(request,'barcode/admin_dashboard.html',context)

@admin_only
def admin_manufacturer(request):
    total_feedback = Feedback.objects.all().count()
    context ={
        'total_feedback': total_feedback,
    }
    return render(request,'barcode/admin_manufacturer.html',context)

@admin_only
def admin_feedback(request):
    total_feedback = Feedback.objects.all().count()
    context = {
        'total_feedback': total_feedback,
    }
    return  render(request,'barcode/admin_feedback.html',context)
@admin_only
def admin_verification(request):
    total_feedback = Feedback.objects.all().count()
    context = {
        'total_feedback': total_feedback,
    }
    return render(request,'barcode/verification_logs.html',context)
@admin_only
def admin_report(request):
    total_feedback = Feedback.objects.all().count()
    context = {
        'total_feedback': total_feedback,
    }
    return render(request,'barcode/admin_reports.html',context)

@admin_only
def approve_manufacturer(request,id):
    manufacturerProfile=ManufacturerProfile.objects.get(id=id)
    manufacturerProfile.is_approved = True
    manufacturerProfile.save()
    return redirect('/admin_dashboard')

@admin_only
def disapprove_manufacturer(request,id):
    manufacturerProfile=ManufacturerProfile.objects.get(id=id)
    manufacturerProfile.is_approved = False
    manufacturerProfile.save()
    return redirect('/admin_dashboard')

@login_required
def register_company(request):
    user_has_company = False

    if request.user.is_authenticated:
        user_has_company = ManufacturerProfile.objects.filter(user=request.user).exists()

    if request.method == 'POST':
        manufacurerProfile=ManufacturerProfile(
            user = request.user,
            company_name=request.POST['company_name'],
            Business_licence=request.POST['Business_licence'],
            address=request.POST['address'],
            phone_number=request.POST['phone_number'],
        )
        manufacurerProfile.save()
        return redirect('/my_company')

    context = {
        'user_has_company': user_has_company,
    }

    return render(request, 'barcode/register_company.html', context)

@login_required
def my_company(request):
    # Fetch the user's company profiles
    manufactures = ManufacturerProfile.objects.filter(user=request.user)
    user_has_company = manufactures.exists()

    # Prepare context for the template
    context = {
        'user_has_company': user_has_company,
        'manufactures': manufactures,
    }

    # Handle form submission
    if request.method == 'POST':
        try:
            # Create a new ManufacturerProfile instance
            ManufacturerProfile.objects.create(
                user=request.user,
                company_name=request.POST['company_name'],
                Business_licence=request.POST['Business_licence'],
                address=request.POST['address'],
                phone_number=request.POST['phone_number'],
            )
            # Redirect to the same page after successful submission
            return redirect('my_company')
        except KeyError as e:
            # Handle missing form fields gracefully
            context['error'] = f"Missing required field: {e}"
            return render(request, 'barcode/my_company.html', context)

    # Render the template
    return render(request, 'barcode/my_company.html', context)


@login_required
def upload_product(request, id):
    manufacturer = get_object_or_404(ManufacturerProfile, id=id)
    products = Product.objects.filter(manufacturer=manufacturer).select_related('barcode').prefetch_related('images')

    user_has_company = False
    if request.user.is_authenticated:
        user_has_company = ManufacturerProfile.objects.filter(user=request.user).exists()

    context = {
        'products': products,
        'user_has_company': user_has_company,
    }
    return render(request, 'barcode/upload-product.html', context)


@login_required
def delete_company(request, id):

    # Ensure the ManufacturerProfile belongs to the logged-in user
    manufacturerProfile = get_object_or_404(ManufacturerProfile, id=id, user=request.user)

    # Delete the ManufacturerProfile
    manufacturerProfile.delete()

    # Check if the user has any other ManufacturerProfile
    if ManufacturerProfile.objects.filter(user=request.user).exists():
        return redirect('/my_company')
    else:
        return redirect('/register_company')


@login_required
def delete_products(request, id):
    # Ensure the product belongs to the logged-in user's company
    product = get_object_or_404(Product, id=id, manufacturer__user=request.user)
    # Delete the product
    product.delete()
    # Redirect to the product upload page or any other page
    return redirect('upload_product', id=product.manufacturer.id)