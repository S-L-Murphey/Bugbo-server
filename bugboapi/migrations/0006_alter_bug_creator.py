# Generated by Django 3.2.7 on 2021-09-13 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bugboapi', '0005_auto_20210913_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='bugboapi.employee'),
        ),
    ]