from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CourseForm, LessonForm
from .models import Course, Enrollment, Lesson


def is_owner(user):
    """SeaLearn Academy has one owner account: the Django staff/superuser."""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def course_list(request):
    courses = Course.objects.filter(is_published=True).select_related('tutor')
    q = request.GET.get('q')
    if q:
        courses = courses.filter(title__icontains=q)
    return render(request, 'courses/course_list.html', {'courses': courses, 'q': q or ''})


def course_detail(request, pk):
    qs = Course.objects.select_related('tutor').prefetch_related('lessons')
    if is_owner(request.user):
        course = get_object_or_404(qs, pk=pk)
    else:
        course = get_object_or_404(qs, pk=pk, is_published=True)

    enrolled = request.user.is_authenticated and Enrollment.objects.filter(student=request.user, course=course).exists()
    can_access_lessons = enrolled or is_owner(request.user)
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'enrolled': enrolled,
        'can_access_lessons': can_access_lessons,
    })


@login_required
def enroll_course(request, pk):
    if is_owner(request.user):
        messages.info(request, 'Owner account can already view all uploaded lessons.')
        return redirect('course_detail', pk=pk)
    course = get_object_or_404(Course, pk=pk, is_published=True)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    messages.success(request, 'You are enrolled successfully.')
    return redirect('course_detail', pk=course.pk)


@login_required
@user_passes_test(is_owner)
def owner_dashboard(request):
    courses = Course.objects.all().prefetch_related('lessons', 'enrollments')
    lessons = Lesson.objects.select_related('course').order_by('-course__created_at', 'order')
    stats = {
        'courses': courses.count(),
        'published': courses.filter(is_published=True).count(),
        'drafts': courses.filter(is_published=False).count(),
        'lessons': lessons.count(),
        'students': Enrollment.objects.values('student').distinct().count(),
    }
    return render(request, 'courses/owner_dashboard.html', {'courses': courses, 'lessons': lessons, 'stats': stats})


# Backward compatibility: old URL names still work, but UI now says Owner.
tutor_dashboard = owner_dashboard


@login_required
@user_passes_test(is_owner)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.tutor = request.user
            course.save()
            messages.success(request, 'Course created successfully.')
            return redirect('owner_dashboard')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Create course'})


@login_required
@user_passes_test(is_owner)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('owner_dashboard')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Edit course'})


@login_required
@user_passes_test(is_owner)
def course_toggle_publish(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.is_published = not course.is_published
    course.save(update_fields=['is_published'])
    messages.success(request, 'Course status updated.')
    return redirect('owner_dashboard')


@login_required
@user_passes_test(is_owner)
def lesson_create(request, course_pk=None):
    initial = {}
    if course_pk:
        initial['course'] = get_object_or_404(Course, pk=course_pk)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video / live class added successfully.')
            return redirect('owner_dashboard')
    else:
        form = LessonForm(initial=initial)
    return render(request, 'courses/lesson_form.html', {'form': form, 'title': 'Add video / live class'})


@login_required
@user_passes_test(is_owner)
def lesson_update(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video / live class updated successfully.')
            return redirect('owner_dashboard')
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'courses/lesson_form.html', {'form': form, 'title': 'Edit video / live class'})
