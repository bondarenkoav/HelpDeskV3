from datetime import datetime

from django import template

from base.models import Profile, Menu
from exploitation.models import ExploitationProposal

register = template.Library()


@register.inclusion_tag('templatetags/dashboard_upcoming_birthdays.html')
def informer_birthdayboy():
    return {
        'profiles': Profile.objects.filter(birthday__gte=datetime.today()).values('user', 'birthday').order_by('birthday')[:5],
        'curr_date': datetime.today()
    }


@register.inclusion_tag('templatetags/dashboard_card_exploitation.html')
def informer_exploitation(user):
    proposals_iscomplete = 0
    proposals = ExploitationProposal.objects.filter(
        service_company=user.profile.current_scompany, date_schedule=datetime.today())
    proposals_isshedule_today = proposals.count()
    if proposals_isshedule_today > 0:
        proposals_iscomplete = proposals.filter(status__slug__in=['complete', 'close']).count()
    return {'proposals_iscomplete': proposals_iscomplete,
            'percent_iscomplete': (proposals_iscomplete/100)*proposals_isshedule_today}


@register.inclusion_tag('templatetags/dashboard_card_build.html')
def informer_build(user):
    proposals_open_count = ExploitationProposal.objects.filter(
        status__slug='open', service_company__in=user.profile.current_scompany).count()
    return {'proposals_open': proposals_open_count}


@register.inclusion_tag('templatetags/dashboard_card_maintenance.html')
def informer_maintenance(user):
    proposals_open_count = ExploitationProposal.objects.filter(
        status__slug='open', service_company__in=user.profile.current_scompany).count()
    return {'proposals_open': proposals_open_count}


@register.inclusion_tag('templatetags/rb_navigation.html')
def rb_menu():
    qs = Menu.objects.filter(slug="reference_books")
    nodes = qs.get_descendants(include_self=False)
    return {
        'nodes': nodes
    }