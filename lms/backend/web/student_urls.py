from django.urls import path
from . import views
from web.views import home
from . import instructor_views, student_views

from django.http import HttpResponse




urlpatterns = [
    path('get_enrolled_courses/<str:student_id>/', student_views.get_enrolled_courses, name='get_enrolled_courses'),
    path('search_available_courses/', student_views.search_available_courses, name='search_available_courses'),
    path('submit_homework/<str:assignment_id>/', student_views.submit_homework, name='submit_homework'),
    path('submit_quiz_answers/<str:quiz_id>/', student_views.submit_quiz_answers, name='submit_quiz_answers'),
    path('get_completion_status/<str:student_id>/<str:course_id>/', student_views.get_completion_status, name='get_completion_status'),
    path('join_group_project/<str:group_id>/', student_views.join_group_project, name='join_group_project'),
    path('get_group_members/<str:group_id>/', student_views.get_group_members, name='get_group_members'),
    path('get_announcements/<str:course_id>/', student_views.get_announcements, name='get_announcements'),
    path('discussions/post/<str:course_id>/', student_views.post_discussion, name='post_discussion'),
    path('discussions/reply/<str:discussion_id>/', student_views.reply_to_discussion, name='reply_to_discussion'),
    path('discussions/view/<str:course_id>/', student_views.get_discussion_threads, name='get_discussion_threads'),
    path('private-notes/add/<str:student_id>/', student_views.add_private_note, name='add_private_note'),
    path('private-notes/view/<str:student_id>/', student_views.get_private_notes, name='get_private_notes'),
    path('materials/download/<str:material_id>/', student_views.download_course_material, name='download_course_material'),
    path('feedback/submit/<str:course_id>/', student_views.submit_course_feedback, name='submit_course_feedback'),
    path('feedback/view/<str:course_id>/', student_views.get_course_feedback, name='get_course_feedback'),

    # Q&A Sessions
    path('qa/schedule/<str:course_id>/', student_views.schedule_qa_session, name='schedule_qa_session'),
    path('qa/view/<str:course_id>/', student_views.view_qa_sessions, name='view_qa_sessions'),
    path('qa/join/<str:qa_session_id>/', student_views.join_qa_session, name='join_qa_session'),

    # Bookmark Lessons
    path('bookmark/<str:student_id>/<str:course_id>/', student_views.bookmark_content, name='bookmark_content'),
    path('bookmarks/view/<str:student_id>/<str:course_id>/', student_views.view_bookmarks, name='view_bookmarks'),
    path('bookmark/remove/<str:student_id>/<str:bookmark_id>/', student_views.remove_bookmark, name='remove_bookmark'),

]