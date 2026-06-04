# Generated starter migration for Merchant Navy education app
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=160)),
                ('subtitle', models.CharField(blank=True, max_length=220)),
                ('description', models.TextField()),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='course_thumbnails/')),
                ('level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner', max_length=20)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('is_published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teaching_courses', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=160)),
                ('description', models.TextField(blank=True)),
                ('session_type', models.CharField(choices=[('recorded', 'Recorded'), ('live', 'Live')], default='recorded', max_length=20)),
                ('video_file', models.FileField(blank=True, null=True, upload_to='recordings/')),
                ('video_url', models.URLField(blank=True, help_text='YouTube/Vimeo/private streaming URL')),
                ('live_link', models.URLField(blank=True, help_text='Zoom/Google Meet/Teams link')),
                ('live_starts_at', models.DateTimeField(blank=True, null=True)),
                ('notes_file', models.FileField(blank=True, null=True, upload_to='lesson_notes/')),
                ('order', models.PositiveIntegerField(default=1)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.course')),
            ],
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='courses.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL)),
            ],
            options={'unique_together': {('student', 'course')}},
        ),
    ]
