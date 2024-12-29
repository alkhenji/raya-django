from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import InvestorProfile, StartupProfile, IndividualProfile, Deal
from django.utils import timezone
from datetime import timedelta
import random
import decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating dummy data...')
        
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write('Superuser created')

        # Sample data
        INDUSTRIES = ['Fintech', 'Healthtech', 'E-commerce', 'SaaS', 'AI/ML', 'Cleantech', 'Edtech']
        LOCATIONS = ['San Francisco', 'New York', 'London', 'Berlin', 'Singapore', 'Dubai', 'Tokyo']
        
        # Create Investors
        investor_users = []
        for i in range(10):
            user = User.objects.create_user(
                username=f'investor{i}',
                email=f'investor{i}@example.com',
                password='password123',
                user_type='investor'
            )
            investor_users.append(user)
            
            InvestorProfile.objects.create(
                user=user,
                company_name=f'Investment Firm {i}',
                description=f'A leading investment firm specializing in {random.choice(INDUSTRIES)}',
                website=f'https://investor{i}.com',
                location=random.choice(LOCATIONS),
                founded_year=random.randint(1990, 2020),
                team_size=random.randint(5, 100),
                preferred_industries=[random.choice(INDUSTRIES) for _ in range(3)],
                preferred_stages=['seed', 'series_a', 'series_b'],
                investment_range_min=decimal.Decimal(random.randint(50000, 500000)),
                investment_range_max=decimal.Decimal(random.randint(1000000, 5000000)),
                sectors_of_interest=[random.choice(INDUSTRIES) for _ in range(3)],
                total_investments=random.randint(10, 50),
                total_capital_deployed=decimal.Decimal(random.randint(5000000, 50000000)),
                verified=random.choice([True, False]),
                linkedin_url=f'https://linkedin.com/company/investor{i}',
                crunchbase_url=f'https://crunchbase.com/company/investor{i}'
            )
        self.stdout.write('Created investors')

        # Create Startups
        startup_users = []
        for i in range(20):
            user = User.objects.create_user(
                username=f'startup{i}',
                email=f'startup{i}@example.com',
                password='password123',
                user_type='startup'
            )
            startup_users.append(user)
            
            StartupProfile.objects.create(
                user=user,
                company_name=f'Startup {i}',
                tagline=f'Revolutionizing {random.choice(INDUSTRIES)}',
                description=f'An innovative startup in the {random.choice(INDUSTRIES)} space',
                industry=random.choice(INDUSTRIES),
                stage=random.choice(['seed', 'series_a', 'series_b']),
                founding_date=timezone.now() - timedelta(days=random.randint(365, 1825)),
                location=random.choice(LOCATIONS),
                team_size=random.randint(2, 50),
                revenue_range=random.choice(['pre_revenue', '0-100k', '100k-500k', '500k-1m']),
                website=f'https://startup{i}.com',
                linkedin_url=f'https://linkedin.com/company/startup{i}',
                crunchbase_url=f'https://crunchbase.com/company/startup{i}',
                total_funding_raised=decimal.Decimal(random.randint(0, 5000000)),
                current_funding_target=decimal.Decimal(random.randint(1000000, 10000000)),
                min_ticket_size=decimal.Decimal(random.randint(50000, 250000)),
                equity_offering=decimal.Decimal(random.randint(5, 20)),
                key_metrics={
                    'mrr': random.randint(0, 100000),
                    'users': random.randint(100, 10000),
                    'growth_rate': random.randint(10, 100)
                },
                verified=random.choice([True, False])
            )
        self.stdout.write('Created startups')

        # Create Individuals
        for i in range(15):
            user = User.objects.create_user(
                username=f'individual{i}',
                email=f'individual{i}@example.com',
                password='password123',
                user_type='individual'
            )
            
            IndividualProfile.objects.create(
                user=user,
                first_name=f'First{i}',
                last_name=f'Last{i}',
                title=f'Professional Title {i}',
                company=f'Company {i}',
                interests=[random.choice(INDUSTRIES) for _ in range(3)],
                linkedin_url=f'https://linkedin.com/in/individual{i}',
                verified=random.choice([True, False])
            )
        self.stdout.write('Created individuals')

        # Create Deals
        startups = StartupProfile.objects.all()
        for startup in startups:
            num_deals = random.randint(1, 3)
            for _ in range(num_deals):
                deal = Deal.objects.create(
                    title=f'Investment Round for {startup.company_name}',
                    description=f'Seeking investment to scale {random.choice(["operations", "product development", "market expansion"])}',
                    startup=startup,
                    deal_type=random.choice(['equity', 'convertible_note', 'safe']),
                    status=random.choice(['draft', 'active', 'in_discussion', 'due_diligence', 'closed']),
                    amount=decimal.Decimal(random.randint(500000, 5000000)),
                    equity_offered=decimal.Decimal(random.randint(5, 25)),
                    min_investment=decimal.Decimal(random.randint(25000, 100000)),
                    target_close_date=timezone.now() + timedelta(days=random.randint(30, 180)),
                    industry=startup.industry,
                    terms_and_conditions=f'Standard terms for {startup.stage} investment'
                )
                
                # Add some interested and committed investors
                investors = list(InvestorProfile.objects.all())
                random.shuffle(investors)
                deal.interested_investors.add(*investors[:random.randint(1, 5)])
                deal.committed_investors.add(*investors[:random.randint(1, 3)])
                
                # Update deal progress
                committed_investors = deal.committed_investors.all()
                deal.number_of_investors = len(committed_investors)
                deal.amount_raised = decimal.Decimal(sum(random.randint(100000, 500000) for _ in range(deal.number_of_investors)))
                deal.save()
                
        self.stdout.write('Created deals')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with dummy data')) 