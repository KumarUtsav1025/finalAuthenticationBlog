from django.contrib import admin
from roboproject.models import Post, Comment, PostImage

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostImage)