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

    path('courses/<str:course_id>/view-gradebook/', instructor_views.view_gradebook, name='view_gradebook'),
    path('submissions/<str:submission_id>/auto-grade-quiz/', instructor_views.auto_grade_quiz, name='auto_grade_quiz'),
    path('courses/<str:course_id>/export-grades-csv/', instructor_views.export_grades_to_csv, name='export_grades_to_csv'),
    path('submissions/<str:submission_id>/track-grade-history/', instructor_views.track_grade_history, name='track_grade_history'),
    path('submissions/<str:submission_id>/update-grade-history/', instructor_views.update_grade_with_history, name='update_grade_with_history'),






    #Exam and quizes

    path('courses/<str:course_id>/create-quiz-exam/', instructor_views.create_quiz_exam, name='create_quiz_exam'),
    path('courses/<str:course_id>/create-question-pool/', instructor_views.create_question_pool, name='create_question_pool'),
    path('question-pools/<str:pool_id>/get-random-questions/', instructor_views.get_random_questions, name='get_random_questions'),
    path('submissions/<str:submission_id>/submit-timed-exam/', instructor_views.submit_timed_exam, name='submit_timed_exam'),
    path('submissions/<str:submission_id>/ai-proctor-exam/', instructor_views.ai_proctor_exam, name='ai_proctor_exam'),
    path('quizzes/<str:quiz_id>/set-retake-rules/', instructor_views.set_retake_rules, name='set_retake_rules'),
    path('submissions/<str:submission_id>/request-retake/', instructor_views.request_retake, name='request_retake'),

    path('courses/<str:course_id>/create-assignment/', instructor_views.create_assignment, name='create_assignment'),
    path('courses/<str:course_id>/create-discussion-thread/', instructor_views.create_discussion_thread, name='create_discussion_thread'),
    path('discussion-threads/<str:thread_id>/post-comment/', instructor_views.post_comment, name='post_comment'),
    path('discussion-threads/<str:thread_id>/view/', instructor_views.view_discussion_thread, name='view_discussion_thread'),
    path('courses/<str:course_id>/create-survey/', instructor_views.create_survey, name='create_survey'),
    path('surveys/<str:survey_id>/submit-response/', instructor_views.submit_survey_response, name='submit_survey_response'),
    path('surveys/<str:survey_id>/results/', instructor_views.view_survey_results, name='view_survey_results'),
    path('courses/<str:course_id>/create-peer-review-assignment/', instructor_views.create_peer_review_assignment, name='create_peer_review_assignment'),
    path('peer-reviews/<str:review_id>/submit/', instructor_views.submit_peer_review, name='submit_peer_review'),


    path('courses/<str:course_id>/import_export_content/', instructor_views.import_export_course_content, name='import_export_content'),
    path('courses/<str:course_id>/modules/<str:module_id>/duplicate/', instructor_views.duplicate_module, name='duplicate_module'),
    path('courses/<str:course_id>/modules/<str:module_id>/schedule/', instructor_views.schedule_content, name='schedule_content'),
    path('courses/<str:course_id>/modules/<str:module_id>/add_resource/', instructor_views.add_external_resource, name='add_external_resource'),
    path('courses/templates/', instructor_views.create_course_template, name='create_course_template'),
    path('courses/templates/apply/', instructor_views.apply_course_template, name='apply_course_template'),
    path('courses/<str:course_id>/archive/', instructor_views.archive_course_content, name='archive_course_content'),
    path('courses/<str:course_id>/restore/', instructor_views.restore_course_content, name='restore_course_content'),
    path('courses/<str:course_id>/versions/', instructor_views.course_version_control, name='course_version_control'),
    path('courses/<str:course_id>/batch_upload_materials/', instructor_views.batch_upload_materials, name='batch_upload_materials'),
    path('courses/<str:course_id>/reorder_modules/', instructor_views.reorder_modules, name='reorder_modules'),




    path('courses/<str:course_id>/review-content/', instructor_views.review_content, name='review_content'),

    # Draft vs. Published States for Modules and Materials
    path('courses/<str:course_id>/publish-module/', instructor_views.publish_module, name='publish_module'),
    path('courses/<str:course_id>/publish-material/', instructor_views.publish_material, name='publish_material'),

    # Permissions and Collaboration Tools
    path('courses/<str:course_id>/add-collaborator/', instructor_views.add_collaborator, name='add_collaborator'),

    # Global Search for Course Content
    path('search-course-content/', instructor_views.search_course_content, name='search_course_content'),

    # Interactive Content (Quizzes Embedded in Content)
    path('courses/<str:course_id>/add-interactive-section/', instructor_views.add_interactive_section, name='add_interactive_section'),

    # Track Student Engagement for Each Module or Content Section
    path('courses/<str:course_id>/track-engagement/', instructor_views.track_engagement, name='track_engagement'),

    # Course Announcements and Updates History
    path('courses/<str:course_id>/updates-history/', instructor_views.updates_history, name='updates_history'),

    # Adaptive Release for Content Based on Performance or Time
    path('courses/<str:course_id>/set-adaptive-release/', instructor_views.set_adaptive_release, name='set_adaptive_release'),

    # Archive/Unarchive Modules (Not Just the Whole Course)
    path('courses/<str:course_id>/archive-module/', instructor_views.archive_module, name='archive_module'),

    # External Tools Integration and API Configuration
    path('courses/<str:course_id>/add-external-tool/', instructor_views.add_external_tool, name='add_external_tool'),

    # Resource Download Management
    path('courses/<str:course_id>/set-download-permission/', instructor_views.set_download_permission, name='set_download_permission'),

    # Set Course Permissions
    path('courses/<str:course_id>/set-permissions/', instructor_views.set_course_permissions, name='set_course_permissions'),

    # Certificate Issuance
    path('courses/<str:course_id>/issue-certificate/', instructor_views.issue_certificate, name='issue_certificate'),

    # Completion Progress Reports
    path('courses/<str:course_id>/generate-completion-report/', instructor_views.generate_completion_report, name='generate_completion_report'),
    path('clone_course/<str:course_id>/', instructor_views.clone_course, name='clone_course'),
    path('download_all_materials/<str:course_id>/', instructor_views.download_all_materials, name='download_all_materials'),
    path('save_versioned_content/<str:course_id>/', instructor_views.save_versioned_content, name='save_versioned_content'),
    path('add_private_note/<str:course_id>/', instructor_views.add_private_note, name='add_private_note'),
    path('get_private_notes/<str:course_id>/', instructor_views.get_private_notes, name='get_private_notes'),

]
