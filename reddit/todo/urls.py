from django.urls import path

from .views import TodoListView


app_name = "todos"
urlpatterns = [
    path('', TodoListView.as_view(), name='todo-list'),
]
