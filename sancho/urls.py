# django import
from django.urls import path

# Project import
from . import views

# Needed for the include in the settings
app_name = 'sancho'

urlpatterns = [
    path("", views.index, name="index"),
    # Vista de los BT
    path('backtest/list.html', views.bt_list, name='backtest_list'),
    path('backtest/detail.html?<int:bt_id>/', views.bt_detail, name='backtest_detail')
]