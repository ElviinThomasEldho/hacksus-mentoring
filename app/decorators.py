from django.http import HttpResponse
from django.shortcuts import redirect

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('loginUser')

    return wrapper_func

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        groups = None
        if request.user.groups.exists(): 
            groups = set(group.name for group in request.user.groups.all())
            for group in groups:
                print('Admin', group)
                if 'Admin' == group:
                    return view_func(request, *args, **kwargs)
        return redirect('loginUser')
    return wrapper_func

def admin_mentor_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        groups = None
        if request.user.groups.exists(): 
            groups = set(group.name for group in request.user.groups.all())
            for group in groups:
                print('Admin', group)
                if 'Admin' == group or 'Mentor' == group:
                    return view_func(request, *args, **kwargs)
        return redirect('loginUser')
    return wrapper_func

def mentor_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        groups = None
        if request.user.groups.exists(): 
            groups = set(group.name for group in request.user.groups.all())
            for group in groups:
                print('Mentor', group)
                if 'Mentor' == group:
                    return view_func(request, *args, **kwargs)
        return redirect('loginUser')
    return wrapper_func

def team_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        groups = None
        if request.user.groups.exists(): 
            groups = set(group.name for group in request.user.groups.all())
            for group in groups:
                print('Team', group)
                if 'Team' == group:
                    return view_func(request, *args, **kwargs)
        return redirect('loginUser')
    return wrapper_func

