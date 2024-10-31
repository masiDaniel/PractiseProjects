from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from .serializers import  CandidateSerializer, ElectionSerializer, MessageSerializer, UserSerializer, VoteSerializer
from knox.models import AuthToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser, Election, Vote, Candidate

# Create your views here.
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

class LogoutAPIView(APIView):
    """
    Handles User logout
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handles log out of the user
        """
        logout(request)
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)



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
            users = CustomUser.objects.filter(email__icontains=query)
        else:
            users = CustomUser.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VotesAPIView(APIView):
    """
    Handles deasling with votes
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handles getting all votes
        """

        #can improve this for future purposes
        # query = request.query_params.get('q')
        # if query:
        #     users = CustomUser.objects.filter(email__icontains=query)
        # else:
        #     users = CustomUser.objects.all()

        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, candidate_id, *args, **kwargs):
        print(f"this is the request {request}")
        user = request.user
        candidate = get_object_or_404(Candidate, id=candidate_id)
        election = candidate.election  # Get the election associated with the candidate

        # Check if the user has already voted for this candidate
        # if Vote.objects.filter(voter=user, candidate=candidate).exists():
        #     return Response({"message": "You have already voted for this candidate."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has already voted in this election
        if Vote.objects.filter(voter=user,  candidate__election=election).exists():
            return Response({"message": "You have already voted."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the vote
        Vote.objects.create(voter=user, candidate=candidate)
        return Response({"message": "Your vote has been recorded!"}, status=status.HTTP_201_CREATED)


class ElectionsAPIView(APIView):
    """
    Handles deasling with elections
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handles getting all elections
        """

        #can improve this for future purposes
        # query = request.query_params.get('q')
        # if query:
        #     users = CustomUser.objects.filter(email__icontains=query)
        # else:
        #     users = CustomUser.objects.all()

        elections = Election.objects.all()
        serializer = ElectionSerializer(elections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CandidatesAPIView(APIView):
    """
    handles all the candidate issues
    """

    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        """
        handles getting all the candidates
        """

        candidate = Candidate.objects.all()
        serializer = CandidateSerializer(candidate, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)