# Generated by Django 3.2.7 on 2021-11-23 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('google_oauth_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='google_oauth_app.course'),
        ),
    ]
