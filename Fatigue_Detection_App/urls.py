from django.urls import path, include , re_path
from . import views, admin_views
#from users.views import ResetPasswordView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('index/', views.index, name='index'),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('logout_user/', views.logout_user, name="logout_user"),

    #=================admin views============================#
    path('admin_home/', admin_views.Admin_home.as_view(), name='admin_home'),
    path('admin_view_worker/<worker_uuid>/', admin_views.View_worker.as_view(), name='admin_view_worker'),
]