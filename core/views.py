from django.shortcuts import render
from courses.models import Course

def home(request):
    featured_courses = Course.objects.filter(is_published=True)[:6]
    return render(request, 'core/home.html', {'featured_courses': featured_courses})
