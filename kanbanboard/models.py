from django.conf import settings
from django.db import models


# Create your models here.
class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=30)
    column_id = models.IntegerField()
    crated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assigned_to = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        # return str(self.id) + ' ' + self.title
        return f'({self.id}) {self.title}'
