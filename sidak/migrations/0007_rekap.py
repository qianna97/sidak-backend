# Generated by Django 3.1 on 2021-10-02 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sidak', '0006_auto_20210930_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rekap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Rekap',
            },
        ),
    ]
