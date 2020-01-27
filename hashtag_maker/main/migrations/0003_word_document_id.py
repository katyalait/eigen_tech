# Generated by Django 2.2 on 2020-01-27 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_sentence_word'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='document_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='main.Document'),
            preserve_default=False,
        ),
    ]