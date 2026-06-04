from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    STUDENT = 'student'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    bio = models.TextField(blank=True)
    qualification = models.CharField(max_length=180, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user.is_staff or self.user.is_superuser:
            return f'{self.user.username} - SeaLearn Owner'
        return f'{self.user.username} - Student'

    @property
    def is_student(self):
        return self.role == self.STUDENT
