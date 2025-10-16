from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('start/<int:listing_id>/', views.start, name='start'),
    path('threads/', views.thread_list, name='thread_list'),
    path('t/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('t/<int:thread_id>/send/', views.send_message, name='send_message'),
    path('t/<int:thread_id>/report/<int:message_id>/', views.report_message, name='report_message'),
    path('block/<int:user_id>/', views.block_user, name='block_user'),
    path('t/<int:thread_id>/read/', views.mark_read, name='mark_read'),
]


