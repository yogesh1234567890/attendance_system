from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from attendance.models import *
from .serializers import *


class AttendanceViewSet(ModelViewSet):
    serializer_class = classSerializer
    queryset = Classes.objects.all()
    http_method_names = ['get']
    
    def list(self, request, *args, **kwargs):            
        classes = self.request.query_params.get('class', None)
        queryset = self.get_queryset()
        if classes:
            queryset = Classes.objects.get(id=classes)
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset)
        
        subjects = Subject.objects.filter(subject_class_id=classes)   
        subjects_list = list(subjects.values_list('subject_name', flat=True))
        classes = serializer.data.get('class_name', None)
        present=[]
        absent=[]
        for i in subjects:
            attendane_present = Attendance.objects.filter(subject=i, attendance=True).count()
            attendane_absent = Attendance.objects.filter(subject=i, attendance=False).count()
            present.append(attendane_present)        
            absent.append(attendane_absent)       
        return Response({'subjects': subjects_list, 'present': present, 'absent': [2,3]})
    
    @action(detail=False, methods=['get'])
    def get_individual_class_attendance(self, request):
        classes = self.request.query_params.get('class')
        print(classes)
        attendance = Classes.objects.filter(id=classes)
        serializer = self.get_serializer(attendance, many=True)
        return Response(serializer.data)
    
    
    
    