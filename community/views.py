from alumni.models import Alumni
from django.views import generic
from django.db.models import Q


class CommunityView(generic.ListView):
    template_name = 'community/community.html'

    def get_queryset(self):
        request = self.request
        queryset_list = Alumni.objects.all()
        query = request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(area_of_expertise__icontains=query) |
                Q(permanent_address__icontains=query) |
                Q(email__icontains=query)
            ).distinct()
        return queryset_list
