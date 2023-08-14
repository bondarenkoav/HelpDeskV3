from django.urls import path

from base.views import ClientList, ClientUpdate, RoutList, RoutUpdate, change_service_company

app_name = 'base'

urlpatterns = [
    path('change-service-company/<int:pk>/', change_service_company, name='change-service-company'),

    # Контрагенты
    path('reference_books/clients/<int:pk>/update/', ClientUpdate.as_view(), name='upd-client'),
    path('reference_books/clients/', ClientList.as_view(), name='getlist-clients'),

    # Маршруты
    path('reference_books/routs/<int:pk>/update/', RoutUpdate.as_view(), name='upd-rout'),
    path('reference_books/routs/', RoutList.as_view(), name='getlist-routs'),
]