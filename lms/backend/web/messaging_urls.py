from django.urls import path
from . import views
from web.views import home
from . import instructor_views, student_views

from django.http import HttpResponse





urlpatterns = [
    path("send_message/", views.send_message, name="send_message"),
    path("get_messages/<str:user_id>/", views.get_messages, name="get_messages"),
    path("mark_message_read/<str:message_id>/", views.mark_message_read, name="mark_message_read"),
    path("delete_message/<str:message_id>/", views.delete_message, name="delete_message"),
    path("send_group_message/", views.send_group_message, name="send_group_message"),
    path("reply_message/<str:thread_id>/", views.reply_message, name="reply_message"),
    path("filter_messages/<str:user_id>/", views.filter_messages, name="filter_messages"),
    path("unread_count/<str:user_id>/", views.get_unread_count, name="unread_count"),
]