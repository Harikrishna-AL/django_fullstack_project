from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    code = models.CharField(max_length=6, unique=True)  # Room code
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_rooms')
    participants = models.ManyToManyField(User, related_name='joined_rooms')
    is_active = models.BooleanField(default=False)  # Whether the quiz has started
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    text = models.TextField()
    difficulty = models.IntegerField(default=1)  # Difficulty level for dynamic allocation
    category = models.CharField(max_length=50, blank=True)  # Optional categorization
    correct_answer = models.CharField(max_length=255, blank=True)
    choices = models.JSONField(default=list)  # Store multiple-choice options as JSON

class UserPerformance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    answered_questions = models.ManyToManyField(Question, blank=True)  # Questions already answered

class Leaderboard(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    rankings = models.JSONField(default=dict)  # E.g., {"user_id": score, ...}
