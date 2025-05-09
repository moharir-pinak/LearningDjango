# Generated by Django 5.2 on 2025-04-15 11:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CharVarity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='learningimages/')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(choices=[('py', 'Python'), ('java', 'Java'), ('cpp', 'C++'), ('js', 'JavaScript'), ('html', 'HTML'), ('css', 'CSS'), ('sql', 'SQL')], max_length=5)),
            ],
        ),
    ]
