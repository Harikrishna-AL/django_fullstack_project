from django.urls import re_path, path
from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/quiz/$', consumers.QuizConsumer.as_asgi()),
# ]
websocket_urlpatterns = [
    path('ws/quiz/<str:room_code>/', consumers.QuizConsumer.as_asgi()),
]