# Generated by Django 3.1.7 on 2021-09-07 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_tag_classification'),
        ('recommend', '0013_alter_option_description'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='option',
            unique_together={('title', 'category', 'tag')},
        ),
    ]
