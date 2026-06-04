# SeaLearn Academy - Owner + Student Django App

This project is now configured for one SeaLearn Academy owner and many students.

## Roles

- Owner: create with `python manage.py createsuperuser`
- Student: signup from `/accounts/signup/student/`

There is no tutor signup. The owner uploads and manages all courses, videos, live classes and notes.

## Run locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## Important URLs

- Home: `/`
- Student signup: `/accounts/signup/student/`
- Login: `/accounts/login/`
- Student dashboard: `/accounts/dashboard/`
- Owner dashboard: `/courses/owner/`
- Admin panel: `/admin/`

## Upload flow

1. Login as owner/superuser.
2. Open Owner Dashboard.
3. Create a course.
4. Add video/live class inside course.
5. Click Publish when students should see it.

Draft courses are visible to owner only. Published courses are visible to students.
