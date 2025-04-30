from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name= 'team')
    name = models.CharField(max_length= 100, unique= True)
    members = models.TextField(help_text="enter seperated by commas")
    created_at = models.DateTimeField(auto_now_add= True)
    score = models.IntegerField(default=0)
    current_question_number = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-score', 'created_at']
    
class Question(models.Model):
    question_number = models.IntegerField(unique= True)
    points = models.IntegerField(default= 10)
    question_text = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question_number
    
    class Meta:
        ordering = ["question_number"]

