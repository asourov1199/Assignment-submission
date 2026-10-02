from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AdoptionRequestForm, RegisterForm
from .models import AdoptionRequest, Favorite, Pet


def home(request):
    available_pets = Pet.objects.filter(status=Pet.Status.AVAILABLE)[:6]
    context = {
        'available_pets': available_pets,
        'pet_count': Pet.objects.count(),
        'available_count': Pet.objects.filter(status=Pet.Status.AVAILABLE).count(),
        'adopted_count': Pet.objects.filter(status=Pet.Status.ADOPTED).count(),
    }
    return render(request, 'pets/home.html', context)


def pet_list(request):
    pets = Pet.objects.all()
    search = request.GET.get('search', '').strip()
    animal_type = request.GET.get('animal_type', '').strip()
    breed = request.GET.get('breed', '').strip()
    gender = request.GET.get('gender', '').strip()
    location = request.GET.get('location', '').strip()
    status = request.GET.get('status', '').strip()

    if search:
        pets = pets.filter(
            Q(name__icontains=search)
            | Q(animal_type__icontains=search)
            | Q(breed__icontains=search)
            | Q(location__icontains=search)
        )
    if animal_type:
        pets = pets.filter(animal_type=animal_type)
    if breed:
        pets = pets.filter(breed__icontains=breed)
    if gender:
        pets = pets.filter(gender=gender)
    if location:
        pets = pets.filter(location__icontains=location)
    if status:
        pets = pets.filter(status=status)

    paginator = Paginator(pets, 8)
    page_obj = paginator.get_page(request.GET.get('page'))
    params = request.GET.copy()
    params.pop('page', None)

    context = {
        'page_obj': page_obj,
        'animal_types': Pet.AnimalType.choices,
        'genders': Pet.Gender.choices,
        'statuses': Pet.Status.choices,
        'query_string': params.urlencode(),
    }
    return render(request, 'pets/pet_list.html', context)


def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    is_favorite = False
    pending_request = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, pet=pet).exists()
        pending_request = AdoptionRequest.objects.filter(
            user=request.user,
            pet=pet,
            status=AdoptionRequest.Status.PENDING,
        ).exists()
    return render(
        request,
        'pets/pet_detail.html',
        {'pet': pet, 'is_favorite': is_favorite, 'pending_request': pending_request},
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    context = {
        'request_count': request.user.adoption_requests.count(),
        'favorite_count': request.user.favorites.count(),
    }
    return render(request, 'pets/profile.html', context)


@login_required
def apply_adoption(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if pet.status != Pet.Status.AVAILABLE:
        messages.error(request, 'This pet has already been adopted and is no longer available.')
        return redirect('pet_detail', pk=pet.pk)

    if AdoptionRequest.objects.filter(
        user=request.user,
        pet=pet,
        status=AdoptionRequest.Status.PENDING,
    ).exists():
        messages.warning(request, 'You already have a pending request for this pet.')
        return redirect('pet_detail', pk=pet.pk)

    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption = form.save(commit=False)
            adoption.user = request.user
            adoption.pet = pet
            try:
                adoption.save()
            except Exception as exc:
                form.add_error(None, str(exc))
            else:
                messages.success(request, f'Your adoption request for {pet.name} was submitted.')
                return redirect('dashboard')
    else:
        form = AdoptionRequestForm()

    return render(request, 'pets/adoption_form.html', {'form': form, 'pet': pet})


@login_required
def dashboard(request):
    requests = request.user.adoption_requests.select_related('pet').all()
    favorites = request.user.favorites.select_related('pet').all()
    return render(request, 'pets/dashboard.html', {'adoption_requests': requests, 'favorites': favorites})


@login_required
def toggle_favorite(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, pet=pet)
    if created:
        messages.success(request, f'{pet.name} was added to your favorites.')
    else:
        favorite.delete()
        messages.info(request, f'{pet.name} was removed from your favorites.')
    return redirect('pet_detail', pk=pet.pk)
