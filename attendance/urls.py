from django.urls import path
from .views import *

app_name = "attendance"

urlpatterns = [
    path("", dashboard, name="dashboard"),
]
