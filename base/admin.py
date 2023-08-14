from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.template.defaultfilters import yesno
from mptt.admin import MPTTModelAdmin

from base.models import *

# Register your models here.


class ProfileAdmin(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = u'Профиль'
    verbose_name_plural = u'Профиль'
    fk_name = 'user'
    list_display = ('user', 'get_fullname', 'post', 'scompany_current', 'birthday', 'phone', 'executor', 'get_active')
    readonly_fields = ('user', 'get_fullname', 'get_active',)
    list_editable = ('executor',)
    list_filter = ('post', 'scompany',)
    ordering = ('user', )
    fieldsets = (
        ('Данные пользователя (не изменяемые данные)', {
            'fields': ('user', 'get_active',)
        }),
        ('Дополнительные данные (изменяемые данные)', {
            'fields': ('gender', 'post', 'birthday', 'phone', 'location',),
        }),
        ('Сервисная компания (изменяемые данные)', {
            'fields': ('scompany', 'scompany_default', 'scompany_current', 'executor',),
        }),
        (None, {
            'fields': ('personal_data',),
        }),
    )

    def get_fullname(self, obj):
        return obj.user.last_name + ' ' + obj.user.first_name
    get_fullname.short_description = "Полное имя"

    def get_active(self, obj):
        return yesno(obj.user.is_active)
    get_active.short_description = "Активен"


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileAdmin, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'inn', 'kpp')
    list_filter = ('type',)
    search_fields = ('name', 'inn',)


@admin.register(ServiceCompany)
class ServiceCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'tr_color')


@admin.register(RoutesMaintenance)
class RoutesMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'serving_company')


@admin.register(StatusTask)
class RoutesMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'tr_color', 'view_list')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'template')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(City)
admin.site.register(Menu, MPTTModelAdmin)
admin.site.register(Post)
admin.site.register(TypeRequest)
admin.site.register(TypeDocument)
admin.site.register(TypeBuild)
admin.site.register(TypeSecurity)
admin.site.register(MonthList)
admin.site.register(ModelTransmitter)
