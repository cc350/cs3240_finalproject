from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models
from django.urls.base import reverse



class Note(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to="notes/pdfs")

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='notes')
    course = models.ForeignKey("Course", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Course(models.Model): 
    # Changed these fields so that they match what is in the fixture.json that we got from https://devhub.virginia.edu/API 
    subject = models.CharField(max_length=255, null=True)
    catalog_number = models.CharField(max_length=255, null=True)
    #class_section = models.CharField(max_length=255, null=True)
    #class_number = models.IntegerField(null=True)
    class_title = models.CharField(max_length=255, null=True)
    #class_topic_formal_desc = models.TextField(blank=True, null=True)
    #instructor = models.CharField(max_length=255, null=True)
    #enrollment_capacity = models.IntegerField(null=True)
    #meeting_days = models.CharField(max_length=255, null=True)
    #meeting_time_start = models.TimeField(null=True)
    #meeting_time_end = models.TimeField(null=True)
    #term = models.CharField(max_length=255, null=True)
    #term_desc = models.CharField(max_length=255, null=True)

    students = models.ManyToManyField(User, blank=True, related_name='courses')

    def __str__(self):
        return self.name

    # Because Course is now matching the data from the devhub.va API, what was previously "name" changed to "class_title". This method with the @property decorator makes it so that we can access the class_title data in the same way we were before, which was using course.name. Without it, we'd have to write course.name() instead of just course.name, but it would do the same thing.
    @property
    def name(self):
        return self.class_title
    
    def get_absolute_url(self):
        return reverse('home')


    @admin.display(description='Student Names')
    def student_names(self):
        return ",\n".join([student.username for student in self.students.all()])

#Citation for task-list code
#https://arbcoms.com/wp-content/endurance-page-cache/_index.html
class Task(models.Model):
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    due = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    # the next two lines are from https://stackoverflow.com/questions/42794518/show-different-content-based-on-logged-in-user-django
    # ForeignKey is for many to one relationships (so here that is many tasks to one user)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='tasks')
    course = models.ForeignKey("Course", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title
