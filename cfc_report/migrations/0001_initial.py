# Generated by Django 5.1.1 on 2024-10-18 22:46

import cfc_report.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                ("cfc_id", cfc_report.models.CfcIdField()),
            ],
        ),
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tournament",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("num_rounds", models.IntegerField()),
                ("date", models.DateField()),
                (
                    "pairing_system",
                    cfc_report.models.PairingSystem(
                        choices=[
                            ("SW", "Swiss"),
                            ("RR", "round robin"),
                            ("DR", "double round robin"),
                        ],
                        max_length=2,
                    ),
                ),
                (
                    "province",
                    cfc_report.models.Province(
                        choices=[
                            ("ON", "Ontario"),
                            ("QC", "Quebec"),
                            ("NS", "Nova Scotia"),
                            ("NB", "New Brunswick"),
                            ("MB", "Manitoba"),
                            ("BC", "British Columbia"),
                            ("PE", "Prince Edward Island"),
                            ("SK", "Saskatchewan"),
                            ("AB", "Alberta"),
                            ("NL", "Newfoundland and Labrador"),
                        ],
                        max_length=2,
                    ),
                ),
                ("to_cfc", cfc_report.models.CfcIdField()),
                ("td_cfc", cfc_report.models.CfcIdField()),
            ],
        ),
        migrations.CreateModel(
            name="TournamentDirector",
            fields=[
                (
                    "player_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="cfc_report.player",
                    ),
                ),
            ],
            bases=("cfc_report.player",),
        ),
        migrations.CreateModel(
            name="TournamentOrganizer",
            fields=[
                (
                    "player_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="cfc_report.player",
                    ),
                ),
            ],
            bases=("cfc_report.player",),
        ),
        migrations.CreateModel(
            name="Match",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "black",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="black_player",
                        to="cfc_report.player",
                    ),
                ),
                (
                    "white",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="white_player",
                        to="cfc_report.player",
                    ),
                ),
                (
                    "winner",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="winning_player",
                        to="cfc_report.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Roster",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "players",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cfc_report.player",
                    ),
                ),
            ],
        ),
    ]
