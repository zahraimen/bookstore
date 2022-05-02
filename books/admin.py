from django.contrib import admin

# Register your models here.
from .models import Book, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'text', 'datetime_created','is_active','recommend',)


admin.site.register(Book)
# admin.site.register(Comment, CommentAdmin)
