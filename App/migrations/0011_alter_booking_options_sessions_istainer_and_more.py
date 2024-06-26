# Generated by Django 5.0.3 on 2024-04-20 09:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_booking_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='sessions',
            name='isTainer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sessions',
            name='price',
            field=models.PositiveIntegerField(default=42000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('pendig', 'Pendig'), ('done', 'Done'), ('paid', 'Paid'), ('cancled', 'Cancled')], default='pendig', max_length=10),
        ),
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.ImageField(upload_to='img/upload', validators=[django.core.validators.validate_image_file_extension]),
        ),
    ]
