from django.test import TestCase
from django.utils import timezone

from .models import Task, Note
from .forms import TaskForm

# Create your tests here.
class basicUnitTest(TestCase):
  
    def test_upper(self):
      '''very basic unit test'''
      self.assertEqual('foo'.upper(), 'FOO')
      
    def test_1eq1(self):
      '''another basic unit test'''
      self.assertEqual(1, 1)
      
class taskTest(TestCase):
    def create_task(self, title ="CS 3240 Sprint 4 Report", complete = False, due = "2021-01-01"):
        return Task.objects.create(title=title, complete=complete, created=timezone.now(), due=due)
    
    # checks if task model was created successfully
    def test_task_creation(self):
        t = self.create_task()
        self.assertTrue(isinstance(t, Task))
        self.assertEqual(t.__str__(), t.title)
    
    # test case where a valid date was passed in
    def test_valid_form(self):
        t = Task.objects.create(title ="CS 3240 Sprint 4 Report", due="2021-01-01", course="Science")
        data = {'title': t.title, 'due': t.due, 'course': t.course}
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())
    

    #test case where an invalid date was passed in
    # def test_invalid_form(self):
    #     t = task.objects.create(title ="CS 3240 Sprint 4 Report", due = "01-01-2021")
    #     data = {'title': t.title, 'due': t.due,}
    #     form = TaskForm(data=data)
    #     self.assertIs(form.is_valid, False)



class noteTest(TestCase):
    def create_note(self, title="Test Note for testing", author="Joseph Mama"):
        return Note.objects.create(title=title, author=author)
    
    #checks if a note was created successfully
    def test_note_creation(self):
        n = self.create_note()
        self.assertTrue(isinstance(n, Note))
        self.assertEqual(n._str_(), n.title)

class courseTest(TestCase):
    def create_course(self, subject ="CS", catalog_number = "3240", class_title= "Advanced Software Development"):
        return Course.objects.create(subject=subject, catalog_number=catalog_number, class_title=class_title)
    
    def test_course_creation(self):
      c = self.create_course()
      self.assertTrue(isinstance(c, Course))
      


        
