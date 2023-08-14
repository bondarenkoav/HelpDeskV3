import logging

from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, DetailView
from django.views.generic.list import ListView

from base.models import Event, Status, Profile
from maintenance.apps import MaintenanceConfig
from maintenance.forms import *
from maintenance.models import *


logger = logging.getLogger(__name__)

events = Event.objects.all()

app = MaintenanceConfig.name
app_name = 'Техническое обслуживание'


class MaintenanceObjectList(LoginRequiredMixin, ListView, FormView):
    template_name = "maintenance/maintenance_object_list.html"
    model = MaintenanceObject
    form_class = MaintenanceObjectCreateForm
    success_url = reverse_lazy('maintenance:getlist_objects', args=['open'])
    paginate_by = 5

    def get_form_kwargs(self):
        kwargs = super(MaintenanceObjectList, self).get_form_kwargs()
        kwargs.update({'initial': {'user': self.request.user}})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(MaintenanceObjectList, self).get_context_data(**kwargs)
        curr_status = self.kwargs['status'] if self.kwargs['status'] else 'open'
        context["status"] = Status.objects.get(slug=curr_status)
        context["app_name"] = app_name
        context["type_document"] = "Заявки"
        context["list_status"] = Status.objects.exclude(slug=curr_status)
        return context

    def get_queryset(self, **kwargs):
        proposals = MaintenanceObject.objects.filter(service_company=self.request.user.profile.current_scompany)
        if self.kwargs['status'] == 'open':
            qs = proposals.filter(status__slug__in=['open', 'complete'], date_schedule__lte=datetime.today())
        elif self.kwargs['status'] == 'scheduled':
            qs = proposals.filter(status__slug__in=['open', 'complete'], date_schedule__gt=datetime.today())
        else:
            qs = proposals.filter(status__slug=self.kwargs['status'], date_schedule__year=datetime.today().year)
        return qs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.service_company = Profile.objects.get(user=self.request.user).current_scompany
        self.object.save()
        return super(MaintenanceObjectList, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, context_key='Form is not valid'))


class MaintenanceObjectUpdate(LoginRequiredMixin, UpdateView):
    model = MaintenanceObject
    template_name = 'maintenance/maintenance_object_upd.html'
    form_class = MaintenanceObjectUpdateManagerForm
    # success_url = reverse_lazy('close_tab')

    def get_form_kwargs(self):
        kwargs = super(MaintenanceObjectUpdate, self).get_form_kwargs()
        kwargs.update({'initial': {'user': self.request.user}})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(MaintenanceObjectUpdate, self).get_context_data(**kwargs)
        proposal = get_object_or_404(MaintenanceObject, pk=self.kwargs['pk'])
        context["app_name"] = app_name
        context["proposal"] = proposal
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, context_key='Form is not valid'))


class MaintenanceObjectDetail(LoginRequiredMixin, DetailView):
    model = MaintenanceObject
    template_name = 'maintenance/maintenance_object_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MaintenanceObjectDetail, self).get_context_data(**kwargs)
        proposal = get_object_or_404(MaintenanceProposalDetail, pk=self.kwargs['pk'])
        context["proposal"] = proposal
        return context


class MaintenanceProposalList(LoginRequiredMixin, ListView, FormView):
    template_name = "maintenance/maintenance_proposal_list.html"
    model = MaintenanceProposal
    form_class = MaintenanceProposalCreateForm
    success_url = reverse_lazy('maintenance:getlist_proposals', args=['open'])
    paginate_by = 5

    def get_form_kwargs(self):
        kwargs = super(MaintenanceProposalList, self).get_form_kwargs()
        kwargs.update({'initial': {'user': self.request.user}})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(MaintenanceProposalList, self).get_context_data(**kwargs)
        curr_status = self.kwargs['status'] if self.kwargs['status'] else 'open'
        context["status"] = Status.objects.get(slug=curr_status)
        context["app_name"] = app_name
        context["type_document"] = "Заявки"
        context["list_status"] = Status.objects.exclude(slug=curr_status)
        return context

    def get_queryset(self, **kwargs):
        proposals = MaintenanceProposal.objects.filter(object__service_company=self.request.user.profile.current_scompany)
        if self.kwargs['status'] == 'open':
            qs = proposals.filter(status__slug__in=['open', 'complete'], date_schedule__lte=datetime.today())
        elif self.kwargs['status'] == 'scheduled':
            qs = proposals.filter(status__slug__in=['open', 'complete'], date_schedule__gt=datetime.today())
        else:
            qs = proposals.filter(status__slug=self.kwargs['status'], date_schedule__year=datetime.today().year)
        return qs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.service_company = Profile.objects.get(user=self.request.user).current_scompany
        self.object.save()
        return super(MaintenanceProposalList, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, context_key='Form is not valid'))


class MaintenanceProposalUpdate(LoginRequiredMixin, UpdateView):
    model = MaintenanceProposal
    template_name = 'maintenance/maintenance_proposal_upd.html'
    form_class = MaintenanceProposalUpdateManagerForm
    # success_url = reverse_lazy('close_tab')

    def get_form_kwargs(self):
        kwargs = super(MaintenanceProposalUpdate, self).get_form_kwargs()
        kwargs.update({'initial': {'user': self.request.user}})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(MaintenanceProposalUpdate, self).get_context_data(**kwargs)
        proposal = get_object_or_404(MaintenanceProposal, pk=self.kwargs['pk'])
        context["app_name"] = app_name
        context["proposal"] = proposal
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, context_key='Form is not valid'))


class MaintenanceProposalDetail(LoginRequiredMixin, DetailView):
    model = MaintenanceProposal
    template_name = 'maintenance/maintenance_proposal_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MaintenanceProposalDetail, self).get_context_data(**kwargs)
        proposal = get_object_or_404(MaintenanceProposalDetail, pk=self.kwargs['pk'])
        context["proposal"] = proposal
        return context
