# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-29 17:31
from __future__ import unicode_literals

import api_server.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_server', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaasCredential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_name', models.CharField(max_length=50)),
                ('password_seed', models.CharField(default=api_server.models.make_secret, max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='paas_password_seed',
        ),
        migrations.AddField(
            model_name='paascredential',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paas_credential_set', to='api_server.Profile'),
        ),
        migrations.AlterUniqueTogether(
            name='paascredential',
            unique_together=set([('profile', 'provider_name')]),
        ),
    ]
