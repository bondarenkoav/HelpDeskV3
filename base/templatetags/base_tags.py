from django import template

from base.models import Menu

register = template.Library()


# @register.inclusion_tag('templatetags/sidebar.html')
# def tag_navigation():
#     return {
#         'nodes': Menu.objects.all()
#     }


@register.simple_tag()
def cleaner_string(string):
    import re
    string = string.strip()
    string = re.sub(r"\s+", "", string)
    return string


@register.simple_tag()
def replace_position_type_client(string):
    i = 0
    list_types = ['ИП', 'ООО', 'ЗАО', 'ПАО', 'ОАО', 'ОДО', 'НПАО', 'ПК', 'КФХ', 'ГУП',
                  'ПК', 'ОО', 'ОД', 'АНО', 'СНТ', 'ДНП', 'ТСЖ']
    for opf in list_types:
        i = i + 1
        if string.startswith(opf[i]):
            string = string.replace(opf[i] + ' ', '', 1) + ' ' + opf[i]
    return string