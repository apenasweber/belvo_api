from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users import views

route = routers.DefaultRouter()
route.register('users', views.UserViewSet, basename='users')
route.register('transactions', views.TransactionViewSet, basename='transactions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(route.urls)),
]
