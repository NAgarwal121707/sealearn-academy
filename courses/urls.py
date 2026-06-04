from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('owner/', views.owner_dashboard, name='owner_dashboard'),
    path('tutor/', views.owner_dashboard, name='tutor_dashboard'),  # old URL kept only to avoid errors
    path('owner/courses/new/', views.course_create, name='course_create'),
    path('owner/courses/<int:pk>/edit/', views.course_update, name='course_update'),
    path('owner/courses/<int:pk>/publish-toggle/', views.course_toggle_publish, name='course_toggle_publish'),
    path('owner/lessons/new/', views.lesson_create, name='lesson_create'),
    path('owner/courses/<int:course_pk>/lessons/new/', views.lesson_create, name='lesson_create_for_course'),
    path('owner/lessons/<int:pk>/edit/', views.lesson_update, name='lesson_update'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
]
