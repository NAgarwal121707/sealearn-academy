from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import StudentSignUpForm
from .models import Profile
from courses.models import Enrollment, Course


def signup_view(request, role=None):
    """Only students can create accounts. SeaLearn owner is created using createsuperuser."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = StudentSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def dashboard(request):
    Profile.objects.get_or_create(user=request.user)

    # SeaLearn Academy owner/admin should never see student dashboard.
    if request.user.is_staff or request.user.is_superuser:
        return redirect('owner_dashboard')

    enrolled = Enrollment.objects.filter(student=request.user).select_related('course')
    available = Course.objects.filter(is_published=True).exclude(enrollments__student=request.user)[:8]
    return render(request, 'accounts/dashboard.html', {'enrolled': enrolled, 'available': available})
