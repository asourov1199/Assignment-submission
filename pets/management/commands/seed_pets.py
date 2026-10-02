from django.core.management.base import BaseCommand
from pets.models import Pet


class Command(BaseCommand):
    help = 'Add a few demo pets for local testing.'

    def handle(self, *args, **options):
        pets = [
            dict(name='Max', animal_type='Dog', breed='Golden Retriever', age=2, gender='Male', location='Dhaka', description='Max is friendly, playful and loves people.'),
            dict(name='Luna', animal_type='Cat', breed='Domestic Shorthair', age=1, gender='Female', location='Gazipur', description='Luna is calm, curious and enjoys quiet homes.'),
            dict(name='Coco', animal_type='Bird', breed='Budgerigar', age=1, gender='Male', location='Dhaka', description='Coco is active and comfortable around people.'),
            dict(name='Milo', animal_type='Rabbit', breed='Mini Lop', age=2, gender='Male', location='Narayanganj', description='Milo is gentle and easy to handle.'),
        ]
        created = 0
        for data in pets:
            _, was_created = Pet.objects.get_or_create(name=data['name'], defaults=data)
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f'Added {created} new demo pet(s).'))
