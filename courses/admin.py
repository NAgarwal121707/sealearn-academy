from django.contrib import admin
from .models import Course, Lesson, Enrollment


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'price', 'is_published', 'owner_name', 'created_at')
    list_filter = ('level', 'is_published')
    search_fields = ('title', 'description')
    inlines = [LessonInline]

    def owner_name(self, obj):
        return obj.tutor or 'SeaLearn Owner'
    owner_name.short_description = 'Owner'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'session_type', 'live_starts_at', 'order')
    list_filter = ('session_type',)
    search_fields = ('title', 'course__title')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    search_fields = ('student__username', 'course__title')
