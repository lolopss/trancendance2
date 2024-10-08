from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User  # Import Django's built-in User model

class Profile(models.Model):
    # Establish a one-to-one relationship with the Django built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    nickname = models.CharField(max_length=15)
    wins = models.IntegerField(default=0)  # Track the number of wins
    losses = models.IntegerField(default=0)  # Track the number of losses

    @property
    def winrate(self):
        # Calculate winrate as a percentage
        total_games = self.wins + self.losses
        if total_games == 0:
            return 0
        return (self.wins / total_games) * 100

    def __str__(self):
        return f"{self.user.username} Profile"
# Signal handler to create or update the Profile whenever the User is saved
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
