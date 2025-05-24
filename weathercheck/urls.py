from django.urls import path
from . import views

app_name = 'weather'
urlpatterns = [
	path('', views.index, name='index'),
	path('show_weather/<str:city_name>/', views.show_weather, name='show_weather'),
	path('api/v1/show_stats/',views.city_stats_api, name='show_stats' )
]
