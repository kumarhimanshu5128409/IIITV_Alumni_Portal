# standard library
from functools import wraps

# Django
# from django.http import Http404
from django.shortcuts import render
from django.http import Http404

# local Django
from alumni.services import get_alumni_by_id
from .models import Alumni


def alumni_id_check(func):
    @wraps(func)
    def wrapped_view(request, alumni_id):
        alu = getattr(request.user, 'alumni')
        if alu is None:
            return render(request, 'alumni/404.html', status=404)
        elif alu is False:
            alumni = get_alumni_by_id(alumni_id)
            if not alumni:
                return render(
                    request, 'alumni/404.html', status=404)
            if not int(alumni.id) == alu.id:
                return render(
                    request, 'alumni/404.html', status=404)
        return func(request, alumni_id=alumni_id)

    return wrapped_view


def check_correct_alumni(func):
    @wraps(func)
    def wrapped_view(request, **kwargs):
        req_alumni = getattr(request.user, "Alumni")
        alumni_id = kwargs['alumni_id']
        if not req_alumni:
            raise Http404
        elif req_alumni is not True:
            try:
                alumni = Alumni.objects.get(id=alumni_id)
            except Alumni.DoesNotExist:
                return render(
                    request, 'alumni/404.html', status=404)
            if alumni.id == req_alumni.id:
                return func(request, alumi=alumni_id)
            else:
                return render(
                    request, 'alumni/404.html', status=404)
        else:
            return render(request, 'alumni/404.html', status=404)

    return wrapped_view