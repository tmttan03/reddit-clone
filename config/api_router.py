from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from reddit.users.api.views import UserViewSet
from reddit.todos.api.views import TodoViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("todos", TodoViewSet, basename="todo-api")


app_name = "api"
urlpatterns = router.urls
