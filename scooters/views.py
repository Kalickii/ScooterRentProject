from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from rest_framework.reverse import reverse_lazy

from scooters.models import Scooter


class ScooterListView(ListView):
    model = Scooter
    context_object_name = 'scooters'
    template_name = 'scooters/scooter_list.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Scooter.objects.all()
        return Scooter.objects.filter(available=True)


class ScooterDetailView(DetailView):
    model = Scooter
    context_object_name = 'scooter'
    template_name = 'scooters/scooter_detail.html'
    pk_url_kwarg = 'scooter_id'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Scooter.objects.all()
        return Scooter.objects.filter(available=True)

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            Scooter.objects.get(pk=self.kwargs['scooter_id']).delete()
            return redirect('scooter-list')


class ScooterUpdateView(UserPassesTestMixin, UpdateView):
    model = Scooter
    template_name = 'scooters/scooter_edit.html'
    pk_url_kwarg = 'scooter_id'
    fields = [
        'available',
        'image',
        'daily_price',
        'weekly_price',
        'monthly_price',
        'deposit_amount',
    ]

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        raise Http404

    def get_success_url(self):
        return reverse_lazy('scooter-detail', kwargs={'scooter_id': self.object.pk})


class ScooterCreateView(UserPassesTestMixin, CreateView):
    model = Scooter
    template_name = 'scooters/scooter_create.html'
    fields = [
        'brand',
        'scooter_model',
        'capacity',
        'year',
        'registration_number',
        'available',
        'image',
        'daily_price',
        'weekly_price',
        'monthly_price',
        'deposit_amount',
    ]

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        raise Http404

    def get_success_url(self):
        return reverse_lazy('scooter-detail', kwargs={'scooter_id': self.object.pk})
