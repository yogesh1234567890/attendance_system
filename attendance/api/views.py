from rest_framework.viewsets import ModelViewSet
from attendance.models import *
from .serializers import *


class AttendanceViewSet(ModelViewSet):
    serializer_class = classSerializer
    queryset = Classes.objects.all()
    http_method_names = ['get']
    
    
    