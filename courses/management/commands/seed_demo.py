from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson

class Command(BaseCommand):
    help = 'Create demo SeaLearn Academy courses and YouTube lessons for client demo.'

    def handle(self, *args, **options):
        User = get_user_model()
        owner = User.objects.filter(is_superuser=True).first() or User.objects.filter(is_staff=True).first()
        if owner is None:
            owner = User.objects.create_superuser(username='owner', email='owner@sealearn.local', password='Owner@12345')
            self.stdout.write(self.style.WARNING('Created demo owner: username=owner password=Owner@12345'))

        data = [
            {
                'title': 'DNS Preparation Basics',
                'subtitle': 'Start your Merchant Navy foundation with simple concepts.',
                'description': 'A beginner-friendly demo course for SeaLearn Academy students preparing for DNS and Merchant Navy entrance learning.',
                'level': 'beginner',
                'lessons': [
                    ('Merchant Navy Career Overview', 'Understand career path, ship life and training expectations.', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
                    ('Basic Navigation Concepts', 'Introduction to navigation, charts and bridge watchkeeping.', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
                ],
            },
            {
                'title': 'Marine Engineering Introduction',
                'subtitle': 'Learn ship machinery basics through recorded sessions.',
                'description': 'A demo course covering basic engine room systems, safety practices and machinery awareness.',
                'level': 'beginner',
                'lessons': [
                    ('Engine Room Overview', 'Basic parts of engine room and duties of engineering cadets.', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
                    ('Safety Systems Onboard', 'Introduction to safety equipment and emergency readiness.', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
                ],
            },
            {
                'title': 'Navigation & Seamanship',
                'subtitle': 'Bridge watchkeeping, rules and practical ship knowledge.',
                'description': 'A demo course for basic seamanship concepts, COLREG awareness and bridge discipline.',
                'level': 'intermediate',
                'lessons': [
                    ('Rules of the Road', 'Simple introduction to collision prevention concepts.', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
                    ('Bridge Equipment', 'Overview of important bridge equipment and usage.', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
                ],
            },
        ]

        created_courses = 0
        created_lessons = 0
        for item in data:
            course, made = Course.objects.get_or_create(
                title=item['title'],
                defaults={
                    'subtitle': item['subtitle'],
                    'description': item['description'],
                    'level': item['level'],
                    'price': 0,
                    'is_published': True,
                    'tutor': owner,
                }
            )
            if made:
                created_courses += 1
            for order, (title, desc, url) in enumerate(item['lessons'], start=1):
                lesson, lmade = Lesson.objects.get_or_create(
                    course=course,
                    title=title,
                    defaults={
                        'description': desc,
                        'session_type': 'recorded',
                        'video_url': url,
                        'order': order,
                    }
                )
                if lmade:
                    created_lessons += 1

        self.stdout.write(self.style.SUCCESS(f'Demo ready: {created_courses} courses and {created_lessons} lessons created.'))
