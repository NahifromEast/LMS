from django.urls import path
from . import views

urlpatterns = [


    # Approve or Reject Course
    path('courses/<str:course_id>/approve/', views.approve_course, name='approve_course'),
    path('courses/<str:course_id>/reject/', views.reject_course, name='reject_course'),

    # Get Instructor Information
    path('instructors/<str:instructor_id>/details/', views.get_instructor_details, name='get_instructor_details'),

    # Assign Course to Instructor
    path('instructors/<str:instructor_id>/assign_course/', views.assign_course, name='assign_course'),

    # Get Reports for Instructor
    path('instructors/<str:instructor_id>/reports/', views.get_instructor_reports, name='get_instructor_reports'),

    # Manage Groups
    path('instructors/groups/create/', views.create_instructor_group, name='create_instructor_group'),
    path('instructors/groups/<str:group_id>/edit/', views.edit_instructor_group, name='edit_instructor_group'),

    # Track Instructor Performance
    path('instructors/<str:instructor_id>/performance/', views.track_instructor_performance, name='track_instructor_performance'),


    path('course/<course_id>/duplicate/', views.duplicate_course, name='duplicate_course'),
    path('course/<course_id>/archive/', views.archive_course, name='archive_course'),
    path('course/<course_id>/assign_instructors/', views.assign_multiple_instructors, name='assign_multiple_instructors'),
    path('course/<course_id>/update_status/', views.update_course_status, name='update_course_status'),
    path('course/<course_id>/report/', views.generate_course_report, name='generate_course_report'),
    path('course/<course_id>/set_prerequisites/', views.set_prerequisites, name='set_prerequisites'),
    path('course/<course_id>/bulk_enroll/', views.bulk_enroll_students, name='bulk_enroll_students'),
    path('course/<course_id>/remove_student/<student_id>/', views.remove_student, name='remove_student'),
    path('student/<student_id>/progress/', views.monitor_student_progress, name='monitor_student_progress'),
    path('course/<course_id>/send_notification/', views.send_notification_to_students, name='send_notification_to_students'),
    path('group/<group_id>/manage/', views.manage_group, name='manage_group'),


    path('course/<str:course_id>/schedule/', views.update_course_schedule, name='update_course_schedule'),
    path('instructor/<str:instructor_id>/performance/', views.get_instructor_performance, name='get_instructor_performance'),

    path('student/<str:student_id>/performance/', views.get_student_performance, name='get_student_performance'),



    path('logs/', views.get_logs, name='get_logs'),   #only the manager shalll be able to do this, making sure privacy is taken into account for instructors and students.

    path('search/', views.search, name='search'),
    path('reports/custom/', views.generate_custom_report, name='generate_custom_report'),


    path('user/deactivate/<str:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('user/transfer/<str:user_id>/', views.transfer_user, name='transfer_user'),
    path('user/update_profile/<str:user_id>/', views.update_profile, name='update_profile'),

    path('students/bulk_add/', views.bulk_upload, name='bulk_add_students'),

]

