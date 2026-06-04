from django.conf import settings
from django.db import models
from django.urls import reverse

LEVELS = [('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]
SESSION_TYPES = [('recorded', 'Recorded'), ('live', 'Live')]

class Course(models.Model):
    title = models.CharField(max_length=160)
    subtitle = models.CharField(max_length=220, blank=True)
    description = models.TextField()
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='teaching_courses')
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    level = models.CharField(max_length=20, choices=LEVELS, default='beginner')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_detail', args=[self.pk])

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES, default='recorded')
    video_file = models.FileField(upload_to='recordings/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text='YouTube/Vimeo/private streaming URL')
    live_link = models.URLField(blank=True, help_text='Zoom/Google Meet/Teams link')
    live_starts_at = models.DateTimeField(blank=True, null=True)
    notes_file = models.FileField(upload_to='lesson_notes/', blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.course.title} - {self.title}'

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student.username} -> {self.course.title}'
