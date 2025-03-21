# the auther name: phinacius wafula simiyu
# the auther email: phinaciussimiyu143@gmail.com
# the auther phone number: +254798681812


from django.http import HttpResponse
from django.shortcuts import redirect


def allowed_users(allowed_roles=[]):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            group=None
            if not request.user.is_authenticated:
                return func(request, *args, **kwargs)
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                print('working',allowed_roles)
                return func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not allowed to access this page')
        return wrapper
    return decorator


#define the admin only
def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        group=None

        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group == 'admin':
            return view_func(request, *args, **kwargs)

        else:
            return redirect('/')




    return wrapper