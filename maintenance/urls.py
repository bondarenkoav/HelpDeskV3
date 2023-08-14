__author__ = 'ipman'

from django.urls import path

from maintenance.views import *

app_name = 'maintenance'

urlpatterns = [
    # Просмотреть объект
    path('objects/<int:pk>/detail/', MaintenanceObjectDetail.as_view(), name='view-object'),
    # Просмотреть заявку
    path('item/<int:pk>/detail/', MaintenanceProposalDetail.as_view(), name='view-proposal'),
    # Обновить заявку
    path('item/<int:pk>/update/', MaintenanceProposalUpdate.as_view(), name='upd-manage-proposal'),
    # Вывести список заявок
    path('objects/<slug:status>/', MaintenanceObjectList.as_view(), name='getlist-objects'),
    path('proposal/<slug:status>/', MaintenanceProposalList.as_view(), name='getlist-proposals'),
]