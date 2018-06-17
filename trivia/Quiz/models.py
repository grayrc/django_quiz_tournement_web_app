from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User

import requests

class Tournement(models.Model):

    DIFFICULTY = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
        )

    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY, default='Medium')
    category = models.CharField(max_length=100, default='General Knowledge')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(default=datetime.now(), blank=True)
    players = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.name
        
    
class Question(models.Model):
    tournement_id = models.ForeignKey(
        'Tournement',
        on_delete=models.CASCADE,
    )
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=100)
    incorrect_one = models.CharField(max_length=100)
    incorrect_two = models.CharField(max_length=100)
    incorrect_three = models.CharField(max_length=100)

class Score(models.Model):
    player_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
        )
    tournement_id = models.ForeignKey(
        'Tournement',
        on_delete=models.PROTECT,
    )
    score = models.IntegerField()