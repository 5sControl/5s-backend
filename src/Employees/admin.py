from django import forms
from django.contrib import admin
from src.Employees.models import CustomUser
from src.erp_5s.models import ReferenceItems


class CustomUserAdminForm(forms.ModelForm):
    workplace = forms.ModelChoiceField(
        queryset=ReferenceItems.objects.filter(reference__name="workplace"), empty_label="Select workplace"
    )

    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserAdminForm
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email', 'role')
    list_filter = ('role',)

    def workplace_name(self, obj):
        return obj.workplace.name if obj.workplace else None
    workplace_name.short_description = 'Workplace'


admin.site.register(CustomUser, CustomUserAdmin)
