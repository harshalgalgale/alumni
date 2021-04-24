from django.contrib import admin

# Register your models here.
from core.models import MainSector, SubSector, Skills


@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    model = Skills

admin.site.register(MainSector)
admin.site.register(SubSector)
