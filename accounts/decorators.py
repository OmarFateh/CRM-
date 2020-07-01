from django.shortcuts import redirect
from django.http import HttpResponse

# unauthenticated user 
# if the user is logged in, this restricts him from visiting the register page and redirects him to the dashboard page 

def unauthenticated_user(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        else:    
            return view_func(request,*args, **kwargs)
    return wrapper_func    


# allowed users 
# we pass a list of allowed groups to visit the page, and if not, it will redirect the other groups to another page  

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists(): # check if the user belongs to any groups 
                group = request.user.groups.all()[0].name  # then assign the name of the group to the first group the user belongs to 
            if group in allowed_roles:   # if the user's group in the list of allowed roles, then it returns the normal page
                return view_func(request, *args, **kwargs)
            # else:  # if not, it returns http response 
                # return HttpResponse('Sorry! You are not authorized to visit this page')
            else:    # if not, it redirects the user to his profile page
                return redirect('accounts:profile')    
        return wrapper
    return decorator        
