import datetime
import bcrypt
import json
import random
import datetime
from django.core.mail import send_mail
from django.http import JsonResponse
from bson import ObjectId
from django.conf import settings
from backend.settings import mongo_db
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from pymongo import MongoClient
from bson import ObjectId
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
course_db = client['course']  # Use the 'course' database

def login_view(request):
    return JsonResponse({"message": "Login Page Placeholder"})

def dashboard_view(request):
    return JsonResponse({"message": "Dashboard Page Placeholder"})

def generate_mfa_code(user_id):
    # Generate a 6-digit OTP
    mfa_code = str(random.randint(100000, 999999))
    expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=5)

    # Store OTP and expiry in the database
    mongo_db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"mfa_code": mfa_code, "mfa_expiry": expiry_time}}
    )

    # Send the OTP via email (or SMS using an external service)
    user = mongo_db.users.find_one({"_id": ObjectId(user_id)})
    send_mail(
        'Your MFA Code',
        f'Your MFA code is: {mfa_code}',
        'no-reply@masesi.com',
        [user['email']],
        fail_silently=False,
    )
    return {"message": "MFA code sent successfully"}

@csrf_exempt
def validate_mfa_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get("user_id")
        mfa_code = data.get("mfa_code")

        user = mongo_db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        # Check if the MFA code is valid and not expired
        if user.get("mfa_code") == mfa_code and datetime.datetime.now() <= user.get("mfa_expiry"):
            # Clear the MFA code after validation
            mongo_db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$unset": {"mfa_code": "", "mfa_expiry": ""}}
            )
            return JsonResponse({"message": "MFA validated successfully"}, status=200)

        return JsonResponse({"error": "Invalid or expired MFA code"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)



def get_courses(request):
    courses = list(mongo_db.course.find({}, {"_id": 1, "name": 1, "description": 1}))  # Include _id, name, and description
    for course in courses:
        course["_id"] = str(course["_id"])  # Convert ObjectId to string
    return JsonResponse(courses, safe=False)
    

def add_course(request):
    new_course = {
        "title": "New Course",
        "description": "Description of the new course",
        "created_at": datetime.datetime.now(),
    }
    mongo_db.courses.insert_one(new_course)
    return JsonResponse({"message": "Course added successfully"})

print(mongo_db.list_collection_names())



def home(request):
    return render(request, 'home.html')  # Use a template for the homepage


def role_required(*roles):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            user_role = request.headers.get("Role")  # Example: Use JWT or headers
            if user_role not in roles:
                return JsonResponse({"error": "Permission denied"}, status=403)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator



#Admin tasks would include these tasks below

@csrf_exempt
@role_required("admin")
def create_school(request):
    if request.method == 'POST':
        try:
            if not request.body:
                return JsonResponse({"error": "Empty request body"}, status=400)
            data = json.loads(request.body)
            new_school = {
                "name": data.get("name"),
                "address": data.get("address"),
                "created_at": datetime.datetime.now(),
            }
            result = mongo_db.schools.insert_one(new_school)
            return JsonResponse({"message": "School created successfully", "school_id": str(result.inserted_id)}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
@csrf_exempt
def get_schools(request):
    schools = list(mongo_db.schools.find({}, {"_id": 0}))  # Exclude ObjectId
    return JsonResponse(schools, safe=False)


@csrf_exempt
@role_required("admin")
def update_school(request, school_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            mongo_db.schools.update_one(
                {"_id": ObjectId(school_id)},
                {"$set": {"name": data['name'], "address": data['address']}}
            )
            return JsonResponse({"message": "School updated successfully"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def delete_school(request, school_id):
    if request.method == 'DELETE':
        mongo_db.schools.delete_one({"_id": ObjectId(school_id)})
        return JsonResponse({"message": "School deleted successfully"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def get_school_details(request, school_id):
    school = mongo_db.schools.find_one({"_id": school_id})
    if not school:
        return JsonResponse({"error": "School not found"}, status=404)
    return JsonResponse(school, safe=False)

def search_schools(request):
    query = request.GET.get('query', '')
    schools = list(mongo_db.schools.find({"name": {"$regex": query, "$options": "i"}}))
    return JsonResponse(schools, safe=False)

@csrf_exempt
@role_required("admin")
def assign_manager(request, school_id):
    if request.method == "POST":
        data = json.loads(request.body)
        manager_id = data.get("manager_id")
        mongo_db.schools.update_one(
            {"_id": school_id},
            {"$set": {"manager": manager_id}}
        )
        return JsonResponse({"message": "Manager assigned successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

@role_required("admin")
def create_language(request):
    if request.method == "POST":
        data = json.loads(request.body)
        new_language = {
            "name": data.get("name"),
            "code": data.get("code")  # e.g., 'en' for English, 'fr' for French
        }
        mongo_db.languages.insert_one(new_language)
        return JsonResponse({"message": "Language added successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

@role_required("admin")
def get_languages(request):
    if request.method == "GET":
        languages = list(mongo_db.languages.find({}, {"_id": 0}))
        return JsonResponse(languages, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@role_required("admin")
def get_pending_users(request):
    if request.method == "GET":
        users = list(mongo_db.users.find({"status": "pending"}, {"_id": 0}))
        return JsonResponse(users, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@role_required("admin")
def approve_user(request, user_id):
    if request.method == "POST":
        mongo_db.users.update_one({"_id": user_id}, {"$set": {"status": "approved"}})
        return JsonResponse({"message": "User approved successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

@role_required("admin")
def reject_user(request, user_id):
    if request.method == "POST":
        mongo_db.users.update_one({"_id": user_id}, {"$set": {"status": "rejected"}})
        return JsonResponse({"message": "User rejected successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)


@role_required("manager", "admin")
def get_reports_summary(request):
    if request.method == "GET":
        schools_count = mongo_db.schools.count_documents({})
        users_count = mongo_db.users.count_documents({})
        courses_count = mongo_db.courses.count_documents({})
        return JsonResponse({
            "schools_count": schools_count,
            "users_count": users_count,
            "courses_count": courses_count,
        })
    return JsonResponse({"error": "Invalid request method"}, status=405)

# View user details
@csrf_exempt
@role_required("manager", "admin")
def view_user(request, user_id):
    if request.method == 'GET':
        user = mongo_db.users.find_one({"_id": ObjectId(user_id)}, {"_id": 0})
        if user:
            return JsonResponse(user, status=200, safe=False)
        return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Create a new user
@role_required("manager", "admin")
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_user = {
            "name": data.get("name"),
            "email": data.get("email"),
            "role": data.get("role"),  # admin, manager, teacher, student
            "password": data.get("password"),
            "school_id": data.get("school_id"),
            "created_at": datetime.datetime.now(),
        }
        user_id = mongo_db.users.insert_one(new_user).inserted_id

        log_action("create_user", request.headers.get("User-ID"), {"user_id": str(user_id)})

        return JsonResponse({"message": "User created successfully", "user_id": str(user_id)}, status=201)
    return JsonResponse({"error": "Invalid request method"}, status=400)

# Update an existing user
@csrf_exempt
@role_required("manager", "admin")
def update_user(request, user_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            mongo_db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"name": data['name'], "email": data['email'], "role": data['role'], "school_id": data['school_id']}}
            )
            
            # Log the action
            log_action("update_user", request.headers.get("User-ID"), {"user_id": user_id})
            
            return JsonResponse({"message": "User updated successfully"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Delete a user
@csrf_exempt
@role_required("manager", "admin")
def delete_user(request, user_id):
    if request.method == 'DELETE':
        mongo_db.users.delete_one({"_id": ObjectId(user_id)})
        
        # Log the action
        log_action("delete_user", request.headers.get("User-ID"), {"user_id": user_id})
        
        return JsonResponse({"message": "User deleted successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

# List all users
@role_required("manager", "admin")
def list_users(request):
    if request.method == 'GET':
        users = list(mongo_db.users.find({}, {"_id": 0}))
        return JsonResponse({"users": users}, status=200, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)



def change_user_role(request, user_id):
    new_role = request.POST.get('role')
    result = mongo_db.users.update_one({"_id": user_id}, {"$set": {"role": new_role}})
    if result.modified_count == 0:
        return JsonResponse({"error": "Role not updated"}, status=400)
    return JsonResponse({"message": "Role updated successfully"})

def activate_user(request, user_id):
    result = mongo_db.users.update_one({"_id": user_id}, {"$set": {"active": True}})
    if result.modified_count == 0:
        return JsonResponse({"error": "User not activated"}, status=400)
    return JsonResponse({"message": "User activated successfully"})

@role_required("admin", "manager")
def deactivate_user(request, user_id):
    result = mongo_db.users.update_one({"_id": user_id}, {"$set": {"active": False}})
    if result.modified_count == 0:
        return JsonResponse({"error": "User not deactivated"}, status=400)
    return JsonResponse({"message": "User deactivated successfully"})

def list_users_paginated(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    skip = (page - 1) * page_size
    users = list(mongo_db.users.find().skip(skip).limit(page_size))
    return JsonResponse(users, safe=False)


#login functionality

def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        user = mongo_db.users.find_one({"email": email})
        if not user:
            return JsonResponse({"error": "Invalid email or password"}, status=401)

        # Check if the account is locked
        if user.get("lockout_until") and datetime.datetime.now() < user["lockout_until"]:
            return JsonResponse({"error": "Account is locked. Try again later."}, status=403)

        # Verify password (hash comparison recommended)
        if user.get("password") != password:
            # Increment failed attempts
            failed_attempts = user.get("failed_attempts", 0) + 1
            lockout_time = None
            if failed_attempts >= 5:
                lockout_time = datetime.datetime.now() + datetime.timedelta(minutes=30)

            mongo_db.users.update_one(
                {"_id": user["_id"]},
                {"$set": {"failed_attempts": failed_attempts, "lockout_until": lockout_time}}
            )
            return JsonResponse({"error": "Invalid email or password"}, status=401)

        # Reset failed attempts on successful login
        mongo_db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"failed_attempts": 0, "lockout_until": None}}
        )

        return JsonResponse({"message": "Login successful"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def logout_user(request):
    return JsonResponse({"message": "Logout successful"})


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, plain_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

@csrf_exempt
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def register_user(request):
    user_data = request.POST.dict()
    user_data['password'] = hash_password(user_data['password'])
    mongo_db.users.insert_one(user_data)
    
    # Log the action
    log_action("register_user", request.headers.get("User-ID"), {"user_id": str(user_data.get("username"))})
    
    return JsonResponse({"message": "User registered successfully"})



@csrf_exempt
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@role_required("manager", "admin")
def forgot_password(request):
    username = request.POST.get('username')
    new_password = hash_password(request.POST.get('new_password'))
    result = mongo_db.users.update_one({"username": username}, {"$set": {"password": new_password}})
    
    # Log the action
    log_action("forgot_password", request.headers.get("User-ID"), {"username": username})
    
    if result.modified_count == 0:
        return JsonResponse({"error": "Password not updated"}, status=400)
    return JsonResponse({"message": "Password reset successfully"})

# Reset user password
@csrf_exempt
@role_required("manager", "admin")
def reset_user_password(request, user_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            mongo_db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"password": data['password']}}
            )
            
            # Log the action
            log_action("reset_user_password", request.headers.get("User-ID"), {"user_id": user_id})
            
            return JsonResponse({"message": "User password reset successfully"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Add a new language
@csrf_exempt
@role_required("admin")
def add_language(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_language = {
            "name": data.get("name"),
            "code": data.get("code"),  # e.g., 'en', 'fr', 'am'
            "created_at": datetime.datetime.now(),
        }
        mongo_db.languages.insert_one(new_language)
        return JsonResponse({"message": "Language added successfully"}, status=201)
    return JsonResponse({"error": "Invalid request method"}, status=400)

# List all languages
def list_languages(request):
    if request.method == 'GET':
        languages = list(mongo_db.languages.find({}, {"_id": 0}))
        return JsonResponse({"languages": languages}, status=200, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)



@csrf_exempt
def update_course(request, course_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            mongo_db.courses.update_one(
                {"_id": ObjectId(course_id)},
                {"$set": data}
            )
            
            # Log the action
            log_action("update_course", request.headers.get("User-ID"), {"course_id": course_id})
            
            return JsonResponse({"message": "Course updated successfully"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def delete_course(request, course_id):
    if request.method == 'DELETE':
        mongo_db.courses.delete_one({"_id": ObjectId(course_id)})
        
        # Log the action
        log_action("delete_course", request.headers.get("User-ID"), {"course_id": course_id})
        
        return JsonResponse({"message": "Course deleted successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

def enroll_students(request, course_id):
    student_ids = request.POST.getlist('student_ids')
    mongo_db.courses.update_one({"_id": course_id}, {"$addToSet": {"students": {"$each": student_ids}}})
    return JsonResponse({"message": "Students enrolled successfully"})



def log_action(action, user_id, details):
    """
    Logs an action performed by a user in the system.

    Args:
        action (str): The type of action performed (e.g., "create_course", "reset_password").
        user_id (str): The ID of the user performing the action.
        details (dict): Additional details about the action (e.g., course_id, timestamp).
    """
    mongo_db.logs.insert_one({
        "action": action,
        "user_id": user_id,
        "details": details,
        "timestamp": datetime.datetime.now()
    })


@role_required("manager")
def get_logs(request):
    logs = list(mongo_db.logs.find({}, {"_id": 0}))
    return JsonResponse({"logs": logs}, status=200)



#Manager tasks would include these tasks below

@csrf_exempt
@role_required("manager")
def assign_teacher(request, school_id, course_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            teacher_id = data.get("teacher_id")
            mongo_db.courses.update_one(
                {"_id": ObjectId(course_id), "school_id": ObjectId(school_id)},
                {"$set": {"teacher": teacher_id}}
            )
            return JsonResponse({"message": "Teacher assigned to course successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@role_required("manager")
def enroll_student(request, school_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            student = {
                "name": data.get("name"),
                "email": data.get("email"),
                "school_id": ObjectId(school_id),
                "created_at": datetime.datetime.now()
            }
            result = mongo_db.students.insert_one(student)
            return JsonResponse({"message": "Student enrolled successfully", "student_id": str(result.inserted_id)}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@role_required("manager")
def update_student(request, school_id, student_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            update_data = {
                "name": data.get("name"),
                "email": data.get("email"),
            }
            mongo_db.students.update_one(
                {"_id": ObjectId(student_id), "school_id": ObjectId(school_id)},
                {"$set": update_data}
            )
            return JsonResponse({"message": "Student updated successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@role_required("manager")
def remove_student(request, school_id, student_id):
    if request.method == "DELETE":
        try:
            mongo_db.students.delete_one({"_id": ObjectId(student_id), "school_id": ObjectId(school_id)})
            return JsonResponse({"message": "Student removed successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@role_required("manager")
def view_school_reports(request, school_id):
    if request.method == "GET":
        try:
            school = mongo_db.schools.find_one({"_id": ObjectId(school_id)})
            if not school:
                return JsonResponse({"error": "School not found"}, status=404)
            
            courses_count = mongo_db.courses.count_documents({"school_id": ObjectId(school_id)})
            students_count = mongo_db.students.count_documents({"school_id": ObjectId(school_id)})
            teachers_count = mongo_db.teachers.count_documents({"school_id": ObjectId(school_id)})
            
            return JsonResponse({
                "school_name": school["name"],
                "courses_count": courses_count,
                "students_count": students_count,
                "teachers_count": teachers_count,
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@role_required("manager")
def approve_course(request, school_id, course_id):
    if request.method == "POST":
        try:
            mongo_db.courses.update_one(
                {"_id": ObjectId(course_id), "school_id": ObjectId(school_id)},
                {"$set": {"status": "approved"}}
            )
            return JsonResponse({"message": "Course approved successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
@role_required("manager")
def reject_course(request, school_id, course_id):
    if request.method == "POST":
        try:
            mongo_db.courses.update_one(
                {"_id": ObjectId(course_id), "school_id": ObjectId(school_id)},
                {"$set": {"status": "rejected"}}
            )
            return JsonResponse({"message": "Course rejected successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@role_required("manager")
def create_announcement(request, school_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            announcement = {
                "title": data.get("title"),
                "content": data.get("content"),
                "school_id": ObjectId(school_id),
                "created_at": datetime.datetime.now()
            }
            mongo_db.announcements.insert_one(announcement)
            return JsonResponse({"message": "Announcement created successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# List all teachers
def list_teachers(request):
    if request.method == 'GET':
        teachers = list(mongo_db.users.find({"role": "teacher"}, {"_id": 0}))
        return JsonResponse({"teachers": teachers}, status=200, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)

# List all students
def list_students(request):
    if request.method == 'GET':
        students = list(mongo_db.users.find({"role": "student"}, {"_id": 0}))
        return JsonResponse({"students": students}, status=200, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)
















######################################################################################################
######################       Manager tasks would include these tasks below       ####################























# View student details
@role_required("manager", "instructor")
def view_student(request, student_id):
    if request.method == 'GET':
        student = mongo_db.users.find_one({"_id": ObjectId(student_id), "role": "student"}, {"_id": 0})
        if student:
            return JsonResponse(student, status=200, safe=False)
        return JsonResponse({"error": "Student not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)


# View all students in a course
@role_required("manager", "instructor")
def view_students_in_course(request, course_id):
    if request.method == 'GET':
        course = mongo_db.courses.find_one({"_id": ObjectId(course_id)})
        if not course:
            return JsonResponse({"error": "Course not found"}, status=404)
        students = list(mongo_db.users.find({"_id": {"$in": course.get("students", [])}, "role": "student"}, {"_id": 0}))
        return JsonResponse({"students": students}, status=200, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)


# View assignments for a course
@role_required("manager", "instructor")
def view_assignments_for_course(request, course_id):
    if request.method == 'GET':
        assignments = list(mongo_db.assignments.find({"course_id": course_id}, {"_id": 0}))
        return JsonResponse({"assignments": assignments}, status=200, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)


# View course reports
@role_required("manager", "instructor")
def view_course_reports(request, course_id):
    if request.method == 'GET':
        reports = mongo_db.reports.find_one({"course_id": course_id}, {"_id": 0})
        if reports:
            return JsonResponse(reports, status=200, safe=False)
        return JsonResponse({"error": "No reports found for this course"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)


# Track student activity in a course
@role_required("manager", "instructor")
def track_student_activity(request, course_id):
    if request.method == 'GET':
        activity_logs = list(mongo_db.activity_logs.find({"course_id": course_id}, {"_id": 0}))
        return JsonResponse({"activity_logs": activity_logs}, status=200, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)


# Create student groups
@csrf_exempt
@role_required("manager", "instructor")
def create_student_group(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            group_name = data.get("group_name")
            student_ids = data.get("student_ids", [])
            if not group_name or not student_ids:
                return JsonResponse({"error": "Group name and student IDs are required"}, status=400)
            new_group = {
                "group_name": group_name,
                "students": student_ids,
                "created_at": datetime.datetime.now(),
            }
            mongo_db.student_groups.insert_one(new_group)
            return JsonResponse({"message": "Student group created successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)






@csrf_exempt
@role_required('manager')
def approve_course(request, course_id):
    if request.method == 'POST':
        result = mongo_db.courses.update_one({"_id": ObjectId(course_id)}, {"$set": {"status": "approved"}})
        if result.modified_count == 0:
            return JsonResponse({"error": "Course not found or already approved"}, status=400)
        return JsonResponse({"message": "Course approved successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
@role_required('manager')
def reject_course(request, course_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        reason = data.get("reason", "No reason provided")
        result = mongo_db.courses.update_one({"_id": ObjectId(course_id)}, {"$set": {"status": "rejected", "rejection_reason": reason}})
        if result.modified_count == 0:
            return JsonResponse({"error": "Course not found or already rejected"}, status=400)
        return JsonResponse({"message": "Course rejected successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
@role_required('manager')
def get_instructor_details(request, instructor_id):
    if request.method == 'GET':
        instructor = mongo_db.users.find_one({"_id": ObjectId(instructor_id), "role": "instructor"}, {"_id": 0})
        if not instructor:
            return JsonResponse({"error": "Instructor not found"}, status=404)
        courses = list(mongo_db.courses.find({"instructor_id": instructor_id}, {"_id": 0}))
        instructor['courses'] = courses
        return JsonResponse(instructor, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@role_required('manager')
def assign_course(request, instructor_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        course_id = data.get("course_id")
        result = mongo_db.courses.update_one({"_id": ObjectId(course_id)}, {"$set": {"instructor_id": instructor_id}})
        if result.modified_count == 0:
            return JsonResponse({"error": "Course not found or already assigned"}, status=400)
        return JsonResponse({"message": "Course assigned to instructor successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@role_required('manager')
def get_instructor_reports(request, instructor_id):
    if request.method == 'GET':
        courses = list(mongo_db.courses.find({"instructor_id": instructor_id}))
        total_courses = len(courses)
        total_students = sum(course.get("enrollment", 0) for course in courses)
        average_feedback = sum(course.get("feedback_score", 0) for course in courses) / total_courses if total_courses > 0 else 0
        return JsonResponse({
            "total_courses": total_courses,
            "total_students": total_students,
            "average_feedback": round(average_feedback, 2)
        }, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
@role_required('manager')
def create_instructor_group(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_group = {
            "name": data.get("name"),
            "instructors": data.get("instructors", []),  # List of instructor IDs
            "created_at": datetime.datetime.now()
        }
        result = mongo_db.instructor_groups.insert_one(new_group)
        return JsonResponse({"message": "Group created successfully", "group_id": str(result.inserted_id)})
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
@role_required('manager')
def edit_instructor_group(request, group_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        update_data = {
            "name": data.get("name"),
            "instructors": data.get("instructors", []),
        }
        result = mongo_db.instructor_groups.update_one({"_id": ObjectId(group_id)}, {"$set": update_data})
        if result.modified_count == 0:
            return JsonResponse({"error": "Group not updated or not found"}, status=400)
        return JsonResponse({"message": "Group updated successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@role_required('manager')
def track_instructor_performance(request, instructor_id):
    if request.method == 'GET':
        courses = list(mongo_db.courses.find({"instructor_id": instructor_id}))
        completed_courses = [course for course in courses if course.get("status") == "completed"]
        total_students = sum(course.get("enrollment", 0) for course in completed_courses)
        return JsonResponse({
            "completed_courses": len(completed_courses),
            "total_students_taught": total_students
        }, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)





# Duplicate a Course
@csrf_exempt
@role_required("manager")
def duplicate_course(request, course_id):
    if request.method == 'POST':
        course = mongo_db.courses.find_one({"_id": ObjectId(course_id)})
        if not course:
            return JsonResponse({"error": "Course not found"}, status=404)
        
        course.pop("_id")  # Remove the original course ID
        course["name"] += " (Copy)"
        course["created_at"] = datetime.datetime.now()
        new_course_id = mongo_db.courses.insert_one(course).inserted_id
        
        return JsonResponse({"message": "Course duplicated successfully", "new_course_id": str(new_course_id)}, status=201)
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Archive a Course
@csrf_exempt
@role_required("manager")
def archive_course(request, course_id):
    if request.method == 'PUT':
        result = mongo_db.courses.update_one({"_id": ObjectId(course_id)}, {"$set": {"status": "archived"}})
        if result.modified_count == 0:
            return JsonResponse({"error": "Course not updated"}, status=400)
        return JsonResponse({"message": "Course archived successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Assign Multiple Instructors
@csrf_exempt
@role_required("manager")
def assign_multiple_instructors(request, course_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        instructor_ids = data.get("instructor_ids", [])
        mongo_db.courses.update_one({"_id": ObjectId(course_id)}, {"$addToSet": {"instructors": {"$each": instructor_ids}}})
        return JsonResponse({"message": "Instructors assigned successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Update Course Status
@csrf_exempt
@role_required("manager")
def update_course_status(request, course_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        new_status = data.get("status")
        mongo_db.courses.update_one({"_id": ObjectId(course_id)}, {"$set": {"status": new_status}})
        return JsonResponse({"message": "Course status updated successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Generate Course Report
@role_required("manager")
def generate_course_report(request, course_id):
    course = mongo_db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        return JsonResponse({"error": "Course not found"}, status=404)
    report = {
        "name": course.get("name"),
        "enrollment": len(course.get("students", [])),
        "instructors": course.get("instructors", []),
        "assignments": course.get("assignments", []),
    }
    return JsonResponse(report, safe=False)

# Set Course Pre-requisites
@csrf_exempt
@role_required("manager")
def set_prerequisites(request, course_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        prerequisites = data.get("prerequisites", [])
        mongo_db.courses.update_one({"_id": ObjectId(course_id)}, {"$set": {"prerequisites": prerequisites}})
        return JsonResponse({"message": "Prerequisites set successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Bulk Enroll Students
@csrf_exempt
@role_required("manager")
def bulk_enroll_students(request, course_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_ids = data.get("student_ids", [])
        mongo_db.courses.update_one({"_id": ObjectId(course_id)}, {"$addToSet": {"students": {"$each": student_ids}}})
        return JsonResponse({"message": "Students enrolled successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Remove a Student
@csrf_exempt
@role_required("manager")
def remove_student(request, course_id, student_id):
    if request.method == 'DELETE':
        mongo_db.courses.update_one({"_id": ObjectId(course_id)}, {"$pull": {"students": student_id}})
        return JsonResponse({"message": "Student removed from course"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Monitor Student Progress
@role_required("manager")
def monitor_student_progress(request, student_id):
    student = mongo_db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        return JsonResponse({"error": "Student not found"}, status=404)
    progress = {
        "name": student.get("name"),
        "courses": student.get("courses", []),
        "assignments": student.get("assignments", []),
    }
    return JsonResponse(progress, safe=False)

# Send Notification to Students
@csrf_exempt
@role_required("manager")
def send_notification_to_students(request, course_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        notification = data.get("message")
        mongo_db.notifications.insert_one({
            "course_id": course_id,
            "message": notification,
            "timestamp": datetime.datetime.now(),
        })
        return JsonResponse({"message": "Notification sent successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Manage Groups
@csrf_exempt
@role_required("manager")
def manage_group(request, group_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        updates = {}
        if "name" in data:
            updates["name"] = data["name"]
        if "students" in data:
            updates["students"] = data["students"]
        mongo_db.groups.update_one({"_id": ObjectId(group_id)}, {"$set": updates})
        return JsonResponse({"message": "Group updated successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
@role_required("manager")
def update_course_schedule(request, course_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        schedule = {
            "start_date": data.get("start_date"),
            "end_date": data.get("end_date"),
            "class_timings": data.get("class_timings"),
        }
        mongo_db.courses.update_one({"_id": ObjectId(course_id)}, {"$set": {"schedule": schedule}})
        return JsonResponse({"message": "Schedule updated successfully"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@role_required("manager")
def get_instructor_performance(request, instructor_id):
    courses = list(mongo_db.courses.find({"instructor_id": instructor_id}, {"_id": 0}))
    feedback_scores = [course.get("feedback_score", 0) for course in courses]
    avg_score = sum(feedback_scores) / len(feedback_scores) if feedback_scores else 0
    completion_rates = [course.get("completion_rate", 0) for course in courses]
    avg_completion_rate = sum(completion_rates) / len(completion_rates) if completion_rates else 0
    return JsonResponse({
        "average_feedback_score": avg_score,
        "average_completion_rate": avg_completion_rate
    }, status=200)



@role_required("manager")
def get_student_attendance(request, course_id):
    attendance = list(mongo_db.attendance.find({"course_id": course_id}, {"_id": 0}))
    return JsonResponse({"attendance": attendance}, status=200)


@role_required("manager")
def get_student_performance(request, student_id):
    student_courses = list(mongo_db.courses.find({"students": {"$elemMatch": {"id": student_id}}}))
    performance = [{"course_name": course["title"], "grade": course.get("grade", "N/A")} for course in student_courses]
    return JsonResponse({"performance": performance}, status=200)



@csrf_exempt
def search(request):
    query = request.GET.get("query", "")
    courses = list(mongo_db.courses.find({"title": {"$regex": query, "$options": "i"}}))
    instructors = list(mongo_db.users.find({"role": "instructor", "name": {"$regex": query, "$options": "i"}}))
    students = list(mongo_db.users.find({"role": "student", "name": {"$regex": query, "$options": "i"}}))
    return JsonResponse({
        "courses": courses,
        "instructors": instructors,
        "students": students
    }, safe=False)


@role_required("manager")
def generate_custom_report(request):
    filters = json.loads(request.body).get("filters", {})
    courses = list(mongo_db.courses.find(filters))
    return JsonResponse({"report": courses}, status=200)


@role_required("manager")
def deactivate_user(request, user_id):
    result = mongo_db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"active": False}}
    )
    if result.modified_count == 0:
        return JsonResponse({"error": "Failed to deactivate user"}, status=400)
    return JsonResponse({"message": "User deactivated successfully"})



@role_required("manager")
def transfer_user(request, user_id):
    data = json.loads(request.body)
    new_school_id = data.get("new_school_id")
    mongo_db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"school_id": new_school_id}}
    )
    return JsonResponse({"message": "User transferred successfully"})


def has_permission(user_role, permission):
    role_data = mongo_db.roles.find_one({"role": user_role})
    return permission in role_data.get("permissions", [])



@csrf_exempt
@role_required("manager")  # Ensures only managers can perform this action
def remove_assignment(request, course_id, assignment_id):
    if request.method == "DELETE":
        try:
            # Validate the course
            course = mongo_db.courses.find_one({"_id": ObjectId(course_id)})
            if not course:
                return JsonResponse({"error": "Course not found"}, status=404)

            # Check if the assignment exists in the course
            assignment = mongo_db.assignments.find_one({"_id": ObjectId(assignment_id), "course_id": course_id})
            if not assignment:
                return JsonResponse({"error": "Assignment not found"}, status=404)

            # Remove the assignment from the database
            mongo_db.assignments.delete_one({"_id": ObjectId(assignment_id)})
            log_action("remove_assignment", {
                "course_id": course_id,
                "assignment_id": assignment_id,
                "removed_by": request.headers.get("User-ID")
            })
            return JsonResponse({"message": "Assignment removed successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
@role_required("Manager")
def bulk_upload(request):
    if request.method == "POST":
        try:
            file = request.FILES.get("file")
            if not file:
                return JsonResponse({"error": "No file provided"}, status=400)

            # Parse CSV
            import csv
            decoded_file = file.read().decode("utf-8").splitlines()
            csv_reader = csv.DictReader(decoded_file)

            success_count = 0
            error_count = 0
            errors = []

            for row in csv_reader:
                try:
                    # Assuming the CSV has student_name, email, and course_id columns
                    new_student = {
                        "name": row["student_name"],
                        "email": row["email"],
                        "course_id": row["course_id"],
                        "created_at": datetime.datetime.now(),
                    }
                    mongo_db.students.insert_one(new_student)
                    success_count += 1
                except Exception as e:
                    errors.append({"row": row, "error": str(e)})
                    error_count += 1

            return JsonResponse({
                "message": "Bulk upload processed",
                "success_count": success_count,
                "error_count": error_count,
                "errors": errors,
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)




###################################Messaging features #############################################
@csrf_exempt
def send_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            recipient_id = data.get("recipient_id")
            sender_id = request.headers.get("User-ID")  # Assuming `User-ID` is passed in headers

            if not recipient_id or not sender_id:
                return JsonResponse({"error": "Recipient ID or Sender ID is missing"}, status=400)

            # Validate recipient and sender
            recipient = mongo_db.users.find_one({"_id": ObjectId(recipient_id)})
            sender = mongo_db.users.find_one({"_id": ObjectId(sender_id)})
            if not recipient or not sender:
                return JsonResponse({"error": "Invalid recipient or sender"}, status=400)

            new_message = {
                "recipient_id": ObjectId(recipient_id),
                "sender_id": ObjectId(sender_id),
                "subject": data.get("subject", ""),
                "message_body": data.get("message_body", ""),
                "created_at": datetime.datetime.now(),
                "read": False,
            }
            mongo_db.messages.insert_one(new_message)

            return JsonResponse({"message": "Message sent successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def get_messages(request, user_id):
    if request.method == "GET":
        try:
            # Validate user
            user = mongo_db.users.find_one({"_id": ObjectId(user_id)})
            if not user:
                return JsonResponse({"error": "User not found"}, status=404)

            messages = list(
                mongo_db.messages.find({"recipient_id": ObjectId(user_id)}, {"_id": 0})
            )
            return JsonResponse({"messages": messages}, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def mark_message_read(request, message_id):
    if request.method == "PUT":
        try:
            result = mongo_db.messages.update_one(
                {"_id": ObjectId(message_id)}, {"$set": {"read": True}}
            )
            if result.modified_count == 0:
                return JsonResponse({"error": "Message not found or already read"}, status=404)

            return JsonResponse({"message": "Message marked as read"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def delete_message(request, message_id):
    if request.method == "DELETE":
        try:
            result = mongo_db.messages.delete_one({"_id": ObjectId(message_id)})
            if result.deleted_count == 0:
                return JsonResponse({"error": "Message not found"}, status=404)

            return JsonResponse({"message": "Message deleted successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def send_group_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            sender_id = request.headers.get("User-ID")  # Assuming `User-ID` is passed in headers
            group_type = data.get("group_type")  # "students", "instructors", etc.

            if not sender_id or not group_type:
                return JsonResponse({"error": "Sender ID or Group Type is missing"}, status=400)

            # Validate sender
            sender = mongo_db.users.find_one({"_id": ObjectId(sender_id)})
            if not sender:
                return JsonResponse({"error": "Invalid sender"}, status=400)

            # Get recipients based on group_type
            recipients = list(mongo_db.users.find({"role": group_type}, {"_id": 1}))
            if not recipients:
                return JsonResponse({"error": "No recipients found for this group"}, status=400)

            new_messages = [
                {
                    "recipient_id": recipient["_id"],
                    "sender_id": ObjectId(sender_id),
                    "subject": data.get("subject", ""),
                    "message_body": data.get("message_body", ""),
                    "created_at": datetime.datetime.now(),
                    "read": False,
                }
                for recipient in recipients
            ]
            mongo_db.messages.insert_many(new_messages)

            return JsonResponse({"message": "Group message sent successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def reply_message(request, thread_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            sender_id = request.headers.get("User-ID")  # Assuming `User-ID` is passed in headers

            if not sender_id or not thread_id:
                return JsonResponse({"error": "Sender ID or Thread ID is missing"}, status=400)

            # Validate sender
            sender = mongo_db.users.find_one({"_id": ObjectId(sender_id)})
            if not sender:
                return JsonResponse({"error": "Invalid sender"}, status=400)

            reply_message = {
                "thread_id": ObjectId(thread_id),
                "sender_id": ObjectId(sender_id),
                "message_body": data.get("message_body", ""),
                "created_at": datetime.datetime.now(),
            }
            mongo_db.message_replies.insert_one(reply_message)

            return JsonResponse({"message": "Reply sent successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)



def filter_messages(request, user_id):
    if request.method == "GET":
        try:
            filters = {}
            if "read" in request.GET:
                filters["read"] = request.GET["read"].lower() == "true"
            if "sender_id" in request.GET:
                filters["sender_id"] = ObjectId(request.GET["sender_id"])
            if "start_date" in request.GET and "end_date" in request.GET:
                filters["created_at"] = {
                    "$gte": datetime.datetime.fromisoformat(request.GET["start_date"]),
                    "$lte": datetime.datetime.fromisoformat(request.GET["end_date"]),
                }
            if "keyword" in request.GET:
                filters["message_body"] = {"$regex": request.GET["keyword"], "$options": "i"}

            messages = list(
                mongo_db.messages.find(
                    {"recipient_id": ObjectId(user_id), **filters}, {"_id": 0}
                )
            )
            return JsonResponse(messages, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_unread_count(request, user_id):
    if request.method == "GET":
        try:
            unread_count = mongo_db.messages.count_documents(
                {"recipient_id": ObjectId(user_id), "read": False}
            )
            return JsonResponse({"unread_count": unread_count}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)



def update_profile(request, user_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        mongo_db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": data}
        )
        return JsonResponse({"message": "Profile updated successfully"})


@csrf_exempt
@role_required('manager', 'instructor')
def generate_attendance_report(request, course_id):
    if request.method == 'GET':
        try:
            # Fetch attendance data for the course
            attendance_data = mongo_db.attendance.find({"course_id": ObjectId(course_id)})
            report = []
            for record in attendance_data:
                report.append({
                    "student_id": str(record["student_id"]),
                    "date": record["date"],
                    "status": record["status"]
                })
            
            # Log the action
            log_action("generate_attendance_report", request.headers.get("User-ID"), {"course_id": course_id})
            
            return JsonResponse({"report": report}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)
