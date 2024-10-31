from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    """
    the default User model can be uses as is but if you want to add custom fields,
    you can extend the AbstractUser model
    """

    bio = models.TextField(null=True, blank=True)

class Election(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.name



class Vote(models.Model):
    voter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'candidate')  # Prevents duplicate votes for the same candidate by the same user

    def __str__(self):
        return f"{self.voter} for {self.candidate}"