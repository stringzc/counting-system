# Generated by Django 3.2.8 on 2023-07-27 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20230727_0359'),
    ]

    operations = [
        migrations.CreateModel(
            name='UandP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.IntegerField(verbose_name='cid')),
                ('power', models.IntegerField(verbose_name='power')),
            ],
        ),
    ]