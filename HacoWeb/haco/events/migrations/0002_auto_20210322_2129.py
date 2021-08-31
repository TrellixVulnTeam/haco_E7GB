# Generated by Django 3.1.7 on 2021-03-22 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('bright_ti4', models.FloatField()),
                ('scan', models.FloatField()),
                ('track', models.FloatField()),
                ('acq_date', models.CharField(max_length=255)),
                ('acq_time', models.CharField(max_length=255)),
                ('satellite', models.CharField(max_length=100)),
                ('severity', models.CharField(max_length=100)),
                ('version', models.CharField(max_length=100)),
                ('bright_ti5', models.FloatField()),
                ('frp', models.FloatField()),
                ('daynight', models.CharField(max_length=1)),
            ],
        ),
        migrations.DeleteModel(
            name='WildfireEvent',
        ),
    ]
