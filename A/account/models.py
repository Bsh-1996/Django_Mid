from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Relations(models.Model):
    from_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'followers') # the pesron who wants to follow
    to_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'following') # the person who is been followed
    created_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f'{self.from_user.username} follows {self.to_user.username}'
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(null= True, blank= True)
    
