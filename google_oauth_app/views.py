import calendar
from datetime import datetime, timedelta, date
from django.db import models

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import generic

from .forms import NoteForm, EditProfileForm, TaskForm, TaskUpdateForm
from .calendar_api import test_calendar
from .models import Task, Note, Course
from .utils import Calendar
from django.contrib.auth.models import User


def index(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'Profile.html')


# Notes CRUD
def note_list(request):
    notes = Note.objects.all()
    context = {'Notes': notes}
    return render(request, 'note_list.html', context)


def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        #note.author = request.user 
        if form.is_valid():
             note = form.save(commit=False)
             note.created_by = request.user
             note.save()
             return redirect('note_list')
    else:
        form = NoteForm()
        form.fields['course'].queryset = request.user.courses.all()
    return render(request, 'note_create.html', {'form': form})



@login_required
def note_delete(request, pk):
    note = Note.objects.get(pk=pk)
    if request.user == note.created_by and request.method == 'POST':
        note.delete()
        return redirect('note_list')

    context = {'note': note}
    return render(request, 'note_delete.html', context)


# Task CRUD
#Citation for task-list code
#https://arbcoms.com/wp-content/endurance-page-cache/_index.html

@login_required
def task_list(request):
    tasks = Task.objects.order_by('complete', 'due')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        # The following 3 steps are taken from https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication and https://stackoverflow.com/questions/42794518/show-different-content-based-on-logged-in-user-django 
        if form.is_valid():
            # 1. Save the form with commit = False to store the task without saving it to the database
            task = form.save(commit=False)

            # 2. Assign logged in user to that specific task to know who created it
            task.created_by = request.user

            # 3. Save the task.
            task.save()
        return redirect('task_list')
    else: 
        form = TaskForm()
        form.fields['course'].queryset = request.user.courses.all()


    context = {
        'tasks': Task.objects.order_by('complete', 'due').filter(created_by=request.user),
        'form': form,
    }
    return render(request, 'task_list.html', context)


#Citation for task-list code
#https://arbcoms.com/wp-content/endurance-page-cache/_index.html
@login_required
def task_update(request, pk):
    task = Task.objects.get(pk=pk)

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskUpdateForm(instance=task)
        form.fields['course'].queryset = request.user.courses.all()

    context = {'form': form}
    return render(request, 'task_update.html', context)


#Citation for task-list code
#https://arbcoms.com/wp-content/endurance-page-cache/_index.html

@login_required
def task_delete(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    context = {'task': task}
    return render(request, 'task_delete.html', context)


# Course CRUD

def course_list(request):
    #removes all duplicate courses (I don't know where else to put this, seems weird to be in a view tbh...)
    for course in Course.objects.values_list('class_title', flat=True).distinct():
        Course.objects.filter(pk__in=Course.objects.filter(class_title=course).values_list('id', flat=True)[1:]).delete()
    
    courses = Course.objects.all()
    #courses = set(Course.objects.all())

    course_name_query = request.GET.get('q') # This q is from what we named the search input in the course_list view
    if course_name_query:
        courses = courses.filter(class_title__icontains=course_name_query)

    context = {'courses': courses}
    return render(request, 'course_list.html', context)

@login_required
def course_delete(request, pk):
    course = Course.objects.get(id=pk)
    if request.method == 'POST':
        course.students.remove(request.user)
        course.save()
        return redirect('my_courses')

    context = {
        'courseItem': course
    }
    return render(request, 'course_delete.html', context)


@login_required
def course_join(request, pk):
    course = Course.objects.get(pk=pk)
    if request.method == 'POST':
        course.students.add(request.user)
        course.save()
        return redirect('my_courses')

    context = {'course': course}
    return render(request, 'course_join.html', context)


@login_required
def my_courses(request):
    return render(request, 'my_courses.html')

@login_required
def my_course_detail(request, pk):
    course = Course.objects.get(class_title=pk)
    context = {'course': course,
            'tasks':Task.objects.order_by('complete', 'due').filter(created_by=request.user, course=course)}
    return render(request, 'my_course_detail.html', context)


# citation for calendar https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
class CalendarView(generic.ListView):
    model = Task
    template_name = 'calendar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # use today's date for the calendar
        # d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month, user)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime(year, month, day=1)
    return datetime.today()




def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('Profile')

    def get_object(self):
        return self.request.user


class PasswordsChangeView(PasswordChangeView):
    from_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')



def password_success(request):
    return render(request, 'password_success.html', {})


# def demo(request):
#     results = test_calendar()
#     context = {"results": results}
#     return render(request, 'demo.html', context)
