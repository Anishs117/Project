# Generated by Django 4.2.7 on 2023-11-20 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0002_remove_medicineprescription_dosage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='bill_no',
            field=models.CharField(default=1, editable=False, max_length=10),
        ),
        migrations.AlterField(
            model_name='medicinebill',
            name='patient_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appcms.patient'),
        ),
        migrations.AlterField(
            model_name='medicinebill',
            name='staff_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appcms.staff'),
        ),
    ]
