# Generated by Django 2.0.2 on 2018-05-10 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20180510_2058'),
        ('notifications', '0006_auto_20180510_2029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='content_template',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='related_question',
        ),
        migrations.RemoveField(
            model_name='usersnotification',
            name='notification',
        ),
        migrations.AddField(
            model_name='usersnotification',
            name='content_template',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='usersnotification',
            name='related_question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Question'),
        ),
        migrations.AddField(
            model_name='usersnotification',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]