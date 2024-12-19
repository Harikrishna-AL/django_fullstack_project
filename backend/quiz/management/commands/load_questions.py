import json
from django.core.management.base import BaseCommand
from quiz.models import Question

class Command(BaseCommand):
    help = 'Load questions from a JSON file into the database'

    def handle(self, *args, **kwargs):
        with open('questions.json', 'r') as file:
            data = json.load(file)

        for item in data:
            question, created = Question.objects.get_or_create(
                text=item['text'],
                defaults={
                    'options': item['options'],
                    'correct_answer': item['correct_answer'],
                    'difficulty': item['difficulty']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added question: {item['text']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Question already exists: {item['text']}"))
