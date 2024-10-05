from django.db import models


class Player(models.Model):
    """A chess player with a cfc_id"""
    # players name
    name = models.CharField(max_length=20)
    # player's CFC id
    cfc_id = models.IntegerField()
