from django.contrib.auth.models import User
from django.db import models


class Questions(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class Answer(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    ans = models.CharField(max_length=50, null=True, blank=True)
    answer = models.CharField(max_length=50, null=True, blank=True)
    correct = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.answer}"


class CurrentGame(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Current GAME - N {self.question}"
