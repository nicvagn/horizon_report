from django.db import models


class Report(models.Model):
    """A CFC tournament report"""
    name = models.CharField(max_length=20)
    TD_cfc = models.CharField(max_length=6)
    TO_cfc = models.CharField(max_length=6)


class Player(models.Model):
    """A chess player"""
    name = models.CharField(max_length=20)
    cfc_id = models.CharField(max_length=6)


class TournamentDirector(models.Model):
    """A tournament director for a chess tournament."""
    name = models.CharField(max_length=20)
    cfc_id = models.CharField(max_length=6)
