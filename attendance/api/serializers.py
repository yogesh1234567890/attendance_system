from rest_framework import serializers
from attendance.models import Attendance,Classes, Subject

class subjectAttendanceSerializer(serializers.ModelSerializer):
    present = serializers.SerializerMethodField()
    absent = serializers.SerializerMethodField()
    class Meta:
        model = Subject
        fields = ['subject_name', 'present', 'absent']
        
    def get_present(self, obj):
        return Attendance.objects.filter(subject=obj, attendance=True).count()  
    
    def get_absent(self, obj):
        return Attendance.objects.filter(subject=obj, attendance=False).count()

class classSerializer(serializers.ModelSerializer):
    attendance = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    class Meta:
        model = Classes
        fields = ['class_name', 'attendance', 'total']
        
    def get_attendance(self, instance):
        subjects = Subject.objects.filter(subject_class=instance)
        subject_attendance = subjectAttendanceSerializer(subjects, many=True)
        return subject_attendance.data
    
    def get_total(self, instance):
        return instance.student_class.count()
