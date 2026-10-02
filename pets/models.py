from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Q


class Pet(models.Model):
    class AnimalType(models.TextChoices):
        DOG = 'Dog', 'Dog'
        CAT = 'Cat', 'Cat'
        BIRD = 'Bird', 'Bird'
        RABBIT = 'Rabbit', 'Rabbit'
        OTHER = 'Other', 'Other'

    class Gender(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'

    class Status(models.TextChoices):
        AVAILABLE = 'Available', 'Available'
        ADOPTED = 'Adopted', 'Adopted'

    name = models.CharField(max_length=120)
    animal_type = models.CharField(max_length=20, choices=AnimalType.choices)
    breed = models.CharField(max_length=120)
    age = models.PositiveIntegerField(help_text='Age in years')
    gender = models.CharField(max_length=10, choices=Gender.choices)
    location = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.animal_type})'


class AdoptionRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        APPROVED = 'Approved', 'Approved'
        REJECTED = 'Rejected', 'Rejected'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adoption_requests')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_requests')
    phone = models.CharField(max_length=30)
    address = models.TextField()
    reason = models.TextField()
    previous_pet_experience = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'pet'],
                condition=Q(status='Pending'),
                name='unique_pending_request_per_user_pet',
            )
        ]

    def __str__(self):
        return f'{self.user.username} → {self.pet.name} ({self.status})'

    def clean(self):
        super().clean()
        if not self.pet_id:
            return

        # New pending/approved requests are valid only while the pet is available.
        if self.status in {self.Status.PENDING, self.Status.APPROVED}:
            original_status = None
            if self.pk:
                original_status = type(self).objects.filter(pk=self.pk).values_list('status', flat=True).first()
            already_approved = original_status == self.Status.APPROVED
            if self.pet.status != Pet.Status.AVAILABLE and not already_approved:
                raise ValidationError({'pet': 'This pet has already been adopted.'})

        duplicate = type(self).objects.filter(
            user_id=self.user_id,
            pet_id=self.pet_id,
            status=self.Status.PENDING,
        )
        if self.pk:
            duplicate = duplicate.exclude(pk=self.pk)
        if self.status == self.Status.PENDING and duplicate.exists():
            raise ValidationError('You already have a pending adoption request for this pet.')

    def save(self, *args, **kwargs):
        self.full_clean()
        with transaction.atomic():
            super().save(*args, **kwargs)
            if self.status == self.Status.APPROVED:
                Pet.objects.filter(pk=self.pet_id).update(status=Pet.Status.ADOPTED)
                type(self).objects.filter(
                    pet_id=self.pet_id,
                    status=self.Status.PENDING,
                ).exclude(pk=self.pk).update(status=self.Status.REJECTED)
                self.pet.status = Pet.Status.ADOPTED


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'pet'], name='unique_favorite_per_user_pet')
        ]

    def __str__(self):
        return f'{self.user.username} ♥ {self.pet.name}'
