from django.db.models import Q
from rest_framework import filters, permissions, viewsets

from .models import AdoptionRequest, Pet
from .serializers import AdoptionRequestSerializer, PetSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'animal_type', 'breed', 'location', 'description']

    def get_queryset(self):
        queryset = Pet.objects.all()
        params = self.request.query_params

        animal_type = params.get('animal_type')
        gender = params.get('gender')
        location = params.get('location')
        status = params.get('status')
        breed = params.get('breed')
        search = params.get('search')

        if animal_type:
            queryset = queryset.filter(animal_type__iexact=animal_type)
        if gender:
            queryset = queryset.filter(gender__iexact=gender)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if status:
            queryset = queryset.filter(status__iexact=status)
        if breed:
            queryset = queryset.filter(breed__icontains=breed)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(animal_type__icontains=search)
                | Q(breed__icontains=search)
                | Q(location__icontains=search)
            )
        return queryset


class AdoptionRequestViewSet(viewsets.ModelViewSet):
    serializer_class = AdoptionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AdoptionRequest.objects.filter(user=self.request.user).select_related('pet')
