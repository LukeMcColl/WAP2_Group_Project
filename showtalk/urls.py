from django.urls import path
from showtalk import views

app_name = 'showtalk'

urlpatterns = [
    path('', views.homepage, name='homepage'),
]