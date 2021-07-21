# Generated by Django 3.2.4 on 2021-07-20 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stroke', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageUploadModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.ImageField(upload_to='images/%Y/%m/%d')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Capture',
        ),
        migrations.DeleteModel(
            name='Discriminate_Stroke',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='post',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.DeleteModel(
            name='Upload',
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]