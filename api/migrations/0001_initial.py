# Generated by Django 3.2.2 on 2021-05-11 18:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('name', models.CharField(max_length=100)),
                ('mode', models.CharField(choices=[('fixed-incomeRenda fixa', 'Fixed Income'), ('variable-incomeRenda Variável', 'Variable Income'), ('cryptoCripto Moeda', 'Crypto')], max_length=100)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('amount', models.IntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('ip_address', models.CharField(max_length=15)),
                ('request_date', models.DateTimeField()),
                ('is_redemption', models.BooleanField()),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.asset')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
