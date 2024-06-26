# Generated by Django 5.0.3 on 2024-03-16 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('court_type', models.CharField(choices=[('clay', 'Clay'), ('grass', 'Grass'), ('hardcourt', 'Hardcourt')], max_length=20)),
                ('court_location', models.CharField(choices=[('indoors', 'Indoors'), ('outside', 'Out-side')], max_length=20)),
                ('has_lighting', models.BooleanField(default=False)),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
