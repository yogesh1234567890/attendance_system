from django.contrib import admin
from .models import Classes, Subject, Students, Attendance
# Register your models here.
admin.site.register([Classes, Subject, Students, Attendance])