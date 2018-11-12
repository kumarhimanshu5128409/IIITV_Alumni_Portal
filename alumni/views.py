import os

# third party
from cities_light.models import Country, Region, City

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
# local Django

from .forms import AlumniForm
from .models import Alumni
from .services import get_alumni_by_id
from .utils import check_correct_alumni


# Create your views here.
class AlumniUpdateView(LoginRequiredMixin, UpdateView, FormView):
    @method_decorator(check_correct_alumni)
    def dispatch(self, *args, **kwargs):
        return super(AlumniUpdateView, self).dispatch(*args, **kwargs)

    form_class = AlumniForm
    template_name = 'alumni/edit.html'
    success_url = reverse_lazy('alumni:profile')

    def get_context_data(self, **kwargs):
        context = super(AlumniUpdateView, self).get_context_data(**kwargs)
        alumni_id = self.kwargs['alumni_id']
        alumni = get_alumni_by_id(alumni_id)
        country_list = Country.objects.all()
        if alumni.country:
            country = alumni.country
            state_list = Region.objects.filter(country=country)
            context['state_list'] = state_list
        if alumni.state:
            state = alumni.state
            city_list = City.objects.filter(region=state)
            context['city_list'] = city_list
        context['country_list'] = country_list
        return context

    def get_object(self, queryset=None):
        alumni_id = self.kwargs['alumni_id']
        obj = Alumni.objects.get(pk=alumni_id)
        return obj

    def form_valid(self, form):
        alumni_id = self.kwargs['alumni_id']
        alumni = get_alumni_by_id(alumni_id)

        alumni_to_edit = form.save(commit=False)
        try:
            country_name = self.request.POST.get('country')
            country = Country.objects.get(name=country_name)
        except ObjectDoesNotExist:
            country = None
        alumni_to_edit.country = country
        try:
            state_name = self.request.POST.get('state')
            state = Region.objects.get(name=state_name)
        except ObjectDoesNotExist:
            state = None
        alumni_to_edit.state = state
        try:
            city_name = self.request.POST.get('city')
            city = City.objects.get(name=city_name)
        except ObjectDoesNotExist:
            city = None
        alumni_to_edit.city = city

        # update the alumni
        alumni_to_edit.save()
        return HttpResponseRedirect(reverse('alumni:profile', args=(alumni_id, )))


'''
  The view to display alumni profile.
  It uses DetailView which is a generic
  class-based views are designed to display data.
'''


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'alumni/profile.html'

    # @method_decorator(check_correct_alumni)
    # @method_decorator(alumni_id_check)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        alumni_id = self.kwargs['alumni_id']
        obj = Alumni.objects.get(id=alumni_id)
        return obj

