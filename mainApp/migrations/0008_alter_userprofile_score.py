# Generated by Django 4.2.16 on 2024-11-11 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0007_useranswer_is_expired_alter_useranswer_end_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="score",
            field=models.IntegerField(default=0, verbose_name="Pontuação do usuário"),
        ),
    ]
