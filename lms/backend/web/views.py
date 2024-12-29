import datetime
import json
from django.http import JsonResponse
from bson import ObjectId
from django.conf import settings
from backend.settings import mongo_db
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt





def get_courses(request):
    courses = list(mongo_db.courses.find({}, {"_id": 0}))  # Exclude ObjectId
    print(courses)
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


#Admin tasks would include these tasks below

@csrf_exempt
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

def get_languages(request):
    if request.method == "GET":
        languages = list(mongo_db.languages.find({}, {"_id": 0}))
        return JsonResponse(languages, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_pending_users(request):
    if request.method == "GET":
        users = list(mongo_db.users.find({"status": "pending"}, {"_id": 0}))
        return JsonResponse(users, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def approve_user(request, user_id):
    if request.method == "POST":
        mongo_db.users.update_one({"_id": user_id}, {"$set": {"status": "approved"}})
        return JsonResponse({"message": "User approved successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

def reject_user(request, user_id):
    if request.method == "POST":
        mongo_db.users.update_one({"_id": user_id}, {"$set": {"status": "rejected"}})
        return JsonResponse({"message": "User rejected successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

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
def view_user(request, user_id):
    if request.method == 'GET':
        user = mongo_db.users.find_one({"_id": ObjectId(user_id)}, {"_id": 0})
        if user:
            return JsonResponse(user, status=200, safe=False)
        return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Create a new user
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
        return JsonResponse({"message": "User created successfully", "user_id": str(user_id)}, status=201)
    return JsonResponse({"error": "Invalid request method"}, status=400)

# Update an existing user
def update_user(request, user_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        update_data = {
            "name": data.get("name"),
            "email": data.get("email"),
            "role": data.get("role"),
        }
        mongo_db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        return JsonResponse({"message": "User updated successfully"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)

# Delete a user
def delete_user(request, user_id):
    if request.method == 'DELETE':
        mongo_db.users.delete_one({"_id": ObjectId(user_id)})
        return JsonResponse({"message": "User deleted successfully"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)

# List all users
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
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = mongo_db.users.find_one({"username": username, "password": password})
    if user:
        return JsonResponse({"message": "Login successful"})
    return JsonResponse({"error": "Invalid credentials"}, status=401)

def logout_user(request):
    return JsonResponse({"message": "Logout successful"})

def register_user(request):
    user_data = request.POST.dict()
    mongo_db.users.insert_one(user_data)
    return JsonResponse({"message": "User registered successfully"})

def forgot_password(request):
    username = request.POST.get('username')
    new_password = request.POST.get('new_password')
    result = mongo_db.users.update_one({"username": username}, {"$set": {"password": new_password}})
    if result.modified_count == 0:
        return JsonResponse({"error": "Password not updated"}, status=400)
    return JsonResponse({"message": "Password reset successfully"})

# Reset user password
@csrf_exempt
def reset_user_password(request, user_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            mongo_db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"password": data['password']}}
            )
            return JsonResponse({"message": "User password reset successfully"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Add a new language
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



def update_course(request, course_id):
    updated_data = request.POST.dict()
    result = mongo_db.courses.update_one({"_id": course_id}, {"$set": updated_data})
    if result.modified_count == 0:
        return JsonResponse({"error": "Course not updated"}, status=400)
    return JsonResponse({"message": "Course updated successfully"})

def delete_course(request, course_id):
    result = mongo_db.courses.delete_one({"_id": course_id})
    if result.deleted_count == 0:
        return JsonResponse({"error": "Course not found"}, status=404)
    return JsonResponse({"message": "Course deleted successfully"})

def enroll_students(request, course_id):
    student_ids = request.POST.getlist('student_ids')
    mongo_db.courses.update_one({"_id": course_id}, {"$addToSet": {"students": {"$each": student_ids}}})
    return JsonResponse({"message": "Students enrolled successfully"})



