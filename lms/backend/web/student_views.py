from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId
import json
import datetime
import csv
import random
from backend.settings import mongo_db
from django.contrib.auth import authenticate
from django.http import JsonResponse

@csrf_exempt
def get_course_details(request, course_id):
    course = mongo_db.course.find_one({"_id": ObjectId(course_id)})
    if course:
        course["_id"] = str(course["_id"])  # Convert ObjectId to string
        return JsonResponse(course, safe=False)
    else:
        return JsonResponse({"error": "Course not found"}, status=404)

@csrf_exempt
def get_enrolled_courses(request, student_id):
    if request.method == "GET":
        # Find the student's enrolled courses by `student_id`
        enrolled_courses = mongo_db.student_enrolled_courses.find_one({"student_id": student_id})
        
        if enrolled_courses:
            # Convert ObjectId to string and prepare response
            courses = enrolled_courses.get("courses", [])
            for course in courses:
                course["_id"] = str(course["_id"])
            return JsonResponse({"enrolled_courses": courses}, safe=False)
        else:
            return JsonResponse({"message": "No enrolled courses found for this student"}, status=404)
    else:
        return JsonResponse({"error": "Only GET requests are allowed"}, status=405)
    
@csrf_exempt
def get_courses(request):
    if request.method == "GET":
        # Fetch all courses from the "course" collection
        courses = list(mongo_db.course.find())
        # Convert ObjectIds to strings for JSON compatibility
        for course in courses:
            course["_id"] = str(course["_id"])
        return JsonResponse({"courses": courses}, safe=False)
    else:
        return JsonResponse({"error": "Only GET requests are allowed"}, status=405)
    
