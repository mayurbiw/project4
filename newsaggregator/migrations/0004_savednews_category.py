# Generated by Django 3.0.4 on 2020-05-27 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsaggregator', '0003_savednews_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='savednews',
            name='category',
            field=models.CharField(default='general', max_length=64),
            preserve_default=False,
        ),
    ]
