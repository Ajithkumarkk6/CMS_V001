from django.contrib import admin
from .models import UserAuthentication, AppBaseConfig, UserCredentialValidation
from django.contrib.admin import SimpleListFilter

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'id')
#     readonly_fields = ('id',)

class MyUserAdmin(UserAdmin):
    # override the default sort column
    ordering = ('-date_joined', )
    # if you want the date they joined or other columns displayed in the list,
    # override list_display too
    list_display = ('username', 'email', 'date_joined', 'first_name', 'last_name', 'is_staff')

# finally replace the default UserAdmin with yours
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

class BooleanDefaultNoFilter(SimpleListFilter):
    def lookups(self, request, model_admin):
        return (
            ('all', 'All'),
            (1, 'Yes'),
            (None, 'No')
        )

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == (str(lookup) if lookup else lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == 'all':
                return queryset
            else:
                return queryset.filter(**{self.parameter_name: self.value()})

        elif self.value() == None:
            return queryset.filter(**{self.parameter_name: False})

# class NamedFilter(BooleanDefaultNoFilter):
#     title = _('InsertName')
#     parameter_name = 'insertname'

class AUserAuthentication(admin.ModelAdmin):
    search_fields = ['user__first_name', 'user__email', 'user__username', 'is_admin']


admin.site.register(UserAuthentication, AUserAuthentication)
admin.site.register(AppBaseConfig)
admin.site.register(UserCredentialValidation)

