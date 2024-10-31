from rest_framework import serializers
from .models import ChatMessage, ChatRoom
from django.contrib.auth.models import  User

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)  # Make sender read-only
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required = False)
    room = serializers.PrimaryKeyRelatedField(queryset=ChatRoom.objects.all(), required = False)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender','receiver', 'room', 'message', 'timestamp']
    
    def validate(self, data):
        receiver = data.get('receiver')
        room = data.get('room')

        # Ensure that either receiver or room is provided, but not both
        if not receiver and not room:
            raise serializers.ValidationError("Either 'receiver' or 'room' must be provided.")
        if receiver and room:
            raise serializers.ValidationError("Specify only one: receiver for direct message or room for group message.")

        return data

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)

class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=100)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'last_login', 'username', 'first_name',
                  'last_name', 'date_joined', 'email', 'is_active']
    
    extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        """
        Creates a new user profile from the request's data
        """
        account = User(**validated_data)
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