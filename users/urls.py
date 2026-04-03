from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("register/", views.register, name="register"),
    path("register/code/", views.verificar_codigo, name="verificar_codigo"),
    path("logout/", views.deslogar_usuario, name='logout'),
    path("reset/", PasswordResetView.as_view( template_name="users/reset.html",success_url=reverse_lazy('users:reset_done'),email_template_name="users/password_reset_email.html" ), name="reset"),
    path("reset/done/", PasswordResetDoneView.as_view(template_name="users/reset_done.html"), name="reset_done"),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(template_name="users/change_password.html",success_url=reverse_lazy('users:change_confirm_password')), name="change_password"),
    path("reset/complete/", PasswordResetCompleteView.as_view(template_name="users/change_confirm_password.html"), name="change_confirm_password"),
]