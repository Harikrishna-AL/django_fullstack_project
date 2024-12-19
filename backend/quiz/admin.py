from django.contrib import admin

# Register your models here.
from .models import Room, Question, UserPerformance, Leaderboard

admin.site.register(Room)
admin.site.register(Question)
admin.site.register(UserPerformance)
admin.site.register(Leaderboard)



