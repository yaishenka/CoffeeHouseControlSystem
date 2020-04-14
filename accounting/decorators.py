from users.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def seller_rights_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated:
            return decorated_view_func(request)

        if request.user.is_seller:
            return function(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('home', args=(), kwargs={}))

    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper


def manager_rights_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated:
            return decorated_view_func(request)

        if request.user.is_manager:
            return function(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('home', args=(), kwargs={}))

    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper
