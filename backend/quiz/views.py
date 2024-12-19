from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'quiz/index.html')

# room code in the function quiz_room
def quiz_room(request, room_code):
    return render(request, 'quiz/quiz.html', {
        'room_code': room_code
    })

def login(request):
    return render(request, 'login.html')

def room(request):
    return render(request, 'room.html')