from django.urls import path
from .views import OrderApiViews

urlpatterns = [
    path('order/', OrderApiViews.as_view())
]