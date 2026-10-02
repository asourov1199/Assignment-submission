# Assignment Summary

## Project: Pet Adoption & Rescue Platform

This project was built with Django and Django REST Framework. It has two parts: a normal template-based website for users and a REST API.

### Main work completed
- User registration, login, logout and profile
- Pet listing, pet details and image support
- Search and filtering by the required pet information
- Adoption application form and personal request dashboard
- Django Admin for pet and adoption management
- Business rules for pet availability and duplicate pending requests
- REST API for pets and adoption requests
- API search/filtering, pagination and token authentication
- Bonus favorite-pet feature

### Important business logic
- Users can apply only when a pet is available.
- The same user cannot keep two pending requests for the same pet.
- Approving a request changes the pet status to Adopted.
- Other pending requests for that pet are rejected.
- Users can only see their own adoption requests through the API.

### Submission note
After testing locally, create a GitHub repository, push this project, and submit the repository URL along with the included README, requirements file, and migrations.
