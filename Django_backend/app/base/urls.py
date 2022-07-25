from django.urls import include, path, re_path
from . import views
from .views import *



urlpatterns = [
path("register", Register.as_view()),
path("get_authorization", UserAPIView.as_view()),
path('login', LoginAPIView.as_view()),
path("refresh", RefreshAPIView.as_view()),
path("send_diagnostics", DiagnosticAPIView.as_view()),
re_path(r"^user_registration", views.user_registration),
]