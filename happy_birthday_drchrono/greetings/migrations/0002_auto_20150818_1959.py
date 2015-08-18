# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('greetings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='happybirthday',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
