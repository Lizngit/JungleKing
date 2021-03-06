# Generated by Django 3.0.8 on 2020-09-09 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0003_auto_20200908_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='position',
            field=models.CharField(max_length=64, null=True, verbose_name='机房位置'),
        ),
        migrations.AlterField(
            model_name='cabinet',
            name='position',
            field=models.CharField(max_length=64, null=True, verbose_name='域位置'),
        ),
        migrations.AlterField(
            model_name='domain',
            name='position',
            field=models.CharField(max_length=64, null=True, verbose_name='区位置'),
        ),
    ]
