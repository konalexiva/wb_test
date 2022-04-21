from rest_framework.routers import DefaultRouter

from posts import views

router: DefaultRouter = DefaultRouter()
router.register(r"", views.PostsView, basename="posts")
urlpatterns = router.urls
