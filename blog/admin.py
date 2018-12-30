from django.contrib import admin
from blog.models import BlogComment, BlogPost, BlogReply


admin.site.register(BlogReply)

admin.site.register(BlogPost)

admin.site.register(BlogComment)
