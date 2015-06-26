# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QandA', '0002_remove_answer_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
