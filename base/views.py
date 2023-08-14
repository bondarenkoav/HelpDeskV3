import logging
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, FormView, UpdateView

from base.models import Profile, ServiceCompany, Menu
from base.forms import *
from helpdesk import settings

app_name = 'Базовое приложение'

logger = logging.getLogger(__name__)
rb_nodes = Menu.objects.get(slug='reference_books')


class CustomLoginPage(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_name'] = settings.ProjectName
        return context

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.get_user()
        profile = Profile.objects.get(user=user)
        if profile.user.is_active:
            auth_login(self.request, form.get_user())
        # get_url = self.get_success_url()
        return HttpResponseRedirect(self.success_url)


@login_required()
def dashboard(request):
    context = {'title': 'Панель управления'}
    return render(request, 'dashboard/dashboard.html', context)


def change_service_company(request, pk):
    try:
        Profile.objects.filter(pk=request.user.profile.pk).update(scompany_current=ServiceCompany.objects.get(pk=pk))
    except:
        logger.error(u'Ошибка смены сервисной компании')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Получаем список активных пользователей
def get_activeusers():
    # 15 минут - время на активные действия в программе
    session_start = datetime.now() - timedelta(minutes=15)
    uid_list = []
    try:
        sessions = Session.objects.filter(expire_date__gte=session_start)
        for session in sessions:
            data = session.get_decoded()
            uid_list.append(data.get('_auth_user_id', None))
    except:
        pass
    return Profile.objects.filter(user__id__in=uid_list)


# class SearchResultsView(ListView):
#     model = City
#     template_name = 'search_results.html'
#
#     def get_queryset(self):  # новый
#         query = self.request.GET.get('q')
#         object_list = City.objects.filter(
#             Q(name__icontains=query) | Q(state__icontains=query)
#         )
#         return object_list


class ClientList(LoginRequiredMixin, ListView, FormView):
    template_name = "base/client_list.html"
    form_class = ClientCreateForm
    success_url = reverse_lazy('base:getlist-clients')

    def get_context_data(self, **kwargs):
        context = super(ClientList, self).get_context_data(**kwargs)
        context["app_name"] = app_name
        context["nodes"] = rb_nodes
        return context

    def get_queryset(self):
        qs = Client.objects.all().order_by('name')
        return qs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(ClientList, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, context_key='Введенные данные не верны'))


class ClientUpdate(LoginRequiredMixin, UpdateView):
    model = Client
    template_name = 'base/client_upd.html'
    form_class = ClientCreateForm

    # success_url = reverse_lazy('close_tab')

    def get_form_kwargs(self):
        kwargs = super(ClientUpdate, self).get_form_kwargs()
        kwargs.update({'initial': {'user': self.request.user}})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ClientUpdate, self).get_context_data(**kwargs)
        proposal = get_object_or_404(self.model, pk=self.kwargs['pk'])
        context["app_name"] = app_name
        context["proposal"] = proposal
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, context_key='Form is not valid'))


class RoutList(LoginRequiredMixin, ListView, FormView):
    model = RoutesMaintenance
    template_name = "base/rout_list.html"
    success_url = reverse_lazy('base:getlist-routs')
    form_class = RoutCreateForm

    def get_context_data(self, **kwargs):
        context = super(RoutList, self).get_context_data(**kwargs)
        context["app_name"] = app_name
        context["nodes"] = rb_nodes
        return context

    def get_queryset(self):
        qs = RoutesMaintenance.objects.all()
        return qs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(RoutList, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, context_key='Введенные данные не верны'))


class RoutUpdate(LoginRequiredMixin, UpdateView):
    model = Client
    template_name = 'base/rout_upd.html'
    fields = ['name']

    def get_form_kwargs(self):
        kwargs = super(RoutUpdate, self).get_form_kwargs()
        kwargs.update({'initial': {'user': self.request.user}})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(RoutUpdate, self).get_context_data(**kwargs)
        rout = get_object_or_404(RoutesMaintenance, pk=self.kwargs['pk'])
        context["app_name"] = app_name
        context["rout"] = rout
        return context
