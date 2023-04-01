# Generated by Django 4.1.7 on 2023-03-24 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CSV_Files',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('ultima_modificasion', models.DateTimeField()),
                ('peso', models.CharField(max_length=150)),
                ('link', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Estaciones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('link', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Registros_CSV',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField()),
                ('presion', models.FloatField()),
                ('temperatura', models.FloatField()),
                ('IWV', models.FloatField()),
                ('ZTD', models.FloatField()),
                ('RMS_ERROR', models.FloatField()),
                ('n_centros_procesamiento', models.FloatField()),
                ('id_CSV', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.csv_files')),
            ],
        ),
        migrations.AddField(
            model_name='csv_files',
            name='id_Estacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.estaciones'),
        ),
        migrations.AddField(
            model_name='csv_files',
            name='id_Year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.year'),
        ),
    ]