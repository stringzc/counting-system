# Generated by Django 3.2.8 on 2023-08-17 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_plun_uci'),
    ]

    operations = [
        migrations.CreateModel(
            name='BASIC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('STARTTIME', models.DateTimeField(null=True, verbose_name='STARTTIME')),
                ('Checkincooldown', models.IntegerField(verbose_name='Checkincooldown')),
                ('Commentonthecooldown', models.IntegerField(verbose_name='Commentonthecooldown')),
            ],
        ),
        migrations.CreateModel(
            name='black',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.IntegerField(verbose_name='uid')),
            ],
        ),
    ]
