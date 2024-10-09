from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Report(models.Model):
    """A CFC tournament report"""
    name = models.CharField(max_length=20)
    TD_cfc = models.IntegerField(
        validators=[MinValueValidator(100000),
                    MaxValueValidator(999999)])
    TO_cfc = models.IntegerField(
        validators=[MinValueValidator(100000),
                    MaxValueValidator(999999)])

    def __str__(self):
        return "Report name: {self.name}, TD CFC: {self.cfc_id}, TO CFC: {self.TO_cfc}"


class Player(models.Model):
    """A chess player"""
    name = models.CharField(max_length=20)
    cfc_id = models.IntegerField(
        validators=[MinValueValidator(100000),
                    MaxValueValidator(999999)])

    def __str__(self):
        return "Player: {self.name} CFC: {self.cfc_id}"


class TournamentDirector(models.Model):
    """A tournament director for a chess tournament."""
    name = models.CharField(max_length=20)
    cfc_id = models.IntegerField(
        validators=[MinValueValidator(100000),
                    MaxValueValidator(999999)])

    def __str__(self):
        return f"Tournament Director: {self.name}, CFC: {self.cfc_id}"


class TournamentOrganizer(models.Model):
    """A tournament director for a chess tournament."""
    name = models.CharField(max_length=20)
    cfc_id = models.IntegerField(
        validators=[MinValueValidator(100000),
                    MaxValueValidator(999999)])

    def __str__(self):
        return f"Tournament Organizer: {self.name}, CFC: {self.cfc_id}"


class Tournament(models.Model):
    """A CFC rated chess tournament"""
    name = models.CharField(max_length=30)
    num_rounds = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"""Tournament name: { self.name }
        Number of rounds: { self.num_rounds }
        date: {self.date}"""
