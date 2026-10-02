from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import AdoptionRequest, Pet


class AdoptionBusinessLogicTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('rahim', password='pass12345')
        self.user2 = User.objects.create_user('karim', password='pass12345')
        self.pet = Pet.objects.create(
            name='Max', animal_type='Dog', breed='Golden Retriever', age=2,
            gender='Male', location='Dhaka', description='Friendly and playful.'
        )

    def make_request(self, user):
        return AdoptionRequest.objects.create(
            user=user, pet=self.pet, phone='01700000000', address='Dhaka',
            reason='I want to give this pet a safe home.', previous_pet_experience=True
        )

    def test_same_user_cannot_create_two_pending_requests(self):
        self.make_request(self.user1)
        duplicate = AdoptionRequest(
            user=self.user1, pet=self.pet, phone='01800000000', address='Dhaka',
            reason='Another request', previous_pet_experience=False
        )
        with self.assertRaises(ValidationError):
            duplicate.save()

    def test_approving_request_marks_pet_adopted(self):
        request = self.make_request(self.user1)
        request.status = AdoptionRequest.Status.APPROVED
        request.save()
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.status, Pet.Status.ADOPTED)

    def test_approving_rejects_other_pending_requests(self):
        request1 = self.make_request(self.user1)
        request2 = self.make_request(self.user2)
        request1.status = AdoptionRequest.Status.APPROVED
        request1.save()
        request2.refresh_from_db()
        self.assertEqual(request2.status, AdoptionRequest.Status.REJECTED)
