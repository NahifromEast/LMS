from django.db import models

# class User(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('manager', 'Manager'), ('teacher', 'Teacher'), ('student', 'Student')])
#     school = models.ForeignKey('School', on_delete=models.CASCADE, null=True, blank=True)

# class School(models.Model):
#     name = models.CharField(max_length=100)
#     address = models.TextField()
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_schools")

# class Course(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_courses")
#     school = models.ForeignKey(School, on_delete=models.CASCADE)
#     students = models.ManyToManyField(User, related_name="enrolled_courses", blank=True)