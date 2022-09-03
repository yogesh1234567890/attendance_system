from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from .models import *
from .forms import *

# Create your views here.
def dashboard(request):
    return render(request, 'index.html')

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
