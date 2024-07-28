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
  
  def get_created_by_username(self, obj):
        return obj.get_created_by_username()
      
  class Meta:
    model = Ticket
    fields = "__all__"
    
class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        # fields = ['title', 'description', 'due_date', 'priority', 'column_id']
        fields = "__all__"

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['created_by_username'] = self.context['request'].user.username
        return super().create(validated_data)
    
