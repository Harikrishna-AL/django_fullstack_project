# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class QuizConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = "quiz_room"
#         self.room_group_name = f"quiz_{self.room_name}"

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']

#         # Broadcast the message to the group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import Room, Question, UserPerformance, Leaderboard

# from django.db.models import Q
# import random

# def get_next_question(user, room):
#     # Exclude already answered questions
#     answered_ids = UserPerformance.objects.get(user=user, room=room).answered_questions.values_list('id', flat=True)

#     # Filter questions based on difficulty and exclude already answered
#     questions = Question.objects.filter(~Q(id__in=answered_ids)).order_by('difficulty')
    
#     # Randomly pick one question
#     return random.choice(questions) if questions.exists() else None

# def update_leaderboard(room):
#     leaderboard = Leaderboard.objects.get(room=room)
#     performances = UserPerformance.objects.filter(room=room)
#     leaderboard.rankings = {
#         str(performance.user.id): performance.score
#         for performance in performances.order_by('-score')
#     }
#     leaderboard.save()


# class QuizConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_code = self.scope['url_route']['kwargs']['room_code']
#         self.room_group_name = f'quiz_{self.room_code}'

#         print(f'Connected to room {self.room_code}')
#         # Add user to room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Remove user from room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         action = data.get('action')

#         if action == 'join_room':
#             await self.join_room(data)
#         elif action == 'start_quiz':
#             await self.start_quiz(data)
#         elif action == 'submit_answer':
#             await self.submit_answer(data)

#     async def join_room(self, data):
#         user = self.scope['user']
#         room = Room.objects.get(code=self.room_code)
#         room.participants.add(user)
#         print(f'{user.username} has joined the room!')

#         # Notify participants
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'room_update',
#                 'message': f'{user.username} has joined the room!'
#             }
#         )

#     async def start_quiz(self, data):
#         room = Room.objects.get(code=self.room_code)
#         room.is_active = True
#         room.save()

#         # Notify participants
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'quiz_start',
#                 'message': 'The quiz has started!'
#             }
#         )

#     async def submit_answer(self, data):
#         user = self.scope['user']
#         room = Room.objects.get(code=self.room_code)
#         question_id = data.get('question_id')
#         answer = data.get('answer')

#         question = Question.objects.get(id=question_id)
#         performance = UserPerformance.objects.get(user=user, room=room)

#         # Check answer and update score
#         if question.correct_answer == answer:
#             performance.score += 10  # Add points for correct answer
#         performance.answered_questions.add(question)
#         performance.save()

#         # Update leaderboard
#         update_leaderboard(room)

#         # Notify participants
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'leaderboard_update',
#                 'leaderboard': Leaderboard.objects.get(room=room).rankings
#             }
#         )

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Question, UserPerformance, Leaderboard
from asgiref.sync import sync_to_async
from django.db.models import Q
import random
import json

async def get_next_question(user, room):
    try:
        # Get answered question IDs for the user in the room
        answered_ids = await sync_to_async(
            lambda: list(UserPerformance.objects.get(user=user, room=room).answered_questions.values_list('id', flat=True))
        )()

        # Fetch unanswered questions
        questions = await sync_to_async(
            lambda: list(Question.objects.filter(~Q(id__in=answered_ids)).order_by('difficulty'))
        )()

        return random.choice(questions) if questions else None

    except UserPerformance.DoesNotExist:
        # Log the error and return None if UserPerformance doesn't exist
        return None


async def update_leaderboard(room):
    # Fetch leaderboard and performances asynchronously
    leaderboard = await sync_to_async(lambda: Leaderboard.objects.get(room=room))()
    performances = await sync_to_async(
        lambda: list(UserPerformance.objects.filter(room=room).select_related('user'))
    )()

    # Build rankings in an async-friendly way
    async def build_rankings(performances):
        rankings = {}
        for performance in sorted(performances, key=lambda p: -p.score):
            user_id = await sync_to_async(lambda: performance.user.id)()
            rankings[str(user_id)] = performance.score
        return rankings

    rankings = await build_rankings(performances)
    leaderboard.rankings = rankings
    await sync_to_async(leaderboard.save)()





