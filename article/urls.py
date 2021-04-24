from rest_framework import routers

from article.views import BulletinViewSet, BlogViewSet, AlbumViewSet

router = routers.DefaultRouter()
router.register('bulletin', BulletinViewSet)
router.register('blog', BlogViewSet)
router.register('album', AlbumViewSet)

urlpatterns = []

urlpatterns += router.urls
