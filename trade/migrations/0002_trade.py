# Generated by Django 4.2.3 on 2023-07-22 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('trade_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=8, max_digits=15)),
                ('quantity', models.DecimalField(decimal_places=8, max_digits=15)),
                ('quote_quantity', models.DecimalField(decimal_places=8, max_digits=15)),
                ('timestamp', models.BigIntegerField()),
                ('is_buyer_maker', models.BooleanField()),
                ('is_best_match', models.BooleanField()),
            ],
        ),
    ]