from django.db import models
from django.utils import timezone

# Create your models here.

class CharVarity(models.Model):
    LEARNING_TYPES_CHOICES = [
        ('py', 'Python'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('js', 'JavaScript'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('sql', 'SQL'),
    ]

    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='learningimages/')
    date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=5, choices=LEARNING_TYPES_CHOICES)
    
    def __str__(self):
        return self.name
