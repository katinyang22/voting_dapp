from django.db import models
from django.contrib.auth.models import AbstractUser
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django import forms

# Extend User model if needed
class User(AbstractUser):
    pass

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    def __str__(self):
        return self.user.username

# Election model for multiple elections
class Election(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

# Candidate model linked to a specific election
class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="candidates")
    name = models.CharField(max_length=255)
    vote_count = models.PositiveIntegerField(default=0)

# Voter model to prevent duplicate votes
class Voter(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="voters")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="voter_profile")
    has_voted = models.BooleanField(default=False)

# Voting function with real-time updates
class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.candidate.vote_count += 1
        self.candidate.save()
        self.broadcast_vote_update()
    
    def broadcast_vote_update(self):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"election_{self.election.id}",
            {
                "type": "vote.update",
                "election_id": self.election.id,
                "candidate_id": self.candidate.id,
                "vote_count": self.candidate.vote_count,
            }
        )
