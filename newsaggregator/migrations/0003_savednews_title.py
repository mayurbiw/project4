# Generated by Django 3.0.4 on 2020-05-20 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsaggregator', '0002_savednews'),
    ]

    operations = [
        migrations.AddField(
            model_name='savednews',
            name='title',
            field=models.CharField(default='a', max_length=64),
            preserve_default=False,
        ),
    ]
