# Generated by Django 3.1.3 on 2020-11-26 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_remove_quiz_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='gap',
            name='guess',
            field=models.CharField(default='', max_length=50),
        ),
    ]
