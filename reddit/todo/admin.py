from django.contrib import admin
from reddit.todos.models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'status')