# SeaLearn Academy - Owner + Student Django App

This version is ready for a live demo with:

- Neon PostgreSQL database
- Render web hosting
- Cloudinary media uploads for course thumbnails, notes and recorded video files
- One SeaLearn Academy owner account
- Student signup/login flow

## Roles

- Owner: create with `python manage.py createsuperuser`
- Student: signup from `/accounts/signup/student/`

There is no tutor signup. The owner uploads and manages all courses, videos, live classes and notes.

## Local setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
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

## Environment variables

Create `.env` locally:

```env
SECRET_KEY=replace-with-your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=your-neon-database-url
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

Use the same `CLOUDINARY_URL` from your previous project if you want both projects to share the same Cloudinary account.

## Upload flow

1. Login as owner/superuser.
2. Open Owner Dashboard.
3. Create a course.
4. Add a recorded video from desktop/gallery using the video file field, or add a live class link.
5. Click Publish when students should see it.

Draft courses are visible to owner only. Published courses are visible to students.

## Render deployment

Build command:

```bash
./build.sh
```

Start command:

```bash
gunicorn merchant_edu.wsgi:application
```

Add these Render environment variables:

```env
PYTHON_VERSION=3.11.9
SECRET_KEY=your-render-secret-key
DEBUG=False
DATABASE_URL=your-neon-database-url
CLOUDINARY_URL=your-cloudinary-url
```

After deploy, open Render Shell and run:

```bash
python manage.py createsuperuser
```
