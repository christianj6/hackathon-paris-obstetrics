# Generated by Django 3.0.2 on 2020-01-27 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_practice_features'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='practice',
            name='features',
        ),
        migrations.AddField(
            model_name='practice',
            name='f_bleeding',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=7),
        ),
        migrations.AddField(
            model_name='practice',
            name='f_breastfeed',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=7),
        ),
        migrations.AddField(
            model_name='practice',
            name='f_communication',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=7),
        ),
        migrations.AddField(
            model_name='practice',
            name='f_fetus',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=7),
        ),
        migrations.AddField(
            model_name='practice',
            name='f_medication',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=7),
        ),
        migrations.AddField(
            model_name='practice',
            name='f_placenta',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=7),
        ),
        migrations.AddField(
            model_name='practice',
            name='f_prepregnancy',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=7),
        ),
        migrations.AddField(
            model_name='practice',
            name='f_psychology',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=7),
        ),
        migrations.AddField(
            model_name='practice',
            name='f_research',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=7),
        ),
        migrations.AddField(
            model_name='practice',
            name='f_risks',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=7),
        ),
        migrations.AddField(
            model_name='practice',
            name='f_tools',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=7),
        ),
    ]