from rest_framework import serializers
from .models import Candidate, CustomUser, Election, Vote
from django.contrib.auth import authenticate

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
    
    def validate(self, data):
        voter = data.get('voter')
        candidate = data.get('candidate')
        if Vote.objects.filter(voter=voter, candidate=candidate).exists():
            raise serializers.ValidationError("You have already voted for this candidate.")
        return data

class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=100)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'password', 'last_login', 'username', 'first_name',
                  'last_name', 'date_joined', 'email', 'is_active']
    
    extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        """
        Creates a new user profile from the request's data
        """
        account = CustomUser(**validated_data)
        account.set_password(account.password)
        account.save()

        # user_profile = UserProfileModel.objects.create(account=account, **validated_data)
        return account
    
    def update(self, instance, validated_data):
        """
        Updates a user's profile from the request's data
        """
        instance.set_password(instance.password)
        validated_data["password"] = instance.password
        return super().update(instance, validated_data)


# class RegisterSerializer(serializers.ModelSerializer):
#     # password = serializers.CharField(write_only = True, read)

#     class Meta:
#         model = CustomUser
#         fields = {'username', 'email', 'password'}
    
#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password']
#         )

#         return user


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         user = authenticate(**data)
#         if user and user.is_active:
#             return user
#         raise serializers.ValidationError("Invalid credentials")