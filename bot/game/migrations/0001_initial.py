# Generated by Django 3.1.3 on 2020-11-19 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(default='', max_length=200)),
                ('answer', models.CharField(default='', max_length=100)),
                ('category', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GuessWhat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_code', models.CharField(default='', max_length=50)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('answer', models.CharField(default='', max_length=50)),
                ('category', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(default='', max_length=200)),
                ('answer', models.CharField(default='', max_length=100)),
                ('category', models.CharField(default='', max_length=50)),
            ],
        ),
    ]
