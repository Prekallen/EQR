# Generated by Django 5.1.4 on 2025-01-24 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placeBoard', '0002_alter_placeboard_address_alter_placeboard_area_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placeboard',
            name='placeNum',
            field=models.CharField(max_length=20, verbose_name='업체 전화 번호'),
        ),
    ]
