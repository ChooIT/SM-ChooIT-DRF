# Generated by Django 3.2.4 on 2021-06-25 05:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import recommend.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_auto_20210621_2044'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=10)),
                ('function1', models.CharField(max_length=10, null=True)),
                ('function2', models.CharField(max_length=10, null=True)),
                ('function3', models.CharField(max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('prod_no', models.AutoField(primary_key=True, serialize=False)),
                ('prod_name', models.CharField(max_length=100)),
                ('prod_manufacturer', models.CharField(max_length=30)),
                ('prod_price', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('prod_category', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='recommend.category')),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_no', models.AutoField(primary_key=True, serialize=False)),
                ('review_title', models.CharField(max_length=50, null=True)),
                ('review_text', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('func1_rate', models.CharField(choices=[('g', 'Good'), ('s', 'So so'), ('b', 'Bad')], default='s', max_length=1, verbose_name='function1 rate')),
                ('func2_rate', models.CharField(choices=[('g', 'Good'), ('s', 'So so'), ('b', 'Bad')], default='s', max_length=1, verbose_name='function2 rate')),
                ('func3_rate', models.CharField(choices=[('g', 'Good'), ('s', 'So so'), ('b', 'Bad')], default='s', max_length=1, verbose_name='function3 rate')),
                ('prod_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommend.product')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SearchLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('prod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='recommend.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReviewTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('review_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_tags', to='recommend.review')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.tag')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReviewImage',
            fields=[
                ('img_no', models.AutoField(primary_key=True, serialize=False)),
                ('img_path', models.ImageField(upload_to=recommend.utils.user_directory_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_no', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='review',
            name='review_img_thumbnail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recommend.reviewimage'),
        ),
        migrations.AddField(
            model_name='review',
            name='user_no',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prod_tags', to='recommend.product')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.tag')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('img_no', models.AutoField(primary_key=True, serialize=False)),
                ('prod_img_path', models.ImageField(upload_to=recommend.utils.user_directory_path)),
                ('prod_is_thumbnail', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('prod_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prod_images', to='recommend.product')),
                ('user_no', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fav_created_at', models.DateTimeField(auto_now_add=True)),
                ('fav_prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommend.product')),
                ('fav_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fav_created_at'],
            },
        ),
    ]
