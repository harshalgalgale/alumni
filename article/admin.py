from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from article.models import Blog, Bulletin, Album, AlbumImage


class AlbumImageInlineAdmin(admin.TabularInline):
    model = AlbumImage
    # extra = 0

    def get_queryset(self, request):
        """
        Fetches related models to avoid extra queries
        """
        return super(
            AlbumImageInlineAdmin, self
        ).get_queryset(
            request
        ).select_related('album')


@admin.register(Bulletin)
class BulletinAdmin(ImportExportModelAdmin):
    list_display = ['title', 'author', 'pub_date', 'view_count', 'clap_count']
    search_fields = (
        'title',
        'author',
    )
    save_as = True


@admin.register(Blog)
class BlogAdmin(ImportExportModelAdmin):
    list_display = ['title', 'author', 'pub_date', 'view_count', 'clap_count']
    search_fields = (
        'title',
        'author',
    )
    save_as = True


@admin.register(Album)
class AlbumAdmin(ImportExportModelAdmin):
    inlines = (
        AlbumImageInlineAdmin,
    )
    list_display = ['title', 'author', 'pub_date', 'view_count', 'clap_count']
    search_fields = (
        'title',
        'author',
    )
    save_as = True
