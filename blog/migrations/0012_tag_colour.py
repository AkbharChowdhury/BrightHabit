# Generated by Django 5.0.6 on 2024-11-14 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_post_post_snippet'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='colour',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
