from django.contrib import admin

# Register your models here.

from .models import Tag,Article,Comment,MyUser


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class ArticleAdmin(admin.ModelAdmin):

    inlines = [CommentInline]


admin.site.register(Tag)

admin.site.register(Article,ArticleAdmin)

admin.site.register(Comment)



