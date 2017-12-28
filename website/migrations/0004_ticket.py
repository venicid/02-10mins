# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-12-28 06:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(choices=[('like', 'like'), ('dislike', 'dislike'), ('normal', 'normal')], max_length=10)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='website.Video')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voter_tickets', to='website.UserProfile')),
            ],
        ),
    ]