class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'quiz_{self.room_code}'

        print(f'Connected to room {self.room_code}')
        # Add user to room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove user from room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'join_room':
            await self.join_room(data)
        elif action == 'start_quiz':
            await self.start_quiz(data)
        elif action == 'submit_answer':
            await self.submit_answer(data)
        elif action == 'get_next_question':
            await self.send_next_question(data)
        elif action == 'host_info':
            await self.host_info(data)

    async def send_next_question(self, data):
        user = self.scope['user']
        room = await sync_to_async(lambda: Room.objects.get(code=self.room_code))()
        question = await get_next_question(user, room)

        print(f'Sending question: {question.text}')

        if question:
            await self.send(text_data=json.dumps({
                'type': 'next_question',
                'question': {
                    'id': question.id,
                    'text': question.text,
                    'options': question.options.split(',')
                }
            }))
        else:
            await self.send(text_data=json.dumps({
                'type': 'quiz_completed',
                'message': 'Quiz completed!'
            }))


    async def join_room(self, data):
        user = self.scope['user']
        room = await sync_to_async(lambda: Room.objects.get(code=self.room_code))()
        await sync_to_async(lambda: room.participants.add(user))()

        await sync_to_async(lambda: UserPerformance.objects.get_or_create(
        user=user,
        room=room,
        defaults={'score': 0}  # Initialize with a score of 0
        ))()

        await sync_to_async(lambda: Leaderboard.objects.get_or_create(room=room))()

        # Notify participants
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room_update',
                'message': f'{user.username} has joined the room!'
            }
        )

    async def room_update(self, event):
        """
        Handles room updates, such as when a new user joins.
        """
        message = event['message']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'room_update',
            'message': message,
        }))

    async def start_quiz(self, data):
        room = await sync_to_async(lambda: Room.objects.get(code=self.room_code))()
        room.is_active = True
        await sync_to_async(room.save)()

        # Notify participants
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'quiz_start',
                'message': 'The quiz has started!'
            }
        )

    async def quiz_start(self, event):
        """
        Handles the quiz start notification.
        """
        message = event['message']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'quiz_start',
            'message': message,
        }))
        
    # async def submit_answer(self, data):
    #     user = self.scope['user']
    #     room = await sync_to_async(lambda: Room.objects.get(code=self.room_code))()
    #     question_id = data.get('question_id')
    #     answer = data.get('answer')

    #     question = await sync_to_async(lambda: Question.objects.get(id=question_id))()
    #     performance = await sync_to_async(lambda: UserPerformance.objects.get(user=user, room=room))()

    #     # Check answer and update score
    #     if question.correct_answer == answer:
    #         performance.score += 10  # Add points for correct answer
    #     await sync_to_async(lambda: performance.answered_questions.add(question))()
    #     await sync_to_async(performance.save)()

    #     # Update leaderboard
    #     await update_leaderboard(room)

    #     # Notify participants
    #     leaderboard = await sync_to_async(lambda: Leaderboard.objects.get(room=room))()
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'leaderboard_update',
    #             'leaderboard': leaderboard.rankings
    #         }
    #     )
    async def host_info(self, data):
        user = self.scope['user']
        
        # Fetch room details asynchronously
        room = await sync_to_async(lambda: Room.objects.select_related('admin').get(code=self.room_code))()
        
        # Check if user is the host
        is_host = await sync_to_async(lambda: room.admin == user)()
        
        # Prepare the message
        message = 1 if is_host else 0

        # Notify participants
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'host_info_room',
                'message': message
            }
        )

    async def host_info_room(self, event):
        """
        Handles the host info room notification.
        """
        message = event['message']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'host_info_room',
            'message': message,
        }))


    async def submit_answer(self, data):
        user = self.scope['user']
        room = await sync_to_async(lambda: Room.objects.get(code=self.room_code))()
        question_id = data.get('question_id')
        answer = data.get('answer')

        question = await sync_to_async(lambda: Question.objects.get(id=question_id))()
        performance = await sync_to_async(lambda: UserPerformance.objects.get(user=user, room=room))()

        # Check answer and update score
        if question.correct_answer == answer:
            performance.score += 10  # Add points for correct answer
        await sync_to_async(lambda: performance.answered_questions.add(question))()
        await sync_to_async(performance.save)()

        # Ensure a leaderboard exists
        leaderboard, _ = await sync_to_async(lambda: Leaderboard.objects.get_or_create(room=room))()

        # Update leaderboard
        await update_leaderboard(room)

        # Notify participants
        leaderboard = await sync_to_async(lambda: Leaderboard.objects.get(room=room))()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'submit_answer',
                'leaderboard': leaderboard.rankings
            }
        )


