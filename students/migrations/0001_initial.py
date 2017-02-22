# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('subject', models.CharField(verbose_name='Title', max_length=256)),
                ('teacher', models.CharField(verbose_name='Teacher', max_length=256, blank=True)),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('notes', models.TextField(verbose_name='Notes', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(verbose_name='Title', max_length=256)),
                ('notes', models.TextField(verbose_name='Notes', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MonthJournal',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('date', models.DateField(verbose_name='Date')),
                ('present_day1', models.BooleanField(default=False)),
                ('present_day2', models.BooleanField(default=False)),
                ('present_day3', models.BooleanField(default=False)),
                ('present_day4', models.BooleanField(default=False)),
                ('present_day5', models.BooleanField(default=False)),
                ('present_day6', models.BooleanField(default=False)),
                ('present_day7', models.BooleanField(default=False)),
                ('present_day8', models.BooleanField(default=False)),
                ('present_day9', models.BooleanField(default=False)),
                ('present_day10', models.BooleanField(default=False)),
                ('present_day11', models.BooleanField(default=False)),
                ('present_day12', models.BooleanField(default=False)),
                ('present_day13', models.BooleanField(default=False)),
                ('present_day14', models.BooleanField(default=False)),
                ('present_day15', models.BooleanField(default=False)),
                ('present_day16', models.BooleanField(default=False)),
                ('present_day17', models.BooleanField(default=False)),
                ('present_day18', models.BooleanField(default=False)),
                ('present_day19', models.BooleanField(default=False)),
                ('present_day20', models.BooleanField(default=False)),
                ('present_day21', models.BooleanField(default=False)),
                ('present_day22', models.BooleanField(default=False)),
                ('present_day23', models.BooleanField(default=False)),
                ('present_day24', models.BooleanField(default=False)),
                ('present_day25', models.BooleanField(default=False)),
                ('present_day26', models.BooleanField(default=False)),
                ('present_day27', models.BooleanField(default=False)),
                ('present_day28', models.BooleanField(default=False)),
                ('present_day29', models.BooleanField(default=False)),
                ('present_day30', models.BooleanField(default=False)),
                ('present_day31', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('first_name', models.CharField(verbose_name='First Name', max_length=256)),
                ('last_name', models.CharField(verbose_name='Last Name', max_length=256)),
                ('middle_name', models.CharField(verbose_name='Middle Name', max_length=256, blank=True, default='')),
                ('birthday', models.DateField(verbose_name='Birthday', null=True)),
                ('photo', models.ImageField(verbose_name='Photo', blank=True, null=True, upload_to='')),
                ('ticket', models.CharField(verbose_name='Ticket', max_length=256)),
                ('notes', models.TextField(verbose_name='Notes', blank=True)),
                ('student_group', models.ForeignKey(verbose_name='Group', null=True, on_delete=django.db.models.deletion.PROTECT, to='students.Group')),
            ],
        ),
        migrations.AddField(
            model_name='monthjournal',
            name='student',
            field=models.ForeignKey(verbose_name='Student', unique_for_month='date', to='students.Student'),
        ),
        migrations.AddField(
            model_name='group',
            name='leader',
            field=models.OneToOneField(verbose_name='Leader', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='students.Student'),
        ),
        migrations.AddField(
            model_name='exam',
            name='group',
            field=models.OneToOneField(verbose_name='Group', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='students.Group'),
        ),
    ]
