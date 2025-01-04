from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId
import json
import datetime
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


