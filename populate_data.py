import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')
django.setup()

from django.utils import timezone
from faker import Faker
from hangarin.models import Priority, Category, Task, Note, SubTask

fake = Faker()

def populate():
    # 1. Populate Priority records
    priorities = ['High', 'Medium', 'Low', 'Critical', 'Optional']
    priority_objs = [Priority.objects.get_or_create(name=p)[0] for p in priorities]

    # 2. Populate Category records
    categories = ['Work', 'School', 'Personal', 'Finance', 'Projects']
    category_objs = [Category.objects.get_or_create(name=c)[0] for c in categories]

    statuses = ["Pending", "In Progress", "Completed"]

    # 3. Generate Fake Tasks, Notes, and SubTasks
    for _ in range(15):
        task = Task.objects.create(
            title=fake.sentence(nb_words=5),
            description=fake.paragraph(nb_sentences=3),
            deadline=timezone.make_aware(fake.date_time_this_month()),
            status=fake.random_element(elements=statuses),
            category=random.choice(category_objs),
            priority=random.choice(priority_objs),
        )

        Note.objects.create(
            task=task,
            content=fake.paragraph(nb_sentences=2)
        )

        SubTask.objects.create(
            parent_task=task,
            title=fake.sentence(nb_words=4),
            status=fake.random_element(elements=statuses)
        )

    print("Database populated successfully.")

if __name__ == '__main__':
    populate()