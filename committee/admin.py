from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from committee.models import CommitteeMember


@admin.register(CommitteeMember)
class CommitteeMemberAdmin(ImportExportModelAdmin):
    list_display = ['position', 'member']
    list_filter = (
        'position',
    )
    search_fields = (
        'position',
        'member__user__first_name',
        'member__user__last_name',
    )
    raw_id_fields = ('member',)
    save_as = True

