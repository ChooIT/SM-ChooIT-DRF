# Generated by Django 3.2.4 on 2021-09-03 13:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recommend', '0008_auto_20210903_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttextcloud',
            name='user_no',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
