from django.forms import ValidationError
from rest_framework import generics
from .models import ChatMessage
from .serializers import ChatMessageSerializer, MessageSerializer, UserSerializer
from django.contrib.auth import authenticate, login, logout
from knox.models import AuthToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import  User


class ChatMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]  # Restrict to authenticated users only

    def get_queryset(self):
        # Get query parameters
        room_id = self.request.query_params.get('room')
        receiver_id = self.request.query_params.get('receiver')

        # Start with all messages
        queryset = ChatMessage.objects.all()

        # Filter by room if provided
        if room_id:
            queryset = queryset.filter(room_id=room_id)

        # Filter by receiver if provided
        if receiver_id:
            queryset = queryset.filter(receiver_id=receiver_id)

        return queryset.order_by("timestamp")  # Return ordered by timestamp


    def perform_create(self, serializer):
        # # Save the message with the sender as the logged-in user
        # receiver = self.request.data.get("receiver")
        # room = self.request.data.get("room")

        #  # Validate: Only one of receiver or room should be provided
        # if receiver and room:
        #     raise ValidationError("Specify only one: receiver for direct message or room for group message.")
        # # Save the message, adding the sender as the current user
        # serializer.save(
        #     sender=self.request.user,
        #     receiver=receiver if receiver else None,
        #     room=room if room else None
        # )

        serializer.save()

class LoginApIView(APIView):
    """
    handles User activities such as Login and Logout
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handles log in of the user
        """
        
        email = request.data.get("email")
        password = request.data.get("password")
        print(email, password)
        user = authenticate(username=email, password=password)
        print(f"user object {user}")

        # if user exists
        if user:
            serializer = UserSerializer(user)
            login(request, user)
            data = serializer.data
            data['token'] = AuthToken.objects.create(user=user)[1]
            return Response(data, status=status.HTTP_200_OK)
        # user doesn't exist
        else:
            data = {
                "message": "Invalid User Credentials",
                }
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)

# class LogoutAPIView(APIView):
#     """
#     Handles User logout
#     """
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         """
#         Handles log out of the user
#         """
#         logout(request)
#         return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)



class RegisterUsersAPIView(APIView):
    """
    Handles Registatration of Users
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handles registration of Users
        """
        data = {
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "email": request.data.get("email"),
            "password": request.data.get("password"),
        }
        # making the username same as the email
        data['username'] = request.data.get("email")

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message': "User Successfully registered",
                }
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSearchAPIView(APIView):
    """
    Handles searching for a user or retrieving all users
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handles getting all users or searching for a specific user
        """
        query = request.query_params.get('q')

        if query:
            users = User.objects.filter(email__icontains=query)
        else:
            users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)