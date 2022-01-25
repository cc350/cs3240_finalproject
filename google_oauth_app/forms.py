
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from .models import Note, Task, Course


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("title", "author", "course", "pdf")

 
#Citation for task-list code
#https://arbcoms.com/wp-content/endurance-page-cache/_index.html
class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Task Title'}), label=False)
    due = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Due Date'}), label=False)

    class Meta:
        model = Task
        fields = ['title', 'due', 'course']

#Citation for task-list code
#https://arbcoms.com/wp-content/endurance-page-cache/_index.html
class TaskUpdateForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Task Title'}))

    class Meta:
        model = Task
        fields = ['title', 'due', 'course', 'complete']




class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username')
