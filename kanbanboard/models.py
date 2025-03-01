from django.conf import settings
from django.db import models
import datetime

# Create your models here.
class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=30)
    created_at = models.DateField(default=datetime.date.today)
    due_date = models.DateField()
    priority = models.CharField(max_length=30)
    column_id = models.CharField(max_length=30)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_by_username = models.CharField(blank=True, max_length=150)
    color = models.CharField(blank=True, max_length=30)
    
    def __str__(self) -> str:
        # return str(self.id) + ' ' + self.title
        return f'({self.id}) {self.title}'
      
       
