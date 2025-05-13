from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
User = get_user_model()
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    

class Thread(models.Model):
    # FRIENDS = 'FRI'
    # PENDING = 'PEN'
    # GROUP = 'GRP'

    # THREAD_STATUS_CHOICES = [
    #     (FRIENDS, 'Friends'),
    #     (PENDING, 'Pending'),
    #     (GROUP, 'Group'),
    # ]

    THREAD_TYPE = [
        ('GRP', 'Group'),
        ('PSN', 'Personal')
    ]
    users = models.ManyToManyField(User, related_name='chat_users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    last_message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    thread_type =  models.CharField(choices=THREAD_TYPE, blank=True, null=True)
    # status = models.CharField(choices=THREAD_STATUS_CHOICES, blank=True, null=True)
    def __str__(self):
        return f"Thread ({self.pk})"



class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender=models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read=models.BooleanField(default=False)
    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)