from django.urls import path
from .views import *

app_name = "attendance"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path('all-classes', classes_list, name='classes_list'),
    path('class-add/',classAdd.as_view(),name='class_add'),
    path('class-edit/<int:pk>',classUpdate.as_view(),name='class_edit'),
    path('class-delete/<int:pk>',classDelete.as_view(),name='class_delete'),
    #...............................................
    path('all-subjects', subject_list, name='subjects_list'),
    path('subject-add/',subjectAdd.as_view(),name='subject_add'),
    path('subject-edit/<int:pk>',subjectUpdate.as_view(),name='subject_edit'),
    path('subject-delete/<int:pk>',subjectDelete.as_view(),name='subject_delete'),
    
     #...............................................
    path('all-student_classes', student_class_list, name='student_class_list'),
    path('student-classes-detail/<int:pk>', student_class_detail, name='student_class_detail'),
]