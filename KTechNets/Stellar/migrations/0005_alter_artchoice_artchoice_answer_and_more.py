# Generated by Django 4.2.1 on 2023-05-29 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Stellar", "0004_remove_artchoice_artchoice_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artchoice",
            name="artchoice_answer",
            field=models.CharField(max_length=1200, null=True),
        ),
        migrations.AlterField(
            model_name="artchoice",
            name="artchoice_method",
            field=models.CharField(default="Sim", max_length=1200),
        ),
    ]
