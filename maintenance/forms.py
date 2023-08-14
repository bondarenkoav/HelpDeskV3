from django.utils import timezone
from django import forms
from django.forms import ModelForm

from easy_select2 import Select2Multiple

from maintenance.models import MaintenanceObject, MaintenanceProposal
from helpdesk.widgets import SelectWidget
from base.models import Profile, Status


class MaintenanceObjectCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MaintenanceObjectCreateForm, self).__init__(*args, **kwargs)
        self.user = kwargs['initial'].pop('user', None)

    object_address = forms.CharField(label=u'Адрес объекта',
                                     widget=forms.widgets.TextInput(attrs={'id': 'id_AddressObject',
                                                                           'style': 'padding: 0px'}))

    class Meta:
        model = MaintenanceObject
        fields = ['object_address', 'client_choices', 'rout', 'month_schedule', 'date_start', 'date_end']


class MaintenanceObjectUpdateManagerForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MaintenanceObjectUpdateManagerForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.user = kwargs['initial'].pop('user', None)

    status = forms.ModelChoiceField(required=False, label='Состояние', widget=SelectWidget,
                                    queryset=Status.objects.all())

    class Meta:
        model = MaintenanceObject
        fields = ['client_choices', 'rout', 'month_schedule', 'date_start', 'date_end', 'status']


class MaintenanceProposalCreateForm(ModelForm):

    class Meta:
        model = MaintenanceProposal
        fields = ['date_schedule']


class MaintenanceProposalUpdateManagerForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MaintenanceProposalUpdateManagerForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.user = kwargs['initial'].pop('user', None)

        self.fields['status'].queryset = Status.objects.exclude(slug__in=['scheduled']).order_by('id')
        self.fields['status'].widget.disabled_choices = [1, 3]
        self.fields['coworkers'].queryset = self.profile.executors

    date_schedule = forms.DateField(required=False, label='Выполнить', input_formats=('%Y-%m-%d',),
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),)
    date_work = forms.DateField(required=False, label='Выполнено', input_formats=('%Y-%m-%d',),
                                widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),)
    descript_work = forms.CharField(required=False, label='Описание выполненных работ',
                                    widget=forms.widgets.Textarea(attrs={'rows': 5}))
    status = forms.ModelChoiceField(required=False, label='Состояние', widget=SelectWidget,
                                    queryset=Status.objects.all())
    coworkers = forms.ModelMultipleChoiceField(required=False, label='Исполнители', queryset=Profile.objects.all(),
                                               widget=Select2Multiple())

    class Meta:
        model = MaintenanceProposal
        fields = ['date_schedule', 'descript_work', 'date_work', 'coworkers', 'status']
