# Generated by Django 5.0.2 on 2024-02-15 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('release_date', models.DateField()),
                ('reviews_count', models.IntegerField()),
                ('positive_reviews_percent', models.FloatField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('img', models.URLField()),
                ('url', models.URLField()),
            ],
        ),
    ]
