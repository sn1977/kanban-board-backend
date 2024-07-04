from rest_framework import serializers
from kanbanboard.models import Ticket


class TicketListSerializer(serializers.ModelSerializer):
  # created_at = serializers.SerializerMethodField()
  # due_date = serializers.SerializerMethodField()
  # created_by_name = serializers.SerializerMethodField()

  def get_created_at(self, obj):
    return obj.created_at  
  
  def get_due_date(self, obj):
    return obj.due_date  
  
  # def get_created_by_name(self, obj):
  #       return obj.get_created_by_name()
      
  class Meta:
    model = Ticket
    fields = "__all__"
