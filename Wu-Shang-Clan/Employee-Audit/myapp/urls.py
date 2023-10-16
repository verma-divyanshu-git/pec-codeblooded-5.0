from django.contrib import admin
from django.urls import path, include
from .views import *
import emp.views as fun
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",fun.emp_home),
    path("index/",fun.emp_home),
    path("about/",about),
    path("services/",services),
    path("emp/",include('emp.urls'))
]
