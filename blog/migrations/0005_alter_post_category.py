# Generated by Django 5.0.6 on 2024-09-29 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='tags', to='blog.category'),
        ),
    ]