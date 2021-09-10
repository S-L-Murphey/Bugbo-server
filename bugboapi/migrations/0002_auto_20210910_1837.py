# Generated by Django 3.2.7 on 2021-09-10 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bugboapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='bug',
            name='priority',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bugboapi.priority'),
            preserve_default=False,
        ),
    ]