@csrf_exempt
def get_course_details(request, course_id):
    """
    Returns detailed information about a course.
    """
    if request.method == 'GET':
        try:
            course = mongo_db.courses.find_one({"_id": ObjectId(course_id)}, {"_id": 0})
            modules = list(mongo_db.modules.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
            assignments = list(mongo_db.assignments.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
            quizzes = list(mongo_db.quizzes.find({"course_id": ObjectId(course_id)}, {"_id": 0}))

            return JsonResponse({
                "course": course,
                "modules": modules,
                "assignments": assignments,
                "quizzes": quizzes
            }, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def search_available_courses(request):
    """
    Returns a list of available courses based on a search query.
    """
    if request.method == 'GET':
        query = request.GET.get("query", "")
        courses = list(mongo_db.courses.find({"name": {"$regex": query, "$options": "i"}}, {"_id": 0}))
        return JsonResponse({"available_courses": courses}, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def submit_homework(request, assignment_id):
    """
    Allows students to submit homework for an assignment.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get("student_id")
            submission_text = data.get("submission_text")

            mongo_db.homework_submissions.insert_one({
                "assignment_id": ObjectId(assignment_id),
                "student_id": student_id,
                "submission_text": submission_text,
                "submitted_at": datetime.datetime.now(),
                "graded": False
            })

            return JsonResponse({"message": "Homework submitted successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def submit_quiz_answers(request, quiz_id):
    """
    Allows students to submit answers for a quiz.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get("student_id")
            answers = data.get("answers")  # JSON object with question IDs and answers

            mongo_db.quiz_submissions.insert_one({
                "quiz_id": ObjectId(quiz_id),
                "student_id": student_id,
                "answers": answers,
                "submitted_at": datetime.datetime.now(),
                "graded": False
            })

            return JsonResponse({"message": "Quiz submitted successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def view_past_submissions(request, student_id, course_id):
    """
    Returns the past homework and quiz submissions for a student in a course.
    """
    if request.method == 'GET':
        try:
            homework_submissions = list(mongo_db.homework_submissions.find({"student_id": student_id, "course_id": ObjectId(course_id)}, {"_id": 0}))
            quiz_submissions = list(mongo_db.quiz_submissions.find({"student_id": student_id, "course_id": ObjectId(course_id)}, {"_id": 0}))

            return JsonResponse({
                "homework_submissions": homework_submissions,
                "quiz_submissions": quiz_submissions
            }, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def get_announcements(request, course_id):
    """
    Returns all announcements for a course.
    """
    if request.method == 'GET':
        try:
            announcements = list(mongo_db.announcements.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
            return JsonResponse({"announcements": announcements}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def get_grades(request, student_id, course_id):
    """
    Returns the grades for assignments and quizzes for a student in a course.
    """
    if request.method == 'GET':
        try:
            grades = list(mongo_db.grades.find({"student_id": student_id, "course_id": ObjectId(course_id)}, {"_id": 0}))
            return JsonResponse({"grades": grades}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def get_completion_status(request, student_id, course_id):
    """
    Returns the completion status for a course (percentage based on completed tasks).
    """
    if request.method == 'GET':
        try:
            completed_assignments = mongo_db.assignment_submissions.count_documents({"student_id": student_id, "course_id": ObjectId(course_id), "graded": True})
            total_assignments = mongo_db.assignments.count_documents({"course_id": ObjectId(course_id)})

            completed_quizzes = mongo_db.quiz_submissions.count_documents({"student_id": student_id, "course_id": ObjectId(course_id), "graded": True})
            total_quizzes = mongo_db.quizzes.count_documents({"course_id": ObjectId(course_id)})

            total_tasks = total_assignments + total_quizzes
            completed_tasks = completed_assignments + completed_quizzes

            completion_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            return JsonResponse({"completion_percentage": completion_percentage})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def join_group_project(request, group_id):
    """
    Allows a student to join an assigned group project.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get("student_id")

            mongo_db.groups.update_one(
                {"_id": ObjectId(group_id)},
                {"$addToSet": {"members": student_id}}
            )

            return JsonResponse({"message": "Joined group project successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def get_group_members(request, group_id):
    """
    Returns a list of group members for a project.
    """
    if request.method == 'GET':
        try:
            group = mongo_db.groups.find_one({"_id": ObjectId(group_id)}, {"_id": 0, "members": 1})
            return JsonResponse({"group_members": group.get("members", [])})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)




#discussion 

@csrf_exempt
def post_discussion(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_post = {
                "course_id": ObjectId(course_id),
                "student_id": data.get("student_id"),
                "title": data.get("title"),
                "content": data.get("content"),
                "created_at": datetime.datetime.now()
            }
            mongo_db.discussions.insert_one(new_post)
            return JsonResponse({"message": "Discussion post created successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def reply_to_discussion(request, discussion_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_reply = {
                "discussion_id": ObjectId(discussion_id),
                "student_id": data.get("student_id"),
                "content": data.get("content"),
                "replied_at": datetime.datetime.now()
            }
            mongo_db.replies.insert_one(new_reply)
            return JsonResponse({"message": "Reply posted successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def get_discussion_threads(request, course_id):
    if request.method == 'GET':
        try:
            threads = list(mongo_db.discussions.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
            return JsonResponse({"discussion_threads": threads}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)




@csrf_exempt
def add_private_note(request, student_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_note = {
                "student_id": student_id,
                "note_title": data.get("note_title"),
                "note_content": data.get("note_content"),
                "created_at": datetime.datetime.now()
            }
            mongo_db.private_notes.insert_one(new_note)
            return JsonResponse({"message": "Private note added successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def get_private_notes(request, student_id):
    if request.method == 'GET':
        try:
            notes = list(mongo_db.private_notes.find({"student_id": student_id}, {"_id": 0}))
            return JsonResponse({"private_notes": notes}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def download_course_material(request, material_id):
    if request.method == 'GET':
        try:
            material = mongo_db.materials.find_one({"_id": ObjectId(material_id)}, {"_id": 0})
            if material:
                return JsonResponse({"material": material}, safe=False)
            else:
                return JsonResponse({"error": "Material not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def submit_course_feedback(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            feedback = {
                "student_id": data.get("student_id"),
                "course_id": ObjectId(course_id),
                "rating": data.get("rating"),
                "comment": data.get("comment"),
                "submitted_at": datetime.datetime.now()
            }
            mongo_db.course_feedback.insert_one(feedback)
            return JsonResponse({"message": "Feedback submitted successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def get_course_feedback(request, course_id):
    if request.method == 'GET':
        try:
            feedback_list = list(mongo_db.course_feedback.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
            return JsonResponse({"feedback": feedback_list}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)



# Schedule a Q&A session
@csrf_exempt
def schedule_qa_session(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qa_session = {
                "title": data.get("title"),
                "description": data.get("description"),
                "date": data.get("date"),  # "YYYY-MM-DD" format
                "time": data.get("time"),  # "HH:MM:SS" format
                "instructor_id": data.get("instructor_id"),
                "course_id": ObjectId(course_id),
                "link": data.get("link"),  # URL for online session
                "created_at": datetime.datetime.now()
            }
            mongo_db.qa_sessions.insert_one(qa_session)
            return JsonResponse({"message": "Q&A session scheduled successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# View upcoming Q&A sessions for a course
def view_qa_sessions(request, course_id):
    if request.method == 'GET':
        try:
            qa_sessions = list(mongo_db.qa_sessions.find({"course_id": ObjectId(course_id)}, {"_id": 0}))
            return JsonResponse({"qa_sessions": qa_sessions}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Join a live Q&A session
@csrf_exempt
def join_qa_session(request, qa_session_id):
    if request.method == 'POST':
        try:
            session = mongo_db.qa_sessions.find_one({"_id": ObjectId(qa_session_id)})
            if not session:
                return JsonResponse({"error": "Q&A session not found"}, status=404)
            return JsonResponse({"message": "Q&A session joined successfully", "session_link": session.get("link")}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)



# Bookmark lesson, video, or material
@csrf_exempt
def bookmark_content(request, student_id, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            bookmark_data = {
                "student_id": ObjectId(student_id),
                "course_id": ObjectId(course_id),
                "content_id": data.get("content_id"),
                "content_type": data.get("content_type"),  # e.g., "lesson", "video", "material"
                "title": data.get("title"),
                "bookmarked_at": datetime.datetime.now()
            }
            mongo_db.bookmarks.insert_one(bookmark_data)
            return JsonResponse({"message": "Content bookmarked successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# View all bookmarks for a student in a specific course
def view_bookmarks(request, student_id, course_id):
    if request.method == 'GET':
        try:
            bookmarks = list(mongo_db.bookmarks.find({"student_id": ObjectId(student_id), "course_id": ObjectId(course_id)}, {"_id": 0}))
            return JsonResponse({"bookmarks": bookmarks}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Remove a bookmark
@csrf_exempt
def remove_bookmark(request, student_id, bookmark_id):
    if request.method == 'DELETE':
        try:
            result = mongo_db.bookmarks.delete_one({"_id": ObjectId(bookmark_id), "student_id": ObjectId(student_id)})
            if result.deleted_count == 0:
                return JsonResponse({"error": "Bookmark not found"}, status=404)
            return JsonResponse({"message": "Bookmark removed successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)




    

