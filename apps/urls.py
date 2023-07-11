from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bulb/<int:bulb_id>/update/', views.update_pin, name='update_pin'),
]
