from django.contrib import admin
from .models import Comment, Seen


class CommentModel(admin.ModelAdmin):
    list_display = ('id','text','created','owner',)

class SeenModel(admin.ModelAdmin):
    list_display = ('id','movie','user')


# Register your models here.
admin.site.register(Comment, CommentModel)
admin.site.register(Seen, SeenModel)
