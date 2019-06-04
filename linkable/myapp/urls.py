from django.urls import path
from myapp import views
from .views import RegistrationAPI
#from rest_framework.authtoken import views

urlpatterns = [
    path('login', views.login),
    path('register', RegistrationAPI.as_view()),
    path('best',views.book_list),
    path('best5',views.book_list5),
    path('book',views.select_book),
    path('user',views.user_info),
    path('search',views.search),
    path('mybook',views.my_book),
    path('rank',views.recommend_book),
    path('category',views.category_list),
    path('category_detail',views.category_book),
    path('category_user', views.category_user),
    path('gauge',views.gauge_cluster),
]