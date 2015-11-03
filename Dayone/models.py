from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=255)


class Entry(models.Model):
    uuid = models.CharField(unique=True, max_length=32)
    date = models.DateTimeField(db_index=True)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
