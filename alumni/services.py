# Django
from django.core.exceptions import ObjectDoesNotExist

# local Django
from .models import Alumni


def delete_alumni(alumni_id):
    result = False

    alumni = get_alumni_by_id(alumni_id)

    if alumni:
        # Django docs recommend to set associated user
        # to not active instead of deleting the user
        user = alumni.user
        user.is_active = False
        # make a call to update the user
        user.save()
        # then delete the alumni
        alumni.delete()
        result = True
    return result


def get_all_alumni():
    alumni_list = Alumni.objects.all()
    return alumni_list


def get_alumni_by_id(alumni_id):
    is_valid = True
    result = None

    try:
        alumni = Alumni.objects.get(pk=alumni_id)
    except ObjectDoesNotExist:
        is_valid = False

    if is_valid:
        result = alumni

    return result


def get_alumni_resume_file_url(alumni_id):

    result = None
    alumni = get_alumni_by_id(alumni_id)

    if alumni and alumni.resume_file:
        result = alumni.resume_file.url

    return result


def get_alumni_ordered_by_first_name():
    alumni_list = Alumni.objects.all().order_by('first_name')
    return alumni_list


def has_resume_file(alumni_id):

    result = False
    alumni = get_alumni_by_id(alumni_id)

    if alumni and alumni.resume_file:
        result = True

    return result


def search_alumni(first_name, last_name, permanent_address, current_city, current_state, current_country, area_of_expertise, email):
    """alumnis search
    None, one, or more parameters may be sent:
    first_name, last_name, permanent address, current_city, current_state, current_country, area_of_expertise, email

    If no search parameters are given, it returns all alumnis

    Examples:
    search_alumnis(None, None, None, None, None, None, None, None))
    will return all alumnis
    search_alumnis("Yoshi", None, None, None, None, None, None, None)
    will return all alumnis with the first name "Yoshi"
    search_alumnis(None, "Doe", None, None, None, None, None, None)
    will return all alumnis with the last name "Doe"
    """

    # if no search parameters are given, it returns all alumnis
    search_query = Alumni.objects.all()
    # build query based on parameters provided
    if first_name:
        search_query = search_query.filter(first_name__icontains=first_name)
    if last_name:
        search_query = search_query.filter(last_name__icontains=last_name)
    if current_city:
        search_query = search_query.filter(city__name__icontains=current_city)
    if current_state:
        search_query = search_query.filter(state__name__icontains=current_state)
    if current_country:
        search_query = search_query.filter(country__name__icontains=current_country)
    if area_of_expertise:
        search_query = search_query.filter(area_of_expertise__icontains=area_of_expertise)
    if permanent_address:
        search_query = search_query.filter(permanent_address__icontains=permanent_address)
    if email:
        search_query = search_query.filter(email__icontains=email)
    return search_query.distinct()

