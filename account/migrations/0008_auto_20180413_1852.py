# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_historicaluserprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluserprofile',
            name='mobile',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
