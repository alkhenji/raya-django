from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import Startup, Investor, Deal
from faker import Faker
import random

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database population...')

        # Create 10 users
        users = []
        for _ in range(10):
            user = User.objects.create_user(
                email=fake.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number(),
            )
            users.append(user)

        # Create 10 startups
        startups = []
        for _ in range(10):
            startup = Startup.objects.create(
                name=fake.company(),
                description=fake.text(max_nb_chars=200),
                website=fake.url(),
                founding_date=fake.date_between(start_date='-5y', end_date='today'),
                industry=fake.random_element(elements=('Tech', 'Healthcare', 'Finance', 'Education', 'E-commerce')),
                location=fake.city(),
                funding_stage=fake.random_element(elements=('Seed', 'Series A', 'Series B', 'Series C')),
                total_funding=random.randint(100000, 10000000),
                team_size=random.randint(5, 100),
                founder=random.choice(users),
            )
            startups.append(startup)

        # Create 10 investors
        investors = []
        for _ in range(10):
            investor = Investor.objects.create(
                name=fake.company(),
                description=fake.text(max_nb_chars=200),
                website=fake.url(),
                investment_focus=fake.random_element(elements=('Tech', 'Healthcare', 'Finance', 'Education', 'E-commerce')),
                investment_stage=fake.random_element(elements=('Seed', 'Early Stage', 'Growth Stage', 'Late Stage')),
                min_investment=random.randint(50000, 500000),
                max_investment=random.randint(1000000, 10000000),
                location=fake.city(),
                representative=random.choice(users),
            )
            investors.append(investor)

        # Create 10 deals
        for _ in range(10):
            Deal.objects.create(
                startup=random.choice(startups),
                investor=random.choice(investors),
                amount=random.randint(100000, 5000000),
                equity_percentage=random.uniform(5.0, 25.0),
                deal_date=fake.date_between(start_date='-2y', end_date='today'),
                status=fake.random_element(elements=('Pending', 'Completed', 'Failed')),
                description=fake.text(max_nb_chars=200),
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database!')) 