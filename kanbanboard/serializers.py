from rest_framework import serializers
from kanbanboard.models import Ticket
from rest_framework.serializers import ModelSerializer, CharField  # Füge ModelSerializer hinzu
from django.contrib.auth.models import User


class TicketListSerializer(serializers.ModelSerializer):
  """
  Serializer class for the Ticket model to serialize and deserialize ticket data.
  """
    
  class Meta:
    """
    The `Meta` class provides additional metadata for the `Ticket` serializer.
    It specifies the model to be used and the fields to include in the serialization.
    """

    model = Ticket
    fields = "__all__"
    
class TicketCreateSerializer(serializers.ModelSerializer):
  """
  Serializer class for creating a new ticket.

  This serializer is used to validate and deserialize the data provided
  when creating a new ticket. It includes all fields of the `Ticket` model.

  Example usage:
  ```
  serializer = TicketCreateSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
  else:
    # Handle invalid data
  ```
  """

  class Meta:
    model = Ticket
    fields = "__all__"
    
class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

   
