# Generated by Django 3.2 on 2024-05-22 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_auto_20240522_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='type',
            field=models.CharField(choices=[('dodanie_zadania', 'Dodanie zadania'), ('zamkniecie_zadania', 'Zamknięcie zadania'), ('edycja_statusu', 'Edycja statusu'), ('edycja_tytulu', 'Edycja tytułu'), ('edycja_opisu', 'Edycja opisu'), ('edycja_etykiety', 'Edycja etykiet'), ('edycja_adresata', 'Edycja adresata')], max_length=50),
        ),
    ]