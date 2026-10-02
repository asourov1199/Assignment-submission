from django.contrib import admin
from .models import AdoptionRequest, Favorite, Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_type', 'breed', 'gender', 'location', 'status', 'created_at')
    list_filter = ('animal_type', 'gender', 'status', 'location')
    search_fields = ('name', 'breed', 'location')
    list_editable = ('status',)


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'pet__name', 'phone', 'reason')
    list_select_related = ('user', 'pet')
    readonly_fields = ('created_at',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'created_at')
    search_fields = ('user__username', 'pet__name')
