# Generated by Django 2.0.2 on 2018-05-10 21:04

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.query_utils


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20180510_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='content_type',
            field=models.ForeignKey(blank=True, limit_choices_to=django.db.models.query_utils.Q(django.db.models.query_utils.Q(('model', 'question'), ('app_label', 'core'), _connector='AND'), django.db.models.query_utils.Q(('model', 'answer'), ('app_label', 'core'), _connector='AND'), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
