from django.db import models


class Books(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.TextField()
    
    def __str__(self):
        return self.title
    
