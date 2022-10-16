from django.urls import include, path
# from .views import  TodoGetUpdateDelete, TodoListCreate, home
# from .views import  home
from rest_framework import routers

from .views import BlogView, CategoryView, comment_list, like

router = routers.DefaultRouter()

router.register('blog', BlogView)
router.register('categories', CategoryView)



urlpatterns = [
    path("", include(router.urls)),
    path("likes/<int:pk>/", like, name="like"),
    path("comments/<int:pk>/", comment_list, name="comment_list"),
]