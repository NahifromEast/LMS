from django.urls import path
from . import views
from web.views import home

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
    path('auth/login/', views.login_user, name='login_user'),
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
    

    
]