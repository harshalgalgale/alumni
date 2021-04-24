from django.urls import path, include

app_name = "api"
# urlpatterns = router.urls
urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    # path(settings.ADMIN_URL, admin.site.urls),
    # # Django Pages
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # # User management
    # # path("users/", include("apps.core.urls", namespace="users")),
    # path("accounts/", include("allauth.urls")),
    # Django API
    # path('', include('accounts.urls')),
    path('', include('students.urls')),
    path('', include('members.urls')),
    path('', include('core.urls')),
    path('', include('committee.urls')),
    path('', include('article.urls')),
]
