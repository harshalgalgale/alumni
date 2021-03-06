from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from members.models import PersonalProfile, WorkProfile, SocialProfile, PermanentAddress


class PermanentAddressInlineAdmin(admin.TabularInline):
    model = PermanentAddress
    extra = 0

    def get_queryset(self, request):
        """
        Fetches related models to avoid extra queries
        """
        return super(
            PermanentAddressInlineAdmin, self
        ).get_queryset(
            request
        ).select_related('personal_profile')


class WorkProfileInlineAdmin(admin.TabularInline):
    model = WorkProfile
    extra = 0

    def get_queryset(self, request):
        """
        Fetches related models to avoid extra queries
        """
        return super(
            WorkProfileInlineAdmin, self
        ).get_queryset(
            request
        ).select_related('personal_profile')


class SocialProfileInlineAdmin(admin.TabularInline):
    model = SocialProfile
    extra = 0

    def get_queryset(self, request):
        """
        Fetches related models to avoid extra queries
        """
        return super(
            SocialProfileInlineAdmin, self
        ).get_queryset(
            request
        ).select_related('personal_profile')


@admin.register(PersonalProfile)
class PersonalProfileAdmin(ImportExportModelAdmin):
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'student', ('first_name', 'middle_name', 'last_name'), ('gender', 'birth_date', 'avatar'),)
        }),
        ('Contact Information', {
            'fields': (('phone', ),),
        }),
        ('About', {
            'fields': ('bio', ),
        }),
    )
    inlines = (
        PermanentAddressInlineAdmin,
        WorkProfileInlineAdmin,
        SocialProfileInlineAdmin,
    )
    list_display = ['first_name', 'last_name', 'user', 'gender', 'birth_date', 'phone']
    list_filter = (
        'gender',
    )
    search_fields = (
        'first_name',
        'last_name',
        'user__email',
        'mobile',
    )
    raw_id_fields = ['user', 'student']
    save_as = True
