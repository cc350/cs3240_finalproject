from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='google_login'),
    path('index/', views.index, name='index'),  # Why is views.index being used twice?
    path('calendar/', views.CalendarView.as_view(), name='calendar'),

    # Tasks 
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<pk>/update',views.task_update, name='task_update'),
    path('tasks/<pk>/delete', views.task_delete, name='task_delete'),

    # Notes
    path('notes/', views.note_list, name='note_list'),
    path('notes/create', views.note_create, name='note_create'),
    path('notes/<pk>/delete', views.note_delete, name='note_delete'),

    # Courses
    path('my-courses/', views.my_courses, name='my_courses'),
    path('my-courses/<pk>/', views.my_course_detail, name="my_course_detail"),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<pk>/delete', views.course_delete, name='course_delete'),
    path('courses/<pk>/join', views.course_join, name='course_join'),

    # Auth views 
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(), name='logout'),
    path('Profile/', views.profile, name='Profile'),
    path('edit_profile/', views.UserEditView.as_view(), name='edit_profile'),
    path('password/', views.PasswordsChangeView.as_view(template_name = 'change_password.html')),
    path('password_success/', views.password_success, name='password_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
