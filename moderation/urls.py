from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    path('report/<str:target_type>/<int:target_id>/', views.report, name='report'),
]


