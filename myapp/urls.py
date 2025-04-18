from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('donate/', views.donate, name='donate'),
    path('pets/', views.pets, name='pets'),
    path('about/', views.about, name='about'),
    path('what/', views.what, name='what'),
    path('profile/', views.profile, name='profile'),
    path('profile/delete/', views.delete_account, name='delete_account'),
]
