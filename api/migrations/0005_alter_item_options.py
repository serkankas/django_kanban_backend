# Generated by Django 4.2.3 on 2023-07-18 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_item_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['category__id', 'order_id']},
        ),
    ]
