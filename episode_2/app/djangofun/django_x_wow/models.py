from django.db import models


class Character(models.Model):
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=10)
    realm = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.region}: {self.realm} - {self.name}"
