from django.urls import path
from . import views
from django.contrib import admin
from web.views import home
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("Welcome to MASESI!")


urlpatterns = [
    path('', views.home, name='home'),
    path('get_courses/', views.get_courses, name='get_courses'),
    path('add_course/', views.add_course, name='add_course'),
    path('get_schools/', views.get_schools, name='get_schools'),
    path('school/update/<str:school_id>/', views.update_school, name='update_school'),
    path('school/<school_id>/delete/', views.delete_school, name='delete_school'),
    path('school/create/', views.create_school, name='create_school'),
    path('school/<school_id>/assign_manager/', views.assign_manager, name='assign_manager'),
    path('language/create/', views.create_language, name='create_language'),
    path('language/', views.get_languages, name='get_languages'),
    path('reports/summary/', views.get_reports_summary, name='get_reports_summary'),


    #user functionality
    path('user/view/<str:user_id>/', views.view_user, name='view_user'),
    path('user/create/', views.create_user, name='create_user'),
    path('user/update/<user_id>/', views.update_user, name='update_user'),
    path('user/delete/<user_id>/', views.delete_user, name='delete_user'),
    path('user/list/', views.list_users, name='list_users'),
    path('users/pending/', views.get_pending_users, name='get_pending_users'),
    path('users/<user_id>/approve/', views.approve_user, name='approve_user'),
    path('users/<user_id>/reject/', views.reject_user, name='reject_user'),
    path('user/<str:user_id>/change_role/', views.change_user_role, name='change_user_role'),
    path('user/<str:user_id>/activate/', views.activate_user, name='activate_user'),
    path('user/<str:user_id>/deactivate/', views.deactivate_user, name='deactivate_user'),
    path('user/list_paginated/', views.list_users_paginated, name='list_users_paginated'),

    #authentications
    
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login_view'),  # Correct path
    path('auth/logout/', views.logout_user, name='logout_user'),
    path('auth/register/', views.register_user, name='register_user'),
    path('auth/forgot_password/', views.forgot_password, name='forgot_password'),
    path('user/reset_password/<str:user_id>/', views.reset_user_password, name='reset_user_password'),



    path('language/add/', views.add_language, name='add_language'),
    path('language/list/', views.list_languages, name='list_languages'),



    # New paths
    path('school/<school_id>/', views.get_school_details, name='get_school_details'),
    path('school/search/', views.search_schools, name='search_schools'),
    path('course/update/<str:course_id>/', views.update_course, name='update_course'),
    path('course/delete/<str:course_id>/', views.delete_course, name='delete_course'),
    

    # Assign Teacher to Course
    path('school/<str:school_id>/course/<str:course_id>/assign_teacher/', views.assign_teacher, name='assign_teacher'),
    
    # Manage Students
    path('school/<str:school_id>/student/enroll/', views.enroll_student, name='enroll_student'),
    path('school/<str:school_id>/student/<str:student_id>/update/', views.update_student, name='update_student'),
    path('school/<str:school_id>/student/<str:student_id>/remove/', views.remove_student, name='remove_student'),
    
    # View School Reports
    path('school/<str:school_id>/reports/', views.view_school_reports, name='view_school_reports'),
    
    # Manage Courses
    path('school/<str:school_id>/course/<str:course_id>/approve/', views.approve_course, name='approve_course'),
    path('school/<str:school_id>/course/<str:course_id>/reject/', views.reject_course, name='reject_course'),
    
    # Add Announcements
    path('school/<str:school_id>/announcements/', views.create_announcement, name='create_announcement'),
    
    # List Teachers and Students
    path('school/<str:school_id>/teachers/', views.list_teachers, name='list_teachers'),
    path('school/<str:school_id>/students/', views.list_students, name='list_students'),

    path('students/<student_id>/view/', views.view_student, name='view_student'),
    path('course/<course_id>/students/', views.view_students_in_course, name='view_students_in_course'),
    path('course/<course_id>/assignments/', views.view_assignments_for_course, name='view_assignments_for_course'),
    path('course/<course_id>/reports/', views.view_course_reports, name='view_course_reports'),
    path('course/<course_id>/activity/', views.track_student_activity, name='track_student_activity'),
    path('student-group/create/', views.create_student_group, name='create_student_group'),


    path('logs/', views.get_logs, name='get_logs'),
    path('search/', views.search, name='search'),

    path('auth/generate_mfa/', views.generate_mfa_code, name='generate_mfa_code'),
    path('auth/validate_mfa/', views.validate_mfa_code, name='validate_mfa_code'),
    
    path('manager/course/<str:course_id>/assignment/<str:assignment_id>/remove/', views.remove_assignment, name='remove_assignment'),

    
    
]


