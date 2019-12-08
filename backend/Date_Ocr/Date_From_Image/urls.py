from django.urls import path
from django.conf.urls import  include
from .views import *


urlpatterns = [
    path('', PostView.as_view())
]