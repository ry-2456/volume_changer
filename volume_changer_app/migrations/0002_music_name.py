# Generated by Django 3.2.4 on 2021-07-12 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volume_changer_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='name',
            field=models.CharField(default='default', max_length=255),
            preserve_default=False,
        ),
    ]
