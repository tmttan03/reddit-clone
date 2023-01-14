from django.urls import path

from .views import (
    TodoListView,
    TranslateView
)

from .api.views import TranslateViewSet


app_name = "todos"
urlpatterns = [
    path('', TodoListView.as_view(), name='todo-list'),
    path('translate/', TranslateView.as_view(), name='translate-view'),
    path('api/translate/', TranslateViewSet.as_view({
        'post': 'translate_sentences',
    }), name="translate_sentences"),
]

