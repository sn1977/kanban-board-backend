from rest_framework import serializers
from kanbanboard.models import Ticket


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

   
