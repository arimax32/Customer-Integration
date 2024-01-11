from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.getUsers, name='users'),
    path('user/', views.addUser, name='user'),
    path("user_detail/<int:id>", views.userDetail, name="userInfo"),
    path("delete_user/<int:id>", views.deleteUser, name="delteUser")
]
