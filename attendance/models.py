from django.db import models

# Create your models here.

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
class Classes(Base):
    class_name = models.CharField(max_length=50)
    class_code = models.CharField(max_length=10, null=True, blank=True)
    class_description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.class_name
    
class Subject(Base):
    subject_name = models.CharField(max_length=50)
    subject_code = models.CharField(max_length=10, null=True, blank=True)
    subject_description = models.CharField(max_length=200, null=True, blank=True)
    subject_class = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='subject_class')
    

    def __str__(self):
        return self.subject_name
    
class Students(Base):
    name = models.CharField(max_length=50)
    roll_no = models.IntegerField()
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    study_class = models.ForeignKey(Classes, related_name="student_class", on_delete=models.CASCADE)

    def __str__(self):
        return self.student_name
    
class Attendance(Base):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    attendance = models.BooleanField(default=False)
    leave_reason = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.student.name