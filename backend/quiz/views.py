from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .models import Room


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
        
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