from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



# Create your models here.

class Post(models.Model):
    title= models.CharField(max_length=100)
    image = models.ImageField(null = True, blank = True, upload_to='images/')
    price = models.IntegerField(default= '')
    locality = models.CharField(max_length=20, default= '')
    Type_of_property = models.CharField(max_length= 20, default='')
    superficy = models.IntegerField(default='')
    content= models.TextField()
    date_posted= models.DateTimeField(default= timezone.now)
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    favourites = models.ManyToManyField(User, related_name= 'favourite', default=None, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class MessageModel(models.Model):
    thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    Image = models.ImageField(upload_to='message_photos/', blank=True, null = True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)


class Notification(models.Model):
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null= True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null= True)
    thread =models.ForeignKey('ThreadModel', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)

RATE_CHOICES = [
    (1, '1- Horrible'),
    (2, '2- Bad'),
    (3, '3- OK'),
    (4, '4- Good'),
    (5, '5- Perfect'),

]
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=3000, blank=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)


    def __str__(self):
        return self.user.username




