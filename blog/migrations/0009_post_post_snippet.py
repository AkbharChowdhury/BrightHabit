# Generated by Django 5.0.6 on 2024-11-14 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_remove_post_title2'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_snippet',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]