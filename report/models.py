from django.db import models


class Report(models.Model):
    """A CFC tournament report"""
    name = models.CharField(max_length=20)
    tournament_director = models.CharField(max_length=20)
    tournament_organizer = models.CharField(max_length=20)
