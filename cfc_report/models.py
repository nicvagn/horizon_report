from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# models relaiting to a CFC Rated chess tournament.


class Cfc_id(models.IntegerField):
    """A CFC ID field"""
    validators = [MinValueValidator(100000), MaxValueValidator(999999)]


class Player(models.Model):
    """A chess player"""
    name = models.CharField(max_length=20)
    cfc_id = Cfc_id()

    def __str__(self):
        return f"Player: {self.name} CFC: {self.cfc_id}"


class TournamentDirector(models.Model):
    """A tournament director for a chess tournament."""
    name = models.CharField(max_length=20)
    cfc_id = Cfc_id()

    def __str__(self):
        return f"Tournament Director: {self.name}, CFC: {self.cfc_id}"


class TournamentOrganizer(models.Model):
    """A tournament director for a chess tournament."""
    name = models.CharField(max_length=20)
    cfc_id = Cfc_id()

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
