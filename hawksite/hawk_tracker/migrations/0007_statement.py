# Generated by Django 2.0.1 on 2018-03-03 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hawk_tracker', '0006_auto_20180302_2327'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement_title', models.CharField(default='Or find out what Hawkwatchers thinks about the latest Fed Statement!', max_length=1200)),
                ('statement_header', models.CharField(max_length=1200)),
                ('statement_text', models.CharField(max_length=1200)),
                ('statement_last', models.DateTimeField(verbose_name='date published')),
                ('statement_next', models.CharField(default='Next Fed Interest Rate Decision: March 21, 2018', max_length=1200)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hawk_tracker.Answer')),
            ],
        ),
    ]
