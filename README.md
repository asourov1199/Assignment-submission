# Pet Adoption & Rescue Platform

A complete Django assignment project where users can browse pets, search/filter them, create accounts, submit adoption requests, and track their request status. The project also includes a Django REST Framework API and Django Admin management.

## Features

### Website
- User registration, login and logout
- User profile page
- Pet list and pet detail pages
- Search/filter by pet name, type, breed, gender, location and adoption status
- Adoption application form for logged-in users
- User dashboard showing Pending / Approved / Rejected requests
- Responsive Bootstrap interface and success/error messages
- Pagination
- Favorite pets (bonus)

### Business Rules
1. Only pets with `Available` status accept new adoption requests.
2. A user cannot create more than one active `Pending` request for the same pet.
3. When an adoption request is approved, that pet becomes `Adopted`.
4. Other pending requests for the same pet are automatically marked `Rejected`.
5. An adopted pet no longer shows the Apply for Adoption button.

### Admin
Django Admin can add/edit/delete pets, upload pet images, change pet status, review adoption requests and set request status.

### REST API
- `GET /api/pets/`
- `GET /api/pets/<id>/`
- `POST /api/pets/` (staff only)
- `PUT/PATCH /api/pets/<id>/` (staff only)
- `DELETE /api/pets/<id>/` (staff only)
- `GET /api/adoptions/` (logged-in user's own requests)
- `POST /api/adoptions/` (logged-in user)
- `GET /api/adoptions/<id>/`
- `PUT/PATCH /api/adoptions/<id>/`
- `DELETE /api/adoptions/<id>/`
- Token login: `POST /api/token/`

Pet API examples:
- `/api/pets/?search=golden`
- `/api/pets/?animal_type=Dog`
- `/api/pets/?gender=Male`
- `/api/pets/?location=Dhaka`
- `/api/pets/?status=Available`
- `/api/pets/?page=2`

## Installation (Windows)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_pets
python manage.py runserver
```

Open:
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- API: http://127.0.0.1:8000/api/pets/

## Installation (Linux/macOS)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_pets
python manage.py runserver
```

## API Token Example

Send a POST request to `/api/token/` with:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Then send the returned token in protected API requests:

```text
Authorization: Token YOUR_TOKEN_HERE
```

## Project Structure

```text
Pet_Adoption_Rescue_Platform/
├── manage.py
├── requirements.txt
├── README.md
├── pet_rescue/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── pets/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── api_views.py
│   ├── serializers.py
│   ├── admin.py
│   ├── tests.py
│   ├── urls.py
│   ├── migrations/
│   └── management/commands/seed_pets.py
├── templates/
└── static/
```

## Submission
The repository is ready to push to GitHub. Keep these files in the repository:
- Source code
- `README.md`
- `requirements.txt`
- Database migrations

Do not commit your local virtual environment or SQLite database.
