from rest_framework import serializers

from .models import AdoptionRequest, Pet


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'animal_type', 'breed', 'age', 'gender', 'location',
            'description', 'image', 'status', 'created_at'
        ]
        read_only_fields = ['created_at']


class AdoptionRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    pet_name = serializers.CharField(source='pet.name', read_only=True)

    class Meta:
        model = AdoptionRequest
        fields = [
            'id', 'user', 'pet', 'pet_name', 'phone', 'address', 'reason',
            'previous_pet_experience', 'message', 'status', 'created_at'
        ]
        read_only_fields = ['user', 'status', 'created_at']

    def validate_pet(self, pet):
        if pet.status != Pet.Status.AVAILABLE:
            raise serializers.ValidationError('This pet has already been adopted.')
        return pet

    def validate(self, attrs):
        request = self.context.get('request')
        pet = attrs.get('pet') or getattr(self.instance, 'pet', None)
        if request and request.user.is_authenticated and pet:
            duplicate = AdoptionRequest.objects.filter(
                user=request.user,
                pet=pet,
                status=AdoptionRequest.Status.PENDING,
            )
            if self.instance:
                duplicate = duplicate.exclude(pk=self.instance.pk)
            if duplicate.exists():
                raise serializers.ValidationError('You already have a pending request for this pet.')
        return attrs

    def create(self, validated_data):
        return AdoptionRequest.objects.create(user=self.context['request'].user, **validated_data)
