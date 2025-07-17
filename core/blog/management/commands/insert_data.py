from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from accounts.models import CustomUser
from blog.models import Post, Category


class Command(BaseCommand):
    help = "Always generate 10 new users, categories, and 50–100 posts"

    def handle(self, *args, **kwargs):
        fake = Faker()

        self.stdout.write("Creating 10 new CustomUsers and profiles...")

        new_profiles = []
        for _ in range(10):
            user = CustomUser.objects.create_user(
                email=fake.unique.email(), password="Test@123456"
            )
            profile = user.profile
            profile.first_name = fake.first_name()
            profile.last_name = fake.last_name()
            profile.bio = fake.paragraph(nb_sentences=3)
            profile.birth_date = fake.date_of_birth(minimum_age=18, maximum_age=60)
            profile.save()
            new_profiles.append(profile)

        self.stdout.write(self.style.SUCCESS("Successfully created 10 users"))

        fixed_categories = ["IT", "Design", "Fun", "Science", "Health"]
        self.stdout.write("Ensuring categories exist (fixed + random)...")

        categories = []
        for name in fixed_categories:
            cat, _ = Category.objects.get_or_create(name=name)
            categories.append(cat)

        for _ in range(5):
            name = fake.unique.word().capitalize()
            cat, _ = Category.objects.get_or_create(name=name)
            categories.append(cat)

        self.stdout.write(
            self.style.SUCCESS(f"Total categories: {Category.objects.count()}")
        )

        post_count = random.randint(50, 100)
        self.stdout.write(f"Creating {post_count} fake blog posts...")

        for _ in range(post_count):
            post = Post.objects.create(
                title=fake.sentence(nb_words=6),
                author=random.choice(new_profiles),
                status=random.choice([True, False]),
                content=fake.paragraph(nb_sentences=10),
                published_at=fake.date_time_between(
                    start_date="-1y", end_date="now", tzinfo=timezone.utc
                ),
            )
            post.category.set(random.sample(categories, random.randint(1, 3)))

        self.stdout.write(
            self.style.SUCCESS(f"Created {post_count} posts for 10 new users!")
        )
