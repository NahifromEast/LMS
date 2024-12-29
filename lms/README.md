

## **Learning Management System (LMS) Setup Documentation**

### **Overview**
This documentation outlines the setup and configuration of the LMS system, including the integration of MongoDB as the database, Django as the backend framework with `pymongo` for database operations, and React.js for the frontend.

---

### **1. Technology Stack**

#### **Backend**
- **Framework**: Django (without ORM, using `pymongo` for database operations)
- **Database**: MongoDB ( via Compass)
- **Database Library**: `pymongo`
- **API Development**: Django views with REST endpoints

#### **Frontend**
- **Framework**: React.js
- **Frontend Library**: React (version 19)
- **HTTP Client**: Fetch API or Axios (if needed for API calls)

#### **Tools**
- **Postman**: API testing
- **MongoDB Compass**: GUI for database management
- **Visual Studio Code**: IDE for development

---

### **2. Backend Configuration**

#### **Setting Up Django**
1. **Project Structure**:
   - A `backend` directory hosts the Django project with settings, URLs, and apps.
   - A `web` app handles API endpoints for the LMS features.

2. **Installed Packages**:
   - Django
   - Pymongo (`pip install pymongo`)

3. **Database Connection**:
   - Replace default Django ORM connection with MongoDB.
   - In `backend/settings.py`, MongoDB was connected using `pymongo`:

     ```python
     from pymongo import MongoClient

     client = MongoClient("your-mongodb-connection-string")
     mongo_db = client['lms_database']
     ```

4. **Models**:
   - `models.py` was created but not utilized for database operations due to the use of `pymongo`.

5. **Views**:
   - API endpoints handle CRUD operations.
   - Example: Creating a school in the database:
     ```python
     from django.http import JsonResponse
     import datetime

     def create_school(request):
         if request.method == 'POST':
             new_school = {
                 "name": request.POST.get("name"),
                 "address": request.POST.get("address"),
                 "created_at": datetime.datetime.now(),
             }
             mongo_db.schools.insert_one(new_school)
             return JsonResponse({"message": "School created successfully"})
         return JsonResponse({"error": "Invalid request method"}, status=400)
     ```

6. **URLs**:
   - Backend URL configuration:
     ```python
     from django.urls import path
     from . import views

     urlpatterns = [
         path('api/school/create/', views.create_school, name='create_school'),
     ]
     ```

7. **Testing with Postman**:
   - Use Postman to test API endpoints (e.g., POST requests to `/api/school/create/` with the required data).

---

### **3. Database Configuration**

#### **MongoDB Setup**
1. **Hosting**:
   - MongoDB Atlas was used as the database host.
   - Compass connected to the database for local development.

2. **Collections**:
   - The database contains collections for `schools`, `users`, `courses`, etc.

3. **Example Data Model**:
   - School Collection:
     ```json
     {
       "name": "Test School",
       "address": "123 Test Address",
       "created_at": "2024-12-28T12:00:00Z"
     }
     ```

---

### **4. Frontend Configuration**

#### **Setting Up React**
1. **Project Initialization**:
   - Initialized React using `npx create-react-app masesi-frontend`.
   - Resolved compatibility issues with React 19 and dependencies.

2. **Folder Structure**:
   - `src/` directory contains React components and assets.

3. **Testing**:
   - Successfully ran React development server on `http://localhost:3000`.

4. **Connecting to Backend**:
   - Used Fetch API for sending requests to the Django backend.
   - Example API call:
     ```javascript
     fetch('http://127.0.0.1:8000/api/school/create/', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ name: 'Test School', address: '123 Test Address' })
     })
       .then(response => response.json())
       .then(data => console.log(data))
       .catch(error => console.error('Error:', error));
     ```

---

### **5. Workflow**

1. **Admin Features**:
   - Admin creates a school using the `/api/school/create/` endpoint.
   - The school is stored in the MongoDB database.

2. **Manager Features**:
   - Managers will be able to add teachers and students to schools.

3. **Teacher Features**:
   - Teachers will create courses and upload course content.

4. **Student Features**:
   - Students access and enroll in courses.

---

### **6. Challenges and Solutions**

- **Issue**: React version conflicts with dependencies.
  - **Solution**: Used `npm audit fix --force` to resolve issues and ensure compatibility.

- **Issue**: 404 errors in API testing.
  - **Solution**: Verified Django URL configurations and ensured the development server was running.

- **Issue**: Pymongo compatibility with Django.
  - **Solution**: Used `pymongo` directly and avoided Django’s ORM.

---

### **7. Future Steps**

1. **Build Additional Features**:
   - Create more endpoints for manager, teacher, and student functionalities.
   - Implement authentication and authorization.

2. **Frontend Integration**:
   - Use React components to display and interact with backend data.

3. **Testing**:
   - Implement unit and integration tests for backend and frontend.

4. **Deployment**:
   - Deploy backend on a cloud service (e.g., AWS, Heroku).
   - Deploy frontend using services like Vercel or Netlify.

---

### **8. Conclusion**

The LMS setup integrates MongoDB as the backend database with Django handling API logic and React.js for the frontend. Using `pymongo` provides flexibility for MongoDB operations. This architecture allows scalability and easy extension of features as the system evolves.

--- 

Let me know if you'd like additional details or edits!