"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# We can add a login view for use with the browsable API, 
# by editing the URLconf in our project-level urls.py file.
# Add the following import at the top of the file:
from django.conf.urls import include

urlpatterns = [
    path('', include('snippets.urls')),
    path('admin/', admin.site.urls),
    
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]