# Generated by Django 3.1.7 on 2021-03-24 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitteeMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('PR', 'President'), ('VP', 'Vice President'), ('SC', 'Secretary'), ('TR', 'Treasurer'), ('MB', 'Member')], max_length=2)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.personalprofile')),
            ],
            options={
                'verbose_name': 'Committee member',
                'verbose_name_plural': 'Committee members',
                'ordering': ['member'],
            },
        ),
    ]
