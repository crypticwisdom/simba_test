# Generated by Django 4.0.4 on 2022-05-08 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0008_alter_task_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='state',
            new_name='status',
        ),
    ]
