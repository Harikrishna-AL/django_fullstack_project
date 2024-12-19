from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Count

from django.http import JsonResponse
from django.shortcuts import redirect
from .models import Room, Question, UserPerformance


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'redirect_url': '/quiz/room/', 'token': str(RefreshToken.for_user(user))})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)
        
class JoinRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_code):
        try:
            room = Room.objects.get(code=room_code)
            room.participants.add(request.user)
            return Response({'message': 'Joined room successfully!'})
        except Room.DoesNotExist:
            return Response({'error': 'Room does not exist'}, status=404)
        
def index(request):
    return render(request, 'index.html')

# room code in the function quiz_room
def quiz_room(request, room_code):
    if not request.user.is_authenticated:
        return redirect('/quiz/login')
    
    return render(request, 'quiz.html', {
        'room_code': room_code
    })

def login_view(request):
    return render(request, 'login.html')

# @login_required(login_url='/quiz/login', redirect_field_name='')
def room(request):
    if not request.user.is_authenticated:
        return redirect('/quiz/login')
    data = {
        'authenticated': request.user.is_authenticated,
        'username': request.user.username
    }
    return render(request, 'room.html', context=data)

def dashboard(request):
    return render(request, 'dashboard.html')


class DashboardView(APIView):
    def post(self, request, room_code):
        try:
            # Fetch the room
            room = Room.objects.get(code=room_code)

            # Total participants
            total_participants = room.participants.count()

            # Difficulty breakdown
            difficulty_stats = Question.objects.all()\
                .values('difficulty')\
                .annotate(count=Count('difficulty'))

            # Correct answers count
            user_performance = UserPerformance.objects.filter(room=room)
            correct_answers = sum([(perf.score / 10) for perf in user_performance])

            # Build response
            data = {
                'total_participants': total_participants,
                'difficulty_stats': list(difficulty_stats),
                'correct_answers': correct_answers,
            }
            return JsonResponse(data, status=200)
        except Room.DoesNotExist:
            return JsonResponse({'error': 'Room not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)