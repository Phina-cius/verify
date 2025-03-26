# the auther name: phinacius wafula simiyu
# the auther email:phinaciussimiyu143@gmail.com
# the auther phone number:0798681812
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404
from barcodereader.decorator import admin_only
from utills.django_open_cv import CameraStreamingWidget
from utills.upcitemdb import BarcodeVerifier
from barcodereader.models import ManufacturerProfile,Product,Feedback,Barcode,ProductImage,Counterfeit_report,ProductVerificationLog
from utills.notifications import NotificationManager
import uuid
from django.utils.crypto import get_random_string
from django.contrib import messages

# Start streaming camera
stream = CameraStreamingWidget()

def camera_feed(request):
    return StreamingHttpResponse(stream.get_frames(), content_type="multipart/x-mixed-replace; boundary=frame")


def detect(request):
    # Camera status check
    success, _ = stream.camera.read()

    # User company check
    user_has_company = False
    if request.user.is_authenticated:
        user_has_company = ManufacturerProfile.objects.filter(user=request.user).exists()

    # Handle POST request
    if request.method == "POST":
        if stream.latest_barcode:
            counterfeit_report = Counterfeit_report(
                code=stream.latest_barcode
            )
            counterfeit_report.save()
            messages.success(request,"Thank you for reporting. We'll investigate this product")
            return redirect('index')

    context = {
        'user_has_company': user_has_company,
        'cam_status': success,
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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import ManufacturerProfile, Product
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST

def admin_check(user):
    return user.is_superuser or user.is_staff


@user_passes_test(admin_check)
def admin_manufacturer(request):
    # Initial queryset
    manufacturers = ManufacturerProfile.objects.select_related('user').prefetch_related('products').all()

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        manufacturers = manufacturers.filter(
            Q(company_name__icontains=search_query) |
            Q(Business_licence__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    # Status filtering
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'approved':
        manufacturers = manufacturers.filter(is_approved=True)
    elif status_filter == 'pending':
        manufacturers = manufacturers.filter(is_approved=False)

    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['company_name', 'created_at', 'user__email']:
        manufacturers = manufacturers.order_by(sort_by)

    # Pagination
    paginator = Paginator(manufacturers, 25)  # Show 25 manufacturers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'sort_by': sort_by,
        'total_manufacturers': manufacturers.count(),
        'approved_count': manufacturers.filter(is_approved=True).count(),
        'pending_count': manufacturers.filter(is_approved=False).count(),
    }
    return render(request, 'barcode/admin_manufacturer.html', context)

@require_POST
@user_passes_test(admin_check)
def approve_manufacturer(request, manufacturer_id):
    manufacturer = get_object_or_404(ManufacturerProfile, id=manufacturer_id)
    manufacturer.is_approved = True
    manufacturer.save()
    messages.success(request, f'{manufacturer.company_name} has been approved successfully!')
    return redirect('admin_manufacturer')


@require_POST
@user_passes_test(admin_check)
def reject_manufacturer(request, manufacturer_id):
    manufacturer = get_object_or_404(ManufacturerProfile, id=manufacturer_id)
    company_name = manufacturer.company_name
    manufacturer.delete()
    messages.success(request, f'{company_name} has been rejected and removed from the system.')
    return redirect('admin_manufacturer')


@user_passes_test(admin_check)
def manufacturer_detail(request, manufacturer_id):
    manufacturer = get_object_or_404(
        ManufacturerProfile.objects.select_related('user').prefetch_related('products'),
        id=manufacturer_id
    )
    products = manufacturer.products.all().order_by('-created_at')

    # Product search within manufacturer
    product_search = request.GET.get('product_search', '')
    if product_search:
        products = products.filter(
            Q(name__icontains=product_search) |
            Q(date_of_manufacture__icontains=product_search)
        )

        context = {
            'manufacturer': manufacturer,
            'products': products,
            'product_search': product_search,
        }
    return render(request, 'barcode/manufacturer_detail.html', context)


from django.db.models import Q
from django.core.paginator import Paginator


def admin_manufacturer(request):
    manufacturers = ManufacturerProfile.objects.select_related('user').prefetch_related('products').all()

    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        manufacturers = manufacturers.filter(
            Q(company_name__icontains=search_query) |
            Q(Business_licence__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )

    # Status filtering
    status_filter = request.GET.get('status', '')
    if status_filter == 'approved':
        manufacturers = manufacturers.filter(is_approved=True)
    elif status_filter == 'pending':
        manufacturers = manufacturers.filter(is_approved=False)

    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['company_name', '-company_name', 'created_at', '-created_at']:
        manufacturers = manufacturers.order_by(sort_by)

    # Pagination
    paginator = Paginator(manufacturers, 25)  # Show 25 per page
    page_number = request.GET.get('page')
    manufacturers = paginator.get_page(page_number)

    context = {
        'manufacturers': manufacturers,
        'approved_count': ManufacturerProfile.objects.filter(is_approved=True).count(),
        'pending_count': ManufacturerProfile.objects.filter(is_approved=False).count(),
    }
    return render(request, 'barcode/admin_manufacturer.html', context)


@admin_only
def admin_feedback(request):
    feedback_list = Feedback.objects.all().order_by('-created_at')
    total_feedback = feedback_list.count()

    # Pagination
    paginator = Paginator(feedback_list, 10)  # Show 10 feedback per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'feedback_list': page_obj,  # Now using paginated data
        'total_feedback': total_feedback,
        'recent_feedback': feedback_list[:5]  # For sidebar if needed
    }
    return render(request, 'barcode/admin_feedback.html', context)

@admin_only
def admin_verification(request):
    # Get all verification logs ordered by most recent
    verification_logs = ProductVerificationLog.objects.select_related(
        'product',
        'product__manufacturer',
        'product__barcode',
        'scanned_by'
    ).order_by('-scanned_at')

    # Get counts for stats
    total_verifications = verification_logs.count()
    genuine_count = verification_logs.filter(is_verified=True).count()
    counterfeit_count = verification_logs.filter(is_verified=False).count()

    # Get recent counterfeits (last 5)
    recent_counterfeits = verification_logs.filter(is_verified=False)[:5]

    # Other context data
    counterfeit_reports_count = Counterfeit_report.objects.count()
    total_feedback = Feedback.objects.count()

    context = {
        'verification_logs': verification_logs,
        'total_verifications': total_verifications,
        'genuine_count': genuine_count,
        'counterfeit_count': counterfeit_count,
        'recent_counterfeits': recent_counterfeits,
        'counterfeit_reports_count': counterfeit_reports_count,
        'total_feedback': total_feedback,
    }
    return render(request, 'barcode/verification_logs.html', context)


@admin_only
def admin_report(request):
    # Get all reports ordered by most recent
    reports = Counterfeit_report.objects.all().order_by('-reported_at')

    # Get counts for stats
    total_reports = reports.count()
    pending_reports = reports.filter(resolved=False).count()
    resolved_reports = reports.filter(resolved=True).count()

    # Pagination
    paginator = Paginator(reports, 25)  # Show 25 reports per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get recent feedback (last 5)
    recent_feedback = Feedback.objects.order_by('-created_at')[:5]

    # Other context data
    counterfeit_reports_count = Counterfeit_report.objects.filter(resolved=False).count()
    total_feedback = Feedback.objects.count()

    context = {
        'reports': page_obj,
        'total_reports': total_reports,
        'pending_reports': pending_reports,
        'resolved_reports': resolved_reports,
        'recent_feedback': recent_feedback,
        'counterfeit_reports_count': counterfeit_reports_count,
        'total_feedback': total_feedback,
    }
    return render(request, 'barcode/admin_reports.html', context)


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

    if not manufacturer.is_approved:
        messages.error(request, "Your company profile must be verified before you can upload products.")
        return redirect('my_company')

    if request.method == 'POST':
        # Create product
        product = Product(
            manufacturer=manufacturer,
            name=request.POST.get('name'),
            date_of_manufacture=request.POST.get('manufacture_date'),
            date_of_expiry=request.POST.get('expiry_date') or None,  # Handle optional expiry
            price=request.POST.get('price')
        )
        product.save()

        # Generate unique barcode and QR code values
        barcode_value = get_random_string(12, allowed_chars='0123456789')
        qr_code_value = str(uuid.uuid4())

        # Create barcode instance
        barcode = Barcode(
            product=product,
            barcode=barcode_value,
            qr_code=qr_code_value
        )
        barcode.save()  # This will trigger the save() method which generates images

        # Handle multiple image uploads
        images = request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return redirect('upload_product', id=id)
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


def user_feedback_page(request):
    user_has_company = False

    if request.user.is_authenticated:
        user_has_company = ManufacturerProfile.objects.filter(user=request.user).exists()
    context = {
        'user_has_company': user_has_company,
    }
    if request.method == 'POST':
        Feedback.objects.create(
            name=request.POST['name'],
            message=request.POST['message'],
        )
        messages.success(request,'We appreciate your feedback on "The Genuine Scan." It helps us improve!')
        return redirect('index')
    return render(request,'barcode/user_feedback.html',context)

#the function to report the counterfeit product

