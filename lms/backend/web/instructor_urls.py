from django.urls import path
from . import views
from web.views import home
from . import instructor_views, student_views

from django.http import HttpResponse




from django.urls import path
from . import instructor_views

urlpatterns = [
    path('create-course/', instructor_views.create_course, name='create_course'),
    path('update-course/<str:course_id>/', instructor_views.update_course, name='update_course'),
    path('list-courses/<str:instructor_id>/', instructor_views.list_courses, name='list_courses'),
    path('create-assignment/<str:course_id>/', instructor_views.create_assignment, name='create_assignment'),
    path('list-assignments/<str:course_id>/', instructor_views.list_assignments, name='list_assignments'),
    path('delete-assignment/<str:assignment_id>/', instructor_views.delete_assignment, name='delete_assignment'),
    path('message-students/<str:course_id>/', instructor_views.message_students, name='message_students'),

    path('assign-homework/<str:course_id>/', instructor_views.assign_homework, name='assign_homework'),
    path('grade_submission/<str:submission_id>/', instructor_views.grade_submission, name='grade_submission'),
    path('view_student_progress/<str:course_id>/', instructor_views.view_student_progress, name='view_student_progress'),
    path('post_announcement/<str:course_id>/', instructor_views.post_announcement, name='post_announcement'),
    path('schedule_meeting/<str:course_id>/', instructor_views.schedule_meeting, name='schedule_meeting'),
    path('mark_attendance/<str:course_id>/', instructor_views.mark_attendance, name='mark_attendance'),
    path('view_attendance/<str:course_id>/', instructor_views.view_attendance, name='view_attendance'),
    path('upload_materials/<str:course_id>/', instructor_views.upload_materials, name='upload_materials'),
    path('generate_attendance_report/<str:course_id>/', views.generate_attendance_report, name='generate_attendance_report'),
    path('search_courses/', instructor_views.search_courses, name='search_courses'),
    path('update_syllabus/<str:course_id>/', instructor_views.update_syllabus, name='update_syllabus'),
    path('view_course_profile/<str:course_id>/', instructor_views.view_course_profile, name='view_course_profile'),



    path('assignments/<str:assignment_id>/view-submissions/', instructor_views.view_submissions, name='view_submissions'),

    # Communication Tools
    path('messages/send/', instructor_views.send_message, name='send_message'),

    # Course Content Management
    path('courses/<str:course_id>/add-module/', instructor_views.add_module, name='add_module'),
    path('modules/<str:module_id>/update-module/', instructor_views.update_module, name='update_module'),

    # Course Management
    path('courses/<str:course_id>/manage-enrollment/', instructor_views.manage_enrollment, name='manage_enrollment'),
]
