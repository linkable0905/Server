from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser
from .models import Book,Recommend,Cluster,MyCategory

admin.site.register(Book)
admin.site.register(MyUser)
admin.site.register(Recommend)
admin.site.register(Cluster)
admin.site.register(MyCategory)