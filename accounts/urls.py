from django.urls import path
from django.contrib.auth import views as auth_views
from .views import(
    signup_view,
    UserUpdateView,
)
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name = 'accounts/login.html'), name='login'),
    path('myaccount/', UserUpdateView.as_view(), name='myaccount'),
]
