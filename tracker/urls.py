# urls.py
from django.contrib import admin
from django.urls import path
from tracker import views
from .views import track_price_view, price_tracker_list_view
from .views import home_view
app_name = 'tracker'

urlpatterns = [
    path('track/', track_price_view, name='track_price'),
    path('list/', price_tracker_list_view, name='price_tracker_list'),
]
