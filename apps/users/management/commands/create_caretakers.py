import random
import string
from django.core.management.base import BaseCommand
from ...models import CustomUser

EMAILS = [
    "caretaker.agira@thapar.edu",
    "caretaker.amritam@thapar.edu",
    "caretaker.prithvi@thapar.edu",
    "caretaker.neeram@thapar.edu",
    "caretaker.vasudhae@thapar.edu",
    "caretaker.frfg@thapar.edu",
    "caretaker.vasudhag@thapar.edu",
    "caretaker.vyan@thapar.edu",
    "caretaker.ira@thapar.edu",
    "caretaker.ambaram@thapar.edu",
    "caretaker.viyat@thapar.edu",
    "caretaker.anantam@thapar.edu",
    "caretaker.ananta@thapar.edu",
    "caretaker.vyom@thapar.edu",
    "caretaker.dhriti@thapar.edu",
    "caretaker.vahni@thapar.edu",
    "caretaker.tejas@thapar.edu",
]

HOSTELS = [
    "Agira Hall",
    "Amritam Hall",
    "Prithvi Hall",
    "Neeram Hall",
    "Vasudha Hall Block E",
    "Hostel FRFG",
    "Vasudha Hall Block G",
    "Vyan Hall",
    "Ira Hall",
    "Ambaram Hall",
    "Viyat Hall",
    "Anantam Hall",
    "Ananta Hall",
    "Vyom Hall",
    "Dhriti Hall",
    "Vahni Hall",
    "Tejas Hall",
]

def random_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def random_contact():
    return ''.join(random.choices(string.digits, k=10))

from apps.nightpass.models import Hostel
from apps.users.models import Security

class Command(BaseCommand):
    help = 'Create caretaker users with random passwords and contacts.'

    def handle(self, *args, **options):
        import csv
        credentials = []
        for email, hostel_name in zip(EMAILS, HOSTELS):
            password = random_password()
            contact = random_contact()

            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={
                    'user_type': 'security',
                    'is_staff': True,
                }
            )

            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created {email} | Hostel: {hostel_name} | Contact: {contact} | Password: {password}"))
                credentials.append({'email': email, 'password': password})
            else:
                self.stdout.write(self.style.WARNING(f"User {email} already exists."))
                credentials.append({'email': email, 'password': 'Already Exists'})

            # Create or get Hostel object
            hostel_obj, _ = Hostel.objects.get_or_create(
                name=hostel_name,
                defaults={
                    'contact_number': contact,
                    'email': email,
                }
            )
            hostel_obj.save()

            # Create or get Security object for this user and hostel
            security_obj, sec_created = Security.objects.get_or_create(
                user=user,
                defaults={
                    'name': hostel_name + " Caretaker",
                    'hostel': hostel_obj,
                }
            )

            security_obj.save()
            if sec_created:
                self.stdout.write(self.style.SUCCESS(f"Linked Security object for {email} and {hostel_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Security object for {email} already exists."))

        # Write credentials to CSV file
        with open('caretaker_credentials.csv', 'w', newline='') as csvfile:
            fieldnames = ['email', 'password']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in credentials:
                writer.writerow(row)
        self.stdout.write(self.style.SUCCESS('Caretaker credentials written to caretaker_credentials.csv'))

            
