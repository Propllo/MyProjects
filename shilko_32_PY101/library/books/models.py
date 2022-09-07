from django.db import models


class Books(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=50)
    comment = models.TextField()

    def __str__(self):
        return self.title
