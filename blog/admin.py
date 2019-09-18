from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.
from .models import Post, Comment, Subscription

admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Comment, MarkdownxModelAdmin)
admin.site.register(Subscription)
