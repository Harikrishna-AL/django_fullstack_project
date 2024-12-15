from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()

class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
