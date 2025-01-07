from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId
import json
import datetime
import csv
import random
from backend.settings import mongo_db



@csrf_exempt
def create_course(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_course = {
                "name": data.get("name"),
                "description": data.get("description"),
                "school_id": data.get("school_id"),
                "instructor_id": data.get("instructor_id"),
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now()
            }
            result = mongo_db.courses.insert_one(new_course)
            return JsonResponse({"message": "Course created successfully", "course_id": str(result.inserted_id)}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def update_course(request, course_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            mongo_db.courses.update_one(
                {"_id": ObjectId(course_id)},
                {"$set": {
                    "name": data.get("name"),
                    "description": data.get("description"),
                    "updated_at": datetime.datetime.now()
                }}
            )
            return JsonResponse({"message": "Course updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


def list_courses(request, instructor_id):
    if request.method == 'GET':
        courses = list(mongo_db.courses.find({"instructor_id": instructor_id}, {"_id": 0}))
        return JsonResponse({"courses": courses}, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def create_assignment(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_assignment = {
                "course_id": course_id,
                "title": data.get("title"),
                "description": data.get("description"),
                "due_date": data.get("due_date"),
                "created_at": datetime.datetime.now()
            }
            result = mongo_db.assignments.insert_one(new_assignment)
            return JsonResponse({"message": "Assignment created successfully", "assignment_id": str(result.inserted_id)}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


def list_assignments(request, course_id):
    if request.method == 'GET':
        assignments = list(mongo_db.assignments.find({"course_id": course_id}, {"_id": 0}))
        return JsonResponse({"assignments": assignments}, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def delete_assignment(request, assignment_id):
    if request.method == 'DELETE':
        mongo_db.assignments.delete_one({"_id": ObjectId(assignment_id)})
        return JsonResponse({"message": "Assignment deleted successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def message_students(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = {
                "course_id": course_id,
                "sender_id": data.get("sender_id"),
                "message": data.get("message"),
                "timestamp": datetime.datetime.now()
            }
            mongo_db.messages.insert_one(message)
            return JsonResponse({"message": "Message sent successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def assign_homework(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_homework = {
                "title": data.get("title"),
                "description": data.get("description"),
                "due_date": data.get("due_date"),
                "course_id": ObjectId(course_id),
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now()
            }
            result = mongo_db.homework.insert_one(new_homework)
            return JsonResponse({"message": "Homework assigned successfully", "homework_id": str(result.inserted_id)}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def grade_submission(request, submission_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            grade = data.get("grade")
            feedback = data.get("feedback")
            mongo_db.submissions.update_one(
                {"_id": ObjectId(submission_id)},
                {"$set": {
                    "grade": grade,
                    "feedback": feedback,
                    "graded_at": datetime.datetime.now()
                }}
            )
            return JsonResponse({"message": "Submission graded successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def view_student_progress(request, course_id):
    if request.method == 'GET':
        try:
            students = list(mongo_db.students.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
            return JsonResponse({"students_progress": students}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def post_announcement(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_announcement = {
                "title": data.get("title"),
                "message": data.get("message"),
                "course_id": ObjectId(course_id),
                "created_at": datetime.datetime.now()
            }
            mongo_db.announcements.insert_one(new_announcement)
            return JsonResponse({"message": "Announcement posted successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def schedule_meeting(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_meeting = {
                "title": data.get("title"),
                "date": data.get("date"),
                "time": data.get("time"),
                "course_id": ObjectId(course_id),
                "instructor_id": data.get("instructor_id"),
                "link": data.get("link"),  # for online meetings
                "created_at": datetime.datetime.now()
            }
            mongo_db.meetings.insert_one(new_meeting)
            return JsonResponse({"message": "Meeting scheduled successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def mark_attendance(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attendance_record = {
                "student_id": data.get("student_id"),
                "course_id": ObjectId(course_id),
                "status": data.get("status"),  # Present/Absent
                "date": datetime.datetime.now()
            }
            mongo_db.attendance.insert_one(attendance_record)
            return JsonResponse({"message": "Attendance recorded successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def view_attendance(request, course_id):
    if request.method == 'GET':
        try:
            attendance = list(mongo_db.attendance.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
            return JsonResponse({"attendance_records": attendance}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def upload_materials(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_material = {
                "title": data.get("title"),
                "file_url": data.get("file_url"),
                "course_id": ObjectId(course_id),
                "uploaded_at": datetime.datetime.now()
            }
            mongo_db.materials.insert_one(new_material)
            return JsonResponse({"message": "Material uploaded successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def generate_attendance_report(request, course_id):
    if request.method == 'GET':
        try:
            attendance_records = mongo_db.attendance.find({"course_id": ObjectId(course_id)})
            present_count = sum(1 for record in attendance_records if record["status"] == "Present")
            total_count = mongo_db.students.count_documents({"course_id": ObjectId(course_id)})
            attendance_percentage = (present_count / total_count) * 100 if total_count else 0
            return JsonResponse({"attendance_percentage": attendance_percentage})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)



def search_courses(request):
    if request.method == 'GET':
        query = request.GET.get("query", "")
        courses = list(mongo_db.courses.find({"name": {"$regex": query, "$options": "i"}}, {"_id": 0}))
        return JsonResponse({"results": courses}, safe=False)


@csrf_exempt
def update_syllabus(request, course_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            mongo_db.courses.update_one(
                {"_id": ObjectId(course_id)},
                {"$set": {"syllabus": data.get("syllabus"), "updated_at": datetime.datetime.now()}}
            )
            return JsonResponse({"message": "Syllabus updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def view_course_profile(request, course_id):
    if request.method == 'GET':
        course = mongo_db.courses.find_one({"_id": ObjectId(course_id)}, {"_id": 0})
        modules = list(mongo_db.modules.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
        return JsonResponse({"course": course, "modules": modules}, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def view_submissions(request, assignment_id):
    if request.method == 'GET':
        try:
            submissions = list(mongo_db.submissions.find({"assignment_id": ObjectId(assignment_id)}, {"_id": 0}))
            return JsonResponse({"submissions": submissions}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message_data = {
                "sender_id": data.get("sender_id"),
                "recipient_id": data.get("recipient_id"),
                "message": data.get("message"),
                "sent_at": datetime.datetime.now()
            }
            mongo_db.messages.insert_one(message_data)
            return JsonResponse({"message": "Message sent successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def add_module(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_module = {
                "course_id": ObjectId(course_id),
                "title": data.get("title"),
                "description": data.get("description"),
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now()
            }
            result = mongo_db.modules.insert_one(new_module)
            return JsonResponse({"message": "Module created successfully", "module_id": str(result.inserted_id)}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def update_module(request, module_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            updated_data = {
                "title": data.get("title"),
                "description": data.get("description"),
                "updated_at": datetime.datetime.now()
            }
            mongo_db.modules.update_one({"_id": ObjectId(module_id)}, {"$set": updated_data})
            return JsonResponse({"message": "Module updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def manage_enrollment(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get("student_id")
            action = data.get("action")  # 'add' or 'remove'
            if action == "add":
                mongo_db.enrollments.insert_one({"course_id": ObjectId(course_id), "student_id": student_id})
                return JsonResponse({"message": "Student added to course"}, status=201)
            elif action == "remove":
                mongo_db.enrollments.delete_one({"course_id": ObjectId(course_id), "student_id": student_id})
                return JsonResponse({"message": "Student removed from course"}, status=200)
            else:
                return JsonResponse({"error": "Invalid action"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def view_gradebook(request, course_id):
    if request.method == 'GET':
        try:
            gradebook = list(mongo_db.submissions.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
            return JsonResponse({"gradebook": gradebook}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def auto_grade_quiz(request, submission_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            answers = data.get("answers")  # Dictionary of student answers
            quiz_id = data.get("quiz_id")

            # Retrieve quiz details for correct answers
            quiz = mongo_db.quizzes.find_one({"_id": ObjectId(quiz_id)})
            correct_answers = quiz.get("correct_answers")  # Dictionary of correct answers

            # Auto-grade logic
            score = sum(1 for question, answer in answers.items() if correct_answers.get(question) == answer)
            total_questions = len(correct_answers)
            percentage_score = (score / total_questions) * 100

            # Save graded submission
            mongo_db.submissions.update_one(
                {"_id": ObjectId(submission_id)},
                {"$set": {
                    "grade": percentage_score,
                    "graded_at": datetime.datetime.now(),
                    "auto_graded": True
                }}
            )
            return JsonResponse({"message": "Quiz auto-graded successfully", "score": percentage_score}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


def export_grades_to_csv(request, course_id):
    if request.method == 'GET':
        try:
            submissions = list(mongo_db.submissions.find({"course_id": ObjectId(course_id)}))
            
            # Prepare CSV response
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="grades_report.csv"'

            writer = csv.writer(response)
            writer.writerow(['Student ID', 'Assignment Title', 'Grade', 'Feedback', 'Graded At'])

            for submission in submissions:
                writer.writerow([
                    submission.get('student_id'),
                    submission.get('assignment_title', 'N/A'),
                    submission.get('grade', 'N/A'),
                    submission.get('feedback', ''),
                    submission.get('graded_at', '')
                ])

            return response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def track_grade_history(request, submission_id):
    if request.method == 'GET':
        try:
            history = list(mongo_db.grade_history.find({"submission_id": ObjectId(submission_id)}, {"_id": 0}))
            return JsonResponse({"grade_history": history}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def update_grade_with_history(request, submission_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            new_grade = data.get("grade")
            feedback = data.get("feedback")

            # Retrieve the current grade for history
            submission = mongo_db.submissions.find_one({"_id": ObjectId(submission_id)})
            old_grade = submission.get("grade", "N/A")
            old_feedback = submission.get("feedback", "")

            # Store old grade in history collection
            grade_history = {
                "submission_id": ObjectId(submission_id),
                "old_grade": old_grade,
                "old_feedback": old_feedback,
                "updated_at": datetime.datetime.now()
            }
            mongo_db.grade_history.insert_one(grade_history)

            # Update submission with new grade
            mongo_db.submissions.update_one(
                {"_id": ObjectId(submission_id)},
                {"$set": {
                    "grade": new_grade,
                    "feedback": feedback,
                    "graded_at": datetime.datetime.now()
                }}
            )
            return JsonResponse({"message": "Grade updated successfully and history saved"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def create_quiz_exam(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quiz = {
                "title": data.get("title"),
                "description": data.get("description"),
                "course_id": ObjectId(course_id),
                "questions": data.get("questions"),  # List of questions (each question has 'type', 'content', 'choices', 'answer')
                "is_exam": data.get("is_exam", False),  # True if it's an exam, False if it's a quiz
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now(),
                "duration": data.get("duration"),  # In minutes, for timed quizzes/exams
            }
            result = mongo_db.quizzes.insert_one(quiz)
            return JsonResponse({"message": "Quiz/Exam created successfully", "quiz_id": str(result.inserted_id)}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def create_question_pool(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question_pool = {
                "title": data.get("title"),
                "course_id": ObjectId(course_id),
                "questions": data.get("questions"),  # List of questions for the pool
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now()
            }
            result = mongo_db.question_pools.insert_one(question_pool)
            return JsonResponse({"message": "Question pool created successfully", "pool_id": str(result.inserted_id)}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def get_random_questions(request, pool_id):
    if request.method == 'GET':
        try:
            num_questions = int(request.GET.get('num_questions', 5))
            question_pool = mongo_db.question_pools.find_one({"_id": ObjectId(pool_id)})

            if not question_pool:
                return JsonResponse({"error": "Question pool not found"}, status=404)

            questions = random.sample(question_pool['questions'], min(num_questions, len(question_pool['questions'])))
            return JsonResponse({"random_questions": questions}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def submit_timed_exam(request, submission_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            time_taken = data.get("time_taken")  # Time taken by the student to complete the exam in minutes
            quiz = mongo_db.quizzes.find_one({"_id": ObjectId(submission_id)})

            if time_taken > quiz['duration']:
                return JsonResponse({"error": "Time limit exceeded"}, status=400)

            # Save submission
            submission = {
                "student_id": data.get("student_id"),
                "quiz_id": submission_id,
                "answers": data.get("answers"),
                "submitted_at": datetime.datetime.now(),
                "time_taken": time_taken
            }
            mongo_db.submissions.insert_one(submission)
            return JsonResponse({"message": "Submission received within the time limit"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def ai_proctor_exam(request, submission_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ai_flags = data.get("ai_flags", [])  # List of detected suspicious activities (e.g., multiple faces, tab switching)
            
            proctoring_result = {
                "submission_id": ObjectId(submission_id),
                "student_id": data.get("student_id"),
                "quiz_id": data.get("quiz_id"),
                "ai_flags": ai_flags,
                "proctoring_reported_at": datetime.datetime.now(),
                "cheating_detected": len(ai_flags) > 0
            }

            mongo_db.proctoring_reports.insert_one(proctoring_result)
            return JsonResponse({"message": "Proctoring report saved", "cheating_detected": proctoring_result["cheating_detected"]}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def set_retake_rules(request, quiz_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            retake_policy = {
                "max_attempts": data.get("max_attempts", 1),  # Maximum number of attempts allowed
                "extension_days": data.get("extension_days", 0),  # Days extended for retakes
                "updated_at": datetime.datetime.now()
            }

            mongo_db.quizzes.update_one(
                {"_id": ObjectId(quiz_id)},
                {"$set": {"retake_policy": retake_policy}}
            )
            return JsonResponse({"message": "Retake rules set successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def request_retake(request, submission_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            submission = mongo_db.submissions.find_one({"_id": ObjectId(submission_id)})

            if not submission:
                return JsonResponse({"error": "Submission not found"}, status=404)

            attempts = submission.get("attempts", 0)
            quiz = mongo_db.quizzes.find_one({"_id": ObjectId(submission['quiz_id'])})
            max_attempts = quiz['retake_policy']['max_attempts']

            if attempts >= max_attempts:
                return JsonResponse({"error": "Maximum attempts reached"}, status=400)

            # Allow retake
            mongo_db.submissions.update_one(
                {"_id": ObjectId(submission_id)},
                {"$inc": {"attempts": 1}, "$set": {"retake_requested_at": datetime.datetime.now()}}
            )
            return JsonResponse({"message": "Retake request approved"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


#Disscussion board would also be another thing

@csrf_exempt
def create_discussion_thread(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            thread = {
                "title": data.get("title"),
                "description": data.get("description"),
                "course_id": ObjectId(course_id),
                "created_by": data.get("created_by"),  # Instructor or student
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now()
            }
            result = mongo_db.discussion_threads.insert_one(thread)
            return JsonResponse({"message": "Discussion thread created successfully", "thread_id": str(result.inserted_id)}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def post_comment(request, thread_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comment = {
                "thread_id": ObjectId(thread_id),
                "user_id": data.get("user_id"),
                "comment_text": data.get("comment_text"),
                "posted_at": datetime.datetime.now()
            }
            mongo_db.comments.insert_one(comment)
            return JsonResponse({"message": "Comment posted successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def view_discussion_thread(request, thread_id):
    if request.method == 'GET':
        try:
            thread = mongo_db.discussion_threads.find_one({"_id": ObjectId(thread_id)}, {"_id": 0})
            comments = list(mongo_db.comments.find({"thread_id": ObjectId(thread_id)}, {"_id": 0}))
            return JsonResponse({"thread": thread, "comments": comments}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


#Surveys and forms

@csrf_exempt
def create_survey(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            survey = {
                "title": data.get("title"),
                "questions": data.get("questions"),  # List of questions for the survey
                "course_id": ObjectId(course_id),
                "created_at": datetime.datetime.now()
            }
            result = mongo_db.surveys.insert_one(survey)
            return JsonResponse({"message": "Survey created successfully", "survey_id": str(result.inserted_id)}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def submit_survey_response(request, survey_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response = {
                "survey_id": ObjectId(survey_id),
                "student_id": data.get("student_id"),
                "answers": data.get("answers"),  # List of answers corresponding to survey questions
                "submitted_at": datetime.datetime.now()
            }
            mongo_db.survey_responses.insert_one(response)
            return JsonResponse({"message": "Survey response submitted successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def view_survey_results(request, survey_id):
    if request.method == 'GET':
        try:
            responses = list(mongo_db.survey_responses.find({"survey_id": ObjectId(survey_id)}, {"_id": 0}))
            return JsonResponse({"survey_responses": responses}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


#peer reviews, i don't know how that would actually work as of yet

@csrf_exempt
def create_peer_review_assignment(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            peer_review_assignment = {
                "assignment_id": data.get("assignment_id"),
                "reviewer_id": data.get("reviewer_id"),
                "reviewee_id": data.get("reviewee_id"),
                "course_id": ObjectId(course_id),
                "criteria": data.get("criteria"),  # Criteria for grading/feedback
                "created_at": datetime.datetime.now()
            }
            mongo_db.peer_reviews.insert_one(peer_review_assignment)
            return JsonResponse({"message": "Peer review assignment created successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def submit_peer_review(request, review_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            review = {
                "review_id": ObjectId(review_id),
                "comments": data.get("comments"),
                "score": data.get("score"),
                "submitted_at": datetime.datetime.now()
            }
            mongo_db.peer_review_responses.insert_one(review)
            return JsonResponse({"message": "Peer review submitted successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


#there are more things that can be done, but this is just a basic example of how the backend would work
# tasks will be assigned to eyoel or estifanos


# Course Content Tasks:

@csrf_exempt
def import_export_course_content(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get("action")  # 'import' or 'export'
            
            if action == "export":
                course_content = {
                    "course": mongo_db.courses.find_one({"_id": ObjectId(course_id)}, {"_id": 0}),
                    "modules": list(mongo_db.modules.find({"course_id": ObjectId(course_id)}, {"_id": 0})),
                    "materials": list(mongo_db.materials.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
                }
                return JsonResponse({"message": "Course content exported successfully", "content": course_content}, status=200)
            
            elif action == "import":
                imported_content = data.get("content")
                if imported_content:
                    mongo_db.courses.update_one(
                        {"_id": ObjectId(course_id)},
                        {"$set": imported_content.get("course")}
                    )
                    mongo_db.modules.insert_many(imported_content.get("modules"))
                    mongo_db.materials.insert_many(imported_content.get("materials"))
                    return JsonResponse({"message": "Course content imported successfully"}, status=201)
                else:
                    return JsonResponse({"error": "No content provided for import"}, status=400)

            return JsonResponse({"error": "Invalid action"}, status=400)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def duplicate_module(request, course_id, module_id):
    if request.method == 'POST':
        try:
            module = mongo_db.modules.find_one({"_id": ObjectId(module_id), "course_id": ObjectId(course_id)})
            if not module:
                return JsonResponse({"error": "Module not found"}, status=404)
            
            new_module = module.copy()
            del new_module["_id"]
            new_module["title"] = f"{module['title']} (Copy)"
            new_module["created_at"] = datetime.datetime.now()
            new_module["updated_at"] = datetime.datetime.now()
            
            result = mongo_db.modules.insert_one(new_module)
            return JsonResponse({"message": "Module duplicated successfully", "module_id": str(result.inserted_id)}, status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def schedule_content(request, course_id, module_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            visibility_date = data.get("visibility_date")
            
            mongo_db.modules.update_one(
                {"_id": ObjectId(module_id), "course_id": ObjectId(course_id)},
                {"$set": {
                    "visibility_date": visibility_date,
                    "updated_at": datetime.datetime.now()
                }}
            )
            return JsonResponse({"message": "Content scheduling updated successfully"}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def add_external_resource(request, course_id, module_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_resource = {
                "title": data.get("title"),
                "resource_type": data.get("resource_type"),  # e.g., "video", "pdf", "tool"
                "url": data.get("url"),
                "module_id": ObjectId(module_id),
                "course_id": ObjectId(course_id),
                "added_at": datetime.datetime.now()
            }
            mongo_db.resources.insert_one(new_resource)
            return JsonResponse({"message": "External resource added successfully"}, status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def create_course_template(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            template_name = data.get("template_name")
            course_id = data.get("course_id")
            
            course = mongo_db.courses.find_one({"_id": ObjectId(course_id)}, {"_id": 0})
            modules = list(mongo_db.modules.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
            materials = list(mongo_db.materials.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
            
            if not course:
                return JsonResponse({"error": "Course not found"}, status=404)
            
            template = {
                "template_name": template_name,
                "course": course,
                "modules": modules,
                "materials": materials,
                "created_at": datetime.datetime.now()
            }
            result = mongo_db.templates.insert_one(template)
            return JsonResponse({"message": "Template created successfully", "template_id": str(result.inserted_id)}, status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    elif request.method == 'GET':
        try:
            templates = list(mongo_db.templates.find({}, {"_id": 0}))
            return JsonResponse({"templates": templates}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def apply_course_template(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            template_id = data.get("template_id")
            
            template = mongo_db.templates.find_one({"_id": ObjectId(template_id)})
            if not template:
                return JsonResponse({"error": "Template not found"}, status=404)
            
            mongo_db.courses.update_one(
                {"_id": ObjectId(course_id)},
                {"$set": template["course"]}
            )
            mongo_db.modules.insert_many(template["modules"])
            mongo_db.materials.insert_many(template["materials"])
            
            return JsonResponse({"message": "Template applied successfully"}, status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def archive_course_content(request, course_id):
    if request.method == 'POST':
        try:
            mongo_db.courses.update_one(
                {"_id": ObjectId(course_id)},
                {"$set": {"is_archived": True, "archived_at": datetime.datetime.now()}}
            )
            return JsonResponse({"message": "Course content archived successfully"}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def restore_course_content(request, course_id):
    if request.method == 'POST':
        try:
            mongo_db.courses.update_one(
                {"_id": ObjectId(course_id)},
                {"$set": {"is_archived": False, "restored_at": datetime.datetime.now()}}
            )
            return JsonResponse({"message": "Course content restored successfully"}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def course_version_control(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            version_name = data.get("version_name")
            course = mongo_db.courses.find_one({"_id": ObjectId(course_id)}, {"_id": 0})
            modules = list(mongo_db.modules.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
            materials = list(mongo_db.materials.find({"course_id": ObjectId(course_id)}, {"_id": 0}))

            version = {
                "version_name": version_name,
                "course_id": ObjectId(course_id),
                "course_snapshot": course,
                "modules_snapshot": modules,
                "materials_snapshot": materials,
                "created_at": datetime.datetime.now()
            }
            mongo_db.course_versions.insert_one(version)
            return JsonResponse({"message": "Course version saved successfully"}, status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    elif request.method == 'GET':
        try:
            versions = list(mongo_db.course_versions.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
            return JsonResponse({"versions": versions}, safe=False)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def batch_upload_materials(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            materials = data.get("materials", [])
            
            for material in materials:
                new_material = {
                    "title": material.get("title"),
                    "file_url": material.get("file_url"),
                    "course_id": ObjectId(course_id),
                    "uploaded_at": datetime.datetime.now()
                }
                mongo_db.materials.insert_one(new_material)
            
            return JsonResponse({"message": f"{len(materials)} materials uploaded successfully"}, status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def reorder_modules(request, course_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            ordered_module_ids = data.get("ordered_module_ids", [])
            
            for index, module_id in enumerate(ordered_module_ids):
                mongo_db.modules.update_one(
                    {"_id": ObjectId(module_id), "course_id": ObjectId(course_id)},
                    {"$set": {"order": index}}
                )
            
            return JsonResponse({"message": "Modules reordered successfully"}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


#Content Review and Approval (for collaborative course creation)
@csrf_exempt
def review_content(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content_id = data.get("content_id")
            review_status = data.get("status")  # "approved" or "rejected"
            feedback = data.get("feedback", "")

            mongo_db.course_content.update_one(
                {"_id": ObjectId(content_id), "course_id": ObjectId(course_id)},
                {"$set": {
                    "status": review_status,
                    "review_feedback": feedback,
                    "reviewed_at": datetime.datetime.now()
                }}
            )
            return JsonResponse({"message": "Content review status updated successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


#Draft vs. Published States for Modules and Materials
@csrf_exempt
def publish_module(request, course_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            module_id = data.get("module_id")
            mongo_db.modules.update_one(
                {"_id": ObjectId(module_id), "course_id": ObjectId(course_id)},
                {"$set": {"status": "published", "published_at": datetime.datetime.now()}}
            )
            return JsonResponse({"message": "Module published successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def publish_material(request, course_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            material_id = data.get("material_id")
            mongo_db.materials.update_one(
                {"_id": ObjectId(material_id), "course_id": ObjectId(course_id)},
                {"$set": {"status": "published", "published_at": datetime.datetime.now()}}
            )
            return JsonResponse({"message": "Material published successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


#Permissions and Collaboration Tools
@csrf_exempt
def add_collaborator(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            collaborator_id = data.get("collaborator_id")
            role = data.get("role")  # e.g., "co-instructor", "TA"
            mongo_db.courses.update_one(
                {"_id": ObjectId(course_id)},
                {"$push": {"collaborators": {"user_id": collaborator_id, "role": role}}}
            )
            return JsonResponse({"message": "Collaborator added successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


#Global Search for Course Content
def search_course_content(request):
    if request.method == 'GET':
        query = request.GET.get("query", "")
        results = list(mongo_db.course_content.find({"content": {"$regex": query, "$options": "i"}}, {"_id": 0}))
        return JsonResponse({"results": results}, safe=False)
    

#Interactive Content (Quizzes Embedded in Content)
@csrf_exempt
def add_interactive_section(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_interactive_section = {
                "title": data.get("title"),
                "description": data.get("description"),
                "questions": data.get("questions"),  # list of quiz questions
                "course_id": ObjectId(course_id),
                "created_at": datetime.datetime.now()
            }
            mongo_db.interactive_sections.insert_one(new_interactive_section)
            return JsonResponse({"message": "Interactive section added successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


#Track Student Engagement for Each Module or Content Section

@csrf_exempt
def track_engagement(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            engagement_record = {
                "student_id": data.get("student_id"),
                "course_id": ObjectId(course_id),
                "module_id": data.get("module_id"),
                "interaction_type": data.get("interaction_type"),  # e.g., "view", "completed"
                "timestamp": datetime.datetime.now()
            }
            mongo_db.engagement.insert_one(engagement_record)
            return JsonResponse({"message": "Engagement tracked successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


#Course Announcements and Updates History

def updates_history(request, course_id):
    if request.method == 'GET':
        history = list(mongo_db.announcements.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
        return JsonResponse({"updates_history": history}, safe=False)



#Adaptive Release for Content Based on Performance or Time

@csrf_exempt
def set_adaptive_release(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            adaptive_rules = {
                "module_id": data.get("module_id"),
                "release_criteria": data.get("release_criteria"),  # e.g., "score > 80"
                "course_id": ObjectId(course_id),
                "created_at": datetime.datetime.now()
            }
            mongo_db.adaptive_release.insert_one(adaptive_rules)
            return JsonResponse({"message": "Adaptive release set successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)



#Archive/Unarchive Modules (Not Just the Whole Course)

@csrf_exempt
def archive_module(request, course_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            module_id = data.get("module_id")
            mongo_db.modules.update_one(
                {"_id": ObjectId(module_id), "course_id": ObjectId(course_id)},
                {"$set": {"archived": True, "archived_at": datetime.datetime.now()}}
            )
            return JsonResponse({"message": "Module archived successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# External Tools Integration and API Configuration
@csrf_exempt
def add_external_tool(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_tool = {
                "name": data.get("name"),
                "link": data.get("link"),
                "description": data.get("description"),
                "course_id": ObjectId(course_id),
                "added_at": datetime.datetime.now()
            }
            mongo_db.external_tools.insert_one(new_tool)
            return JsonResponse({"message": "External tool added successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Allows the view to be accessed without CSRF token validation (useful for APIs but ensure security measures are in place).
@csrf_exempt
def set_download_permission(request, course_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            material_id = data.get("material_id")
            download_permission = data.get("can_download", True)
            mongo_db.materials.update_one(
                {"_id": ObjectId(material_id), "course_id": ObjectId(course_id)},
                {"$set": {"can_download": download_permission}}
            )
            return JsonResponse({"message": "Download permission updated successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)



#Set Course Permissions: Assign roles to other instructors or TAs (e.g., co-instructors, graders).
@csrf_exempt
def set_course_permissions(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            role = data.get("role")  # e.g., "co-instructor", "grader"
            mongo_db.courses.update_one(
                {"_id": ObjectId(course_id)},
                {"$push": {"permissions": {"user_id": user_id, "role": role, "assigned_at": datetime.datetime.now()}}}
            )
            return JsonResponse({"message": "Course permissions assigned successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Certificate Issuance (Automatically Issue Certificates of Completion):
@csrf_exempt
def issue_certificate(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get("student_id")
            completion_status = data.get("completion_status", "completed")
            certificate_id = str(ObjectId())
            new_certificate = {
                "certificate_id": certificate_id,
                "course_id": ObjectId(course_id),
                "student_id": student_id,
                "completion_status": completion_status,
                "issued_at": datetime.datetime.now(),
                "certificate_url": f"/certificates/{certificate_id}.pdf"
            }
            mongo_db.certificates.insert_one(new_certificate)
            return JsonResponse({"message": "Certificate issued successfully", "certificate_url": new_certificate["certificate_url"]}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Completion Progress Reports (Generate Reports for Students Needing Certification):
@csrf_exempt
def generate_completion_report(request, course_id):
    if request.method == 'GET':
        try:
            students = list(mongo_db.students.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
            completion_data = []

            for student in students:
                certificate = mongo_db.certificates.find_one({"course_id": ObjectId(course_id), "student_id": student["student_id"]})
                completion_data.append({
                    "student_id": student["student_id"],
                    "name": student.get("name"),
                    "email": student.get("email"),
                    "completion_status": "Completed" if certificate else "Not Completed",
                    "certificate_url": certificate["certificate_url"] if certificate else None
                })

            return JsonResponse({"completion_report": completion_data}, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def revoke_certificate(request, course_id):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            student_id = data.get("student_id")
            mongo_db.certificates.delete_one({"course_id": ObjectId(course_id), "student_id": student_id})
            return JsonResponse({"message": "Certificate revoked successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def upload_certificate_template(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            template_url = data.get("template_url")  # URL to the custom template file
            mongo_db.courses.update_one(
                {"_id": ObjectId(course_id)},
                {"$set": {"certificate_template_url": template_url}}
            )
            return JsonResponse({"message": "Certificate template uploaded successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def download_completion_report(request, course_id):
    if request.method == 'GET':
        try:
            students = list(mongo_db.students.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
            completion_data = []
            for student in students:
                certificate = mongo_db.certificates.find_one({"course_id": ObjectId(course_id), "student_id": student["student_id"]})
                completion_data.append({
                    "student_id": student["student_id"],
                    "name": student.get("name"),
                    "email": student.get("email"),
                    "completion_status": "Completed" if certificate else "Not Completed",
                    "certificate_url": certificate["certificate_url"] if certificate else None
                })

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="completion_report_{course_id}.csv"'
            writer = csv.DictWriter(response, fieldnames=["student_id", "name", "email", "completion_status", "certificate_url"])
            writer.writeheader()
            for row in completion_data:
                writer.writerow(row)

            return response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def clone_course(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_term = data.get("term", "Future Term")
            
            # Fetch course details
            course = mongo_db.courses.find_one({"_id": ObjectId(course_id)})
            if not course:
                return JsonResponse({"error": "Course not found"}, status=404)

            # Create a new course document
            course.pop("_id")  # Remove old course ID
            course["name"] += f" ({new_term})"
            course["created_at"] = datetime.datetime.now()
            new_course_id = mongo_db.courses.insert_one(course).inserted_id

            # Clone modules, assignments, etc.
            for collection_name in ["modules", "assignments", "quizzes", "materials"]:
                content = mongo_db[collection_name].find({"course_id": ObjectId(course_id)})
                for item in content:
                    item.pop("_id")
                    item["course_id"] = new_course_id
                    mongo_db[collection_name].insert_one(item)

            return JsonResponse({"message": "Course cloned successfully", "new_course_id": str(new_course_id)}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def download_all_materials(request, course_id):
    if request.method == 'GET':
        try:
            materials = list(mongo_db.materials.find({"course_id": ObjectId(course_id)}, {"_id": 0, "title": 1, "file_url": 1}))
            if not materials:
                return JsonResponse({"error": "No materials found for this course"}, status=404)
            return JsonResponse({"materials": materials}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

#Version Control for Content
#Purpose: Track changes in course materials (e.g., old vs. updated syllabus or module versions).
@csrf_exempt
def save_versioned_content(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content_id = data.get("content_id")
            content = mongo_db.materials.find_one({"_id": ObjectId(content_id), "course_id": ObjectId(course_id)})
            if not content:
                return JsonResponse({"error": "Content not found"}, status=404)

            # Save previous version to version control collection
            versioned_content = {
                "course_id": ObjectId(course_id),
                "content_id": content_id,
                "content": content,
                "versioned_at": datetime.datetime.now()
            }
            mongo_db.version_control.insert_one(versioned_content)

            return JsonResponse({"message": "Content version saved successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)




@csrf_exempt
def add_private_note(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            note = {
                "instructor_id": data.get("instructor_id"),
                "course_id": ObjectId(course_id),
                "title": data.get("title"),
                "content": data.get("content"),
                "created_at": datetime.datetime.now()
            }
            mongo_db.private_notes.insert_one(note)
            return JsonResponse({"message": "Private note added successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_private_notes(request, course_id):
    if request.method == 'GET':
        try:
            instructor_id = request.GET.get("instructor_id")
            notes = list(mongo_db.private_notes.find({"course_id": ObjectId(course_id), "instructor_id": instructor_id}, {"_id": 0}))
            return JsonResponse({"notes": notes}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)