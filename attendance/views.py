from django.shortcuts import render, redirect
from datetime import date
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.forms import inlineformset_factory
from django.db import transaction
from django.db.models import Count, F, Subquery, OuterRef, Case, When
from .models import *
from .forms import *

# Create your views here.
def dashboard(request):
    attendance_total_list = []
    classes = Classes.objects.all().annotate(
            max_count = Count('student_class')
        )
    for i in classes:
        attendance = Attendance.objects.filter(subject__subject_class=i.id).values_list('attendance').aggregate(
            attendees = Count(Case(When(attendance=True, then=1))),
        )
        attendance_total_list.append(
            {
                'class': i,
                'attendance': attendance
            }
        )       
    
    context={
        'attendance_total_list': attendance_total_list, 
        'title': 'Dashboard', 
        'date': date.today(), 
        'classes': classes.count(),
        'students': Students.objects.all().count(),
        }
    return render(request, 'index.html',context)

def classes_list(request):
    grade = Classes.objects.all()
    return render(request, "class_list.html", {"grade": grade, 'title': 'Class'})

class classAdd(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model=Classes
    fields='__all__'
    template_name = 'add.html'
    success_url = reverse_lazy('attendance:classes_list')
    success_message = "New Class added successfully"

    def get_context_data(self, **kwargs):
        data = super(classAdd, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = classForm(self.request.POST)
        else:
            data['items'] = classForm()
            data['title'] = 'Class'
            
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        form=context['form']
        if form.is_valid():
            form.save()
        return super(classAdd, self).form_valid(form)


class classUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Classes
    template_name = 'edit.html'
    fields = '__all__'
    success_url = reverse_lazy('attendance:classes_list')
    success_message = "Updated Successfully"
    
    def get_context_data(self, **kwargs):
        data = super(classUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = classForm(self.request.POST)
        else:
            data['items'] = classForm()
            data['title'] = 'Class'
        return data

class classDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Classes
    template_name = 'modal/confirm_delete.html'
    success_url = reverse_lazy('attendance:classes_list')

    
    def get_context_data(self, **kwargs):
        data = super(classDelete, self).get_context_data(**kwargs)
        data['title'] = 'Class'
        
        return data
    
    
#...................................................#


def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, "subject_list.html", {"subjects": subjects, 'title': 'Subject'})

class subjectAdd(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model=Subject
    fields='__all__'
    template_name = 'add.html'
    success_url = reverse_lazy('attendance:subjects_list')
    success_message = "New Subject added successfully"

    def get_context_data(self, **kwargs):
        data = super(subjectAdd, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = SubjectForm(self.request.POST)
        else:
            data['items'] = SubjectForm()
            data['title'] = 'Subject'
            
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        form=context['form']
        if form.is_valid():
            form.save()
        return super(subjectAdd, self).form_valid(form)


class subjectUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Subject
    template_name = 'edit.html'
    fields = '__all__'
    success_url = reverse_lazy('attendance:subjects_list')
    success_message = "Updated Successfully"
    
    def get_context_data(self, **kwargs):
        data = super(subjectUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = SubjectForm(self.request.POST)
        else:
            data['items'] = SubjectForm()
            data['title'] = 'Subject'
        return data

class subjectDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Subject
    template_name = 'modal/confirm_delete.html'
    success_url = reverse_lazy('attendance:subjects_list')

    
    def get_context_data(self, **kwargs):
        data = super(subjectDelete, self).get_context_data(**kwargs)
        data['title'] = 'Subject'
        return data

#...................................................#


def student_class_list(request):
    classes = Classes.objects.all()
    return render(request, "student_class_list.html", {"classes": classes, 'title': 'Students'})

def student_class_detail(request, pk):
    grade = Classes.objects.get(id=pk)
    ItemFormset = inlineformset_factory(Classes, Students, form=StudentForm, extra=1)
    if request.method == 'POST':
        formset = ItemFormset(request.POST, instance=grade)
        if formset.is_valid():
            formset.save()
            from django.contrib import messages
            messages.success(request, 'Poll successfully updated')
            return redirect('attendance:student_class_list')
    else:
        form = InlineclassForm(instance=grade)
        formset = ItemFormset(instance=grade)

    return render(request, 'students.html', {'form': form, 'formset': formset, 'title': 'Students'})



#....................................................#
# Taking attendance now

def attendance_class_list(request):
    classes = Classes.objects.all()
    return render(request, "main-attendance/attendance_class_list.html", {"classes": classes, 'title': 'Attendance'})

def attendance_class_subjects(request, pk):
    subjects = Subject.objects.filter(subject_class=pk)
    return render(request, "main-attendance/attendance_class_subjects.html", {"subjects": subjects, 'title': 'Attendance'})

def attendance_create(request, pk):
    grade = Subject.objects.get(id=pk).subject_class
    students = Students.objects.filter(study_class=grade).order_by('roll_no')
    today_attendance = Attendance.objects.filter(subject=pk, created_at=date.today())
    
    if request.method == 'POST':
        attendees_list = request.POST.getlist('student-attendance')
        existing_attendance = Attendance.objects.filter(subject=pk, created_at=date.today(), attendance=True).values_list('student', flat=True)
        for i in attendees_list:
            if int(i) in list(existing_attendance):
                attendees_list.remove(i)
        attendees = students.filter(id__in=list(map(int, attendees_list)))
        absence = students.exclude(id__in=attendees)
        
        for i in attendees:
            try:
                attendance_instance = Attendance.objects.get(student=i, subject=pk, created_at=date.today())
                attendance_instance.attendance = True
                attendance_instance.save()
            except:
                pass
        existing_absentee = Attendance.objects.filter(subject=pk, created_at=date.today(), attendance=False).values_list('student', flat=True)
        
        for i in attendees_list:
            if int(i) in list(existing_absentee):
                attendance_instance = Attendance.objects.get(student=i, subject=pk, created_at=date.today())
                attendance_instance.attendance = True
                attendance_instance.save()
        
        present_list = []
        absent_list = []
        for i in attendees_list:
            present = Attendance(
                student_id = int(i),
                subject = Subject.objects.get(id=pk),
                attendance = True,
            )
            present_list.append(present)
        for i in absence:
            if Attendance.objects.filter(subject=pk, created_at=date.today(), attendance=False, student=i).exists():
                present = Attendance(
                    student = i,
                    subject = Subject.objects.get(id=pk),
                    attendance = False,
                )
                absent_list.append(present)
        with transaction.atomic():
            Attendance.objects.bulk_create(present_list)
            Attendance.objects.bulk_create(absent_list)

        return redirect('attendance:attendance_class_list')
        
    return render(request, "main-attendance/attendance.html", {"students": students, 'title': 'Attendance', 'today_attendance': today_attendance})

def attendance_display_table(request, pk):
    sub = Subject.objects.get(id=pk)
    students = Students.objects.filter(study_class=sub.subject_class).order_by('roll_no')
    attendance = Attendance.objects.filter(subject=sub).order_by('-created_at').distinct('created_at')
    return render(request, "attendance_table.html", {"attendance": attendance, 'title': 'Attendance', 'students': students, 'sub': sub})