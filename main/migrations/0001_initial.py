# Generated by Django 4.1.3 on 2023-02-02 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nr_matricol', models.CharField(max_length=32)),
            ],
        ),
    ]
