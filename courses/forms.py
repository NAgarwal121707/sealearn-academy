from django import forms
from .models import Course, Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'subtitle', 'description', 'thumbnail', 'level',
            'price', 'is_published'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            'course', 'title', 'description', 'session_type', 'video_file',
            'video_url', 'live_link', 'live_starts_at', 'notes_file', 'order'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'live_starts_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()
