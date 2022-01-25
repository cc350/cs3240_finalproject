from django.contrib import admin


# Register your models here.
from .models import Task, Course, Note

admin.site.register(Course)
admin.site.register(Task)
admin.site.register(Note)
