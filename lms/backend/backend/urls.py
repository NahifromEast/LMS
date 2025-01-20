"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from web import views
from django.contrib import admin
from django.urls import path, include 
from web.views import login_view  # Adjust the import as needed



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/manager/', include('web.manager_urls')),  # Manager-specific endpoints
    path('api/instructor/', include('web.instructor_urls')),  # Instructor-specific endpoints
    path('api/student/', include('web.student_urls')),  # Student-specific endpoints
    path('api/messages/', include('web.messaging_urls')),  # Messaging-related endpoints
    path('api/login/', login_view, name='login'),  # Ensure this path exists
]