from django import forms
from django.core.exceptions import ValidationError

from base.models import Client, RoutesMaintenance
from base.templatetags.base_tags import cleaner_string, replace_position_type_client


class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['type', 'name', 'inn', 'kpp']

    def clean(self):
        cleaned_data = super(ClientCreateForm, self).clean()
        type_client = cleaned_data['type']
        name = replace_position_type_client(cleaner_string(cleaned_data['name']))
        inn = cleaned_data['inn']
        kpp = cleaned_data['kpp']

        if not self.errors:
            duplicate = Client.objects.none()
            noduplicate_flag = True

            if len(name) < 5:
                raise ValidationError("Заполните правильно наименование")

            if type_client == 'company':
                if len(inn) > 0:
                    if len(inn) != 10 and inn.isdigit is False:
                        raise ValidationError("Введите ИНН правильно (10 цифр)")
                    if len(kpp) > 0:
                        if len(kpp) != 9 and inn.isdigit is False:
                            raise ValidationError("Введите КПП правильно (9 цифр)")
                    try:
                        duplicate = Client.objects.get(inn=inn, kpp=kpp)
                        raise ValidationError('Клиент с таким ИНН уже есть в системе')
                    except:
                        noduplicate_flag = False

            elif type_client == 'employer':
                if len(inn) > 0:
                    if len(inn) != 12 and inn.isdigit is False:
                        raise ValidationError("Введите ИНН правильно (12 цифр)")
                    try:
                        duplicate = Client.objects.get(inn=inn)
                        raise ValidationError('Клиент с таким ИНН уже есть в системе')
                    except:
                        noduplicate_flag = False

            else:
                try:
                    duplicate = Client.objects.get(name__icontains=name)
                    raise ValidationError("Клиент с таким ФИО уже есть в системе")
                except:
                    noduplicate_flag = False

            self.duplicate_flag = noduplicate_flag
            self.name = name

        return cleaned_data


class RoutCreateForm(forms.ModelForm):
    class Meta:
        model = RoutesMaintenance
        fields = ['name']