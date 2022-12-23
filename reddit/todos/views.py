from django.views.generic import (
    ListView
)
from .models import Todo


class TodoListView(ListView):

    model = Todo
    paginate_by = 100

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
