# third party

# Django
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView
from AlumniPortal import settings
# local Django
from cities_light.models import City, Region, Country
from registration.forms import UserForm
from registration.phone_validate import validate_phone
from registration.utils import  match_password
from registration.tokens import account_activation_token
from alumni.forms import AlumniForm


class AlumniSignupView(TemplateView):
    registered = False
    country_list = Country.objects.all()
    city_list = City.objects.all()
    region_list = Region.objects.all()
    phone_error = False
    match_error = False

    def get(self, request):
        if request.user.is_authenticated:
            return render(request,'pages/user_is_logged_in.html')
        else:
            user_form = UserForm(prefix="usr")
            alumni_form = AlumniForm(prefix="alu")
            return render(
                request, 'registration/signup_alumni.html', {
                    'user_form': user_form,
                    'alumni_form': alumni_form,
                    'registered': self.registered,
                    'phone_error': self.phone_error,
                    'match_error': self.match_error,
                    'country_list': self.country_list,
                    'city_list': self.city_list,
                    'region_list': self.region_list,
                })

    def post(self, request):

        if request.method == 'POST':
            user_form = UserForm(request.POST, prefix="usr")
            alumni_form = AlumniForm(request.POST, request.FILES, prefix="alu")
            if user_form.is_valid() and alumni_form.is_valid():
                password1 = request.POST.get('usr-password')
                password2 = request.POST.get('usr-confirm_password')
                if not match_password(password1, password2):
                    self.match_error = True
                    return render(
                        request, 'registration/signup_alumni.html', {
                            'user_form': user_form,
                            'alumni_form': alumni_form,
                            'registered': self.registered,
                            'phone_error': self.phone_error,
                            'match_error': self.match_error,
                            'country_list': self.country_list,
                            'city_list': self.city_list,
                            'region_list': self.region_list,
                        })
                try:
                    alu_country_name = request.POST.get('current_country')
                    alu_country = Country.objects.get(name=alu_country_name)
                except ObjectDoesNotExist:
                    alu_country = None

                try:
                    alu_state_name = request.POST.get('current_state')
                    alu_state = Region.objects.get(name=alu_state_name)
                except ObjectDoesNotExist:
                    alu_state = None

                try:
                    alu_city_name = request.POST.get('current_city')
                    alu_city = City.objects.get(name=alu_city_name)
                except ObjectDoesNotExist:
                    alu_city = None

                alu_phone = request.POST.get('alu-phone_number')

                if alu_country and alu_phone:
                    if not validate_phone(alu_country, alu_phone):
                        self.phone_error = True
                        return render(
                            request, 'registration/signup_alumni.html',
                            {
                                'user_form': user_form,
                                'alumni_form': alumni_form,
                                'registered': self.registered,
                                'phone_error': self.phone_error,
                                'match_error': self.match_error,
                                'country_list': self.country_list,
                                'city_list': self.city_list,
                                'region_list': self.region_list,
                            })

                user = user_form.save(commit=False)

                user.set_password(user.password)
                user.is_active = False
                user.save()

                alumni = alumni_form.save(commit=False)

                alumni.user = user
                alumni.country = alu_country
                alumni.city = alu_city
                alumni.state = alu_state
                alumni.save()

                print('nhi nhi yha pahooncha')

                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string(
                    'registration/acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                        'token': account_activation_token.make_token(user),
                    })
                to_email = alumni_form.cleaned_data.get('email')
                send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
                print('reached')
                return render(request, 'HomePage/email_ask_confirm.html')


            else:
                print('yha pahooncha kya')
                return render(
                    request, 'registration/signup_alumni.html', {
                        'user_form': user_form,
                            'alumni_form': alumni_form,
                            'registered': self.registered,
                            'phone_error': self.phone_error,
                            'match_error': self.match_error,
                            'country_list': self.country_list,
                            'city_list': self.city_list,
                            'region_list': self.region_list,
                    })


def activate(request, uidb64, token):
    """
    Checks token, if valid, then user will active and login

    :param uidb64: used to generate uid
    :param token: to be passed in request
    :return: email
    :raise: BadRequest
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'HomePage/confirmed_email.html')
    else:
        return HttpResponseBadRequest('Activation link is invalid!')